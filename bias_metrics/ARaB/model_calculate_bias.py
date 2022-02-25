import collections
import numpy as np
import pickle
import pandas as pd 

experiments = ['run_file_biased', 'run_file_unbiased'
               ]

metrics = ['ARaB']
methods = ['tf', 'bool']

qry_bias_paths = {}
for metric in metrics:
    qry_bias_paths[metric] = {}
    for exp_name in experiments:
        qry_bias_paths[metric][exp_name] = {}
        for _method in methods:
            qry_bias_paths[metric][exp_name][_method] = 'data/%s_run_bias_%s_%s.pkl' % (exp_name, _method, metric)


at_ranklist = [5, 10, 20, 30, 50, 100]

qry_bias_perqry = {}

for metric in metrics:
    qry_bias_perqry[metric] = {}
    for exp_name in experiments:
        qry_bias_perqry[metric][exp_name] = {}
        for _method in methods:
            _path = qry_bias_paths[metric][exp_name][_method]
            print (_path)
            with open(_path, 'rb') as fr:
                qry_bias_perqry[metric][exp_name][_method] = pickle.load(fr)

# path to one of the run files to fetch unique qids
df = pd.read_csv("../../trec_runs/215_neutral_queries/bert_base_uncased/ranked_list_original.trec", sep = " ", names = ['qid','q0', 'pid', 'rank', 'score', 'model'])
query_ids = pd.unique(df['qid']).tolist()

eval_results_bias = {}
eval_results_feml = {}
eval_results_male = {}

for metric in metrics:
    eval_results_bias[metric] = {}
    eval_results_feml[metric] = {}
    eval_results_male[metric] = {}
    for exp_name in experiments:
        eval_results_bias[metric][exp_name] = {}
        eval_results_feml[metric][exp_name] = {}
        eval_results_male[metric][exp_name] = {}
        for _method in methods:
            eval_results_bias[metric][exp_name][_method] = {}
            eval_results_feml[metric][exp_name][_method] = {}
            eval_results_male[metric][exp_name][_method] = {}
            for at_rank in at_ranklist:
                _bias_list = []
                _feml_list = []
                _male_list = []

                for qryid in query_ids:
                    _bias_list.append(qry_bias_perqry[metric][exp_name][_method][at_rank][qryid][0])
                    _feml_list.append(qry_bias_perqry[metric][exp_name][_method][at_rank][qryid][1])
                    _male_list.append(qry_bias_perqry[metric][exp_name][_method][at_rank][qryid][2])
                    
                eval_results_bias[metric][exp_name][_method][at_rank] = np.mean([(_male_x-_feml_x) for _male_x, _feml_x in zip(_male_list, _feml_list)])
                eval_results_feml[metric][exp_name][_method][at_rank] = np.mean(_feml_list)
                eval_results_male[metric][exp_name][_method][at_rank] = np.mean(_male_list)


result = []  
for metric in metrics:
    print (metric)  
    for at_rank in at_ranklist:
        tmp = []
        tmp.append(at_rank)
        for _method in methods:
            tmp.append(_method)
            for exp_name in experiments:
                print ("%25s\t%2d %5s\t%f\t%f\t%f" % (exp_name, at_rank, _method, eval_results_bias[metric][exp_name][_method][at_rank], eval_results_feml[metric][exp_name][_method][at_rank], eval_results_male[metric][exp_name][_method][at_rank]))
                tmp.append(eval_results_bias[metric][exp_name][_method][at_rank])
        result.append(tmp)
        print()
        print ("==========")











