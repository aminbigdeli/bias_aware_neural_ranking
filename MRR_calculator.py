import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-qrels', type=str, default='')
    parser.add_argument('-run', type=str, default='')
    parser.add_argument('-metric', type=str, default='mrr_cut_10')
    parser.add_argument('-result', type=str, default='')
    args = parser.parse_args()

    metric = args.metric
    k = int(metric.split('_')[-1])
    
    qrel = {}
    with open(args.qrels, 'r') as f_qrel:
        for line in f_qrel:
            qid, _, did, label = line.strip().split()
            if qid not in qrel:
                qrel[qid] = {}
            qrel[qid][did] = int(label)

    run = {}
    with open(args.run, 'r') as f_run:
        for line in f_run:
            qid, _, did, _, _, _ = line.strip().split()
            if qid not in run: 
                run[qid] = []
            run[qid].append(did)
    if (len(args.result) != 0):
        myfile = open(args.result, "w") 
    mrr = 0.0
    for qid in run:
        rr = 0.0
        for i, did in enumerate(run[qid][:k]):
            if qid in qrel and did in qrel[qid] and qrel[qid][did] > 0:
                rr = 1 / (i+1)
                break
        if (len(args.result) != 0):
            myfile.write(str(qid) + "\t" + str(rr) + "\n")
        mrr += rr
    mrr /= len(run)
    if (len(args.result) != 0):
        myfile.write(str("total") + "\t" + str(mrr) + "\t")
        myfile.close()
    print("MRR@10: ", mrr)


if __name__ == "__main__":
    main()
