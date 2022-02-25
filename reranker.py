from pandas.io.parquet import read_parquet
from sentence_transformers import SentenceTransformer, util
import torch
from sentence_transformers import  LoggingHandler, SentenceTransformer, evaluation, util, models
import pandas as pd 
import os
from tqdm import tqdm
from sentence_transformers import CrossEncoder
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-checkpoint', type=str, required=True)
    parser.add_argument('-queries', type=str, default='', required=True)
    parser.add_argument('-run', type=str, default='', required=True)
    parser.add_argument('-res', type=str, default='', required=True)

    args = parser.parse_args()

    model_name = args.checkpoint
    model = CrossEncoder(model_name, max_length=512)

    data_folder = "/msmarco-data/"
    collection_filepath = os.path.join(data_folder, 'collection.tsv')
    corpus = {}
    with open(collection_filepath, 'r', encoding='utf8') as fIn:
        for line in fIn:
            pid, passage = line.strip().split("\t")
            corpus[pid] = passage


    queries_filepath = args.queries
    queries = {}
    with open(queries_filepath, 'r', encoding='utf8') as fIn:
        for line in fIn:
            qid, query = line.strip().split("\t")
            queries[qid] = query

    if '.tsv' in args.run:
        run_dev_small = pd.read_csv(args.run, sep = "\t", names = ['qid', 'pid', 'rank'])
    elif '.trec' in args.run:
        run_dev_small = pd.read_csv(args.run, sep = " ", names = ['qid', 'q0', 'pid', 'rank', 'score', 'ranker'])
        run_dev_small.drop(columns = ['q0', 'score', 'ranker'], inplace = True)

    grps = run_dev_small.groupby('qid')

    reranked_run = []
    scores = []
    for name, group in tqdm(grps):
        query = queries[str(name)].strip()
        list_of_docs = []
        for doc_id in group['pid'].values.tolist():
            passage = corpus[str(doc_id)].strip()
            list_of_docs.append((query,passage))
            reranked_run.append([name, doc_id])
        score = model.predict(list_of_docs).tolist()
        scores.extend(score)


    reranked_run = pd.DataFrame(reranked_run, columns = ['qid', 'pid'])
    reranked_run['score'] = scores
    reranked_run.head()
    reranked_run.sort_values(by = ['qid', 'score'], ascending = False, inplace = True)
    reranked_run.to_csv(args.res, sep = "\t", index=False, header= None)

if __name__ == "__main__":
    main()
