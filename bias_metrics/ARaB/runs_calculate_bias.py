import collections
from re import M
import numpy as np
import pickle


docs_bias_paths = {'tc':"data/msmarco_passage_docs_bias_tc.pkl",
                        'bool':"data/msmarco_passage_docs_bias_bool.pkl",
                        'tf':"data/msmarco_passage_docs_bias_tf.pkl"}

at_ranklist = [5, 10, 20, 30, 50, 100]

root_path = "../../trec_runs/215_neutral_queries/bert_base_uncased/"
# the path of these run files should be set
experiments = {'run_file_biased': root_path + "ranked_list_original.trec",
                'run_file_unbiased': root_path + 'ranked_list_fairness_aware.trec',
               }


#Loading saved document bias values
docs_bias = {}
for _method in docs_bias_paths:
    print (_method)
    with open(docs_bias_paths[_method], 'rb') as fr:
        docs_bias[_method] = pickle.load(fr)

#Loading run files
runs_docs_bias = {}
    
print ('reading run')
for exp_name in experiments:
    print (exp_name)

    run_path = experiments[exp_name]
    runs_docs_bias[exp_name] = {}
    
    for _method in docs_bias_paths:
        runs_docs_bias[exp_name][_method] = {}
    
    with open(run_path) as fr:
        qryid_cur = 0
        for i, line in enumerate(fr):
            if (i % 5000000 == 0) and (i != 0):
                print ('line', i)

            vals = line.strip().split(' ')
            if len(vals) == 6:
                qryid = int(vals[0])
                docid = int(vals[2])
                
                if qryid != qryid_cur:
                    for _method in docs_bias_paths:
                        runs_docs_bias[exp_name][_method][qryid] = []
                    qryid_cur = qryid
                for _method in docs_bias_paths:
                    runs_docs_bias[exp_name][_method][qryid].append(docs_bias[_method][docid])
      
    for _method in docs_bias_paths:
        print (_method, len(runs_docs_bias[exp_name][_method].keys()))
    print ()
print ('done!')

def calc_RaB_q(bias_list, at_rank):
    bias_val = np.mean([x[0] for x in bias_list[:at_rank]])
    bias_feml_val = np.mean([x[1] for x in bias_list[:at_rank]])
    bias_male_val = np.mean([x[2] for x in bias_list[:at_rank]])

    return bias_val, bias_feml_val, bias_male_val


def calc_ARaB_q(bias_list, at_rank):
    _vals = []
    _feml_vals = []
    _male_vals = []
    for t in range(at_rank):
        if len(bias_list) >= t + 1:
            _val_RaB, _feml_val_RaB, _male_val_RaB = calc_RaB_q(bias_list, t + 1)
            _vals.append(_val_RaB)
            _feml_vals.append(_feml_val_RaB)
            _male_vals.append(_male_val_RaB)

    bias_val = np.mean(_vals)
    bias_feml_val = np.mean(_feml_vals)
    bias_male_val = np.mean(_male_vals)

    return bias_val, bias_feml_val, bias_male_val


_test = [(0.0, 0.0, 0.0), (3, 3, 0.0), (0, 0, 0.0), (0, 0, 0.0), (0, 0, 0.0), (0, 0, 0.0), (0, 0.0, 0.0), (-5, 0.0, 5),
         (0, 0.0, 0.0), (-2, 0.0, 2)]

print('RaB_q', calc_RaB_q(_test, 10))
print('ARaB_q', calc_ARaB_q(_test, 10))

qry_bias_RaB = {}
qry_bias_ARaB = {}

print('calculating ranking bias')

for exp_name in experiments:
    print(exp_name)
    qry_bias_RaB[exp_name] = {}
    qry_bias_ARaB[exp_name] = {}

    for _method in docs_bias_paths:
        print(_method)

        qry_bias_RaB[exp_name][_method] = {}
        qry_bias_ARaB[exp_name][_method] = {}

        for at_rank in at_ranklist:
            print(at_rank)

            qry_bias_RaB[exp_name][_method][at_rank] = {}
            qry_bias_ARaB[exp_name][_method][at_rank] = {}

            for qry_id in runs_docs_bias[exp_name][_method]:
                qry_bias_RaB[exp_name][_method][at_rank][qry_id] = calc_RaB_q(runs_docs_bias[exp_name][_method][qry_id],
                                                                              at_rank)
                qry_bias_ARaB[exp_name][_method][at_rank][qry_id] = calc_ARaB_q(
                    runs_docs_bias[exp_name][_method][qry_id], at_rank)

        print()

print('done!')


for exp_name in experiments:
    for _method in docs_bias_paths:
        save_path = "data/%s_run_bias_%s" % (exp_name, _method)

        print (save_path)

        with open(save_path + '_RaB.pkl', 'wb') as fw:
            pickle.dump(qry_bias_RaB[exp_name][_method], fw)

        with open(save_path + '_ARaB.pkl', 'wb') as fw:
            pickle.dump(qry_bias_ARaB[exp_name][_method], fw)
