# A Light-weight Strategy for Restraining Gender Biases in Neural Rankers

This repository contains the code and resources for our proposed bias-aware negative sampling strategy. Our proposed strategy is capable of decreasing the level of gender bias in neural ranking models, while maintaining a comparable level of retrieval effectiveness,and does not require any changes to the architecture or loss function of SOTA neural rankers.
## Example of Bias in IR
Table 1 shows top 3 documents of the re-ranked list of documents that are ranked by the BERT model for two fairness-sensitive queries. We can observe that the third document of the first query and the second document of the second query have inclination towards male gender and represent supervisor and governor as male-oriented positions. However, these biased documents have lower position in the re-ranked list of our proposed fairness-aware version of the model. We note that these biased documents are not considered as the relevance judgment documents of these queries. Therefore, ranking these documents in a lower position would not impact on the performance of the model.
#### Table 1: Top 3 re-ranked documents by the original BERT model.
<table class="tg">
<thead>
  <tr>
    <th class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">Query: is a supervisor considered a manager?</span></th>
    <th class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">Query: How important is a governor?</span></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">So a manager or supervisor who has control or direction of the employment of an employee, or is directly or indirectly responsible for an employee's employment, is considered an employer and subject to the rights and obligations of an employer under the AEPA.</span><br><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent">Ranking Position in Ours: 1</span></td>
    <td class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">Understanding and Adjusting Your Governor. Generally [...]. With the engine at idle, move the governor lever with your finger to open the throttle and it should push the arm back toward idle if working properly. One way to do this test is with the governor spring removed.</span><br><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent">Ranking Position in Ours: 2</span></td>
  </tr>
  <tr>
    <td class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">A manager or supervisor of agricultural employees may also be considered an employer for the purposes of the AEPA.The AEPA defines  employer  to mean the employer of an agricultural employee , and  any other person who , acting on behalf of the employer , has control or direction of , or is directly or indirectly responsible for , the employment …</span><br><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent">Ranking Position in Ours: 2</span></td>
    <td class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">Governor is important because </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>he</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">is the chief executive of the state. </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"> <b>He</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">is the little president that implements the law in the state and oversee the operations of all local government units within <b>his</b> area. The Governor is like the president of the state. </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"> <b>He</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">makes decisions for </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>his</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">state and makes opinions to the ppl of the state where </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>he</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">is president of the state that </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>he</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">controls.... It's important to a specific state. Not important for Congress. a governor is like a presidnet of the state.</span><br><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>Ranking Position in Ours: 88</b></span></td>
  </tr>
  <tr>
    <td class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">It becomes clear that the core of the role and responsibility of a supervisor lies in overlooking the activities of others to the satisfaction of laid standards in an organization. The position of a supervisor in a company is considered to be at the lowest rung of management. A supervisor in any department has more or less the same work experience as the other members in </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>his</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">team, but </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>he</b> </span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">is considered to be the leader of the group. The word manager comes from the word management, and a manager is a person who manages </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>men</b></span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">. To manage is to control and to organize things, </span><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent"><b>men</b></span><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">, and events. Managers do just that. They ensure smooth running of the day to day functioning of a workplace, whether it is business, hospital, or a factory.</span><br><span style="font-weight:700;background-color:transparent"><b>Ranking Position in Ours: 22</b></span><br></td>
    <td class="tg-kwiq"><span style="font-weight:400;font-style:normal;text-decoration:none;background-color:transparent">The governor is the visible official who commands media attention. The governor, along with the lieutenant governor, is also a major legislative player. The governor sets forth a recommended legislative agenda, initiates the budget, and signs or vetoes legislative bills. The governor has several other important roles. These include the role of commander of both the Georgia State Patrol and the Georgia National Guard. Often overlooked is the role of intergovernmental middleman, a fulcrum of power and a center of political gravity.</span><br><span style="font-weight:700;font-style:normal;text-decoration:none;background-color:transparent">Ranking Position in Ours: 1</span></td>
  </tr>
</tbody>
</table>

## Retrieval Effectiveness
In order to investigate how our proposed negative sampling strategy affects retrieval effectiveness, we re-rank MS MARCO dev small dataset which is the common dataset for testing the performance of the model. As shown in Table 2, we can see that retrieval effectiveness remains statistically comparable to the base ranker and no statistically significant changes occur in terms of performance. 

#### Table 2: Comparison between the performance (MRR@10) of  the base ranker and the ranker trained based on our proposed negative sampling strategy on MS MARCO Dev Set.
<table class="tg">
<thead>
  <tr>
    <th class="tg-kwiq" rowspan="2">Neural Ranker</th>
    <th class="tg-kwiq" colspan="2">Training Schema</th>
    <th class="tg-0pky" rowspan="2">Change</th>
  </tr>
  <tr>
    <th class="tg-0pky">Original</th>
    <th class="tg-c3ow">Ours</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">BERT-base-uncased</td>
    <td class="tg-c3ow">0.3688</td>
    <td class="tg-c3ow">0.3583</td>
    <td class="tg-dvpl">-2.84%</td>
  </tr>
  <tr>
    <td class="tg-0pky">DistilRoBERTa-base</td>
    <td class="tg-c3ow">0.3598</td>
    <td class="tg-c3ow">0.3475</td>
    <td class="tg-dvpl">-3.42%</td>
  </tr>
  <tr>
    <td class="tg-0pky">ELECTRA-base</td>
    <td class="tg-c3ow">0.3332</td>
    <td class="tg-c3ow">0.3351</td>
    <td class="tg-dvpl">+0.57%</td>
  </tr>
</tbody>
</table>

## Bias Measurement 
We adopt two bias measurement metrics to calculate the level of biases within the retrieved list of documents: (1) The first metric measures the level of bias in a document based on the presence and frequency of gendered terms in a document, referred to as Boolean and TF ARaB metrics. (2) The Second metric is NFaiRR which calculates the level of fairness within the retrieved list of documents by calculating each document’s neutrality score. We note that less ARaB and higher NFaiRR metric values are desirable. In order to investigate the impact of our proposed negative sampling strategy on reducing gender biases, we re-rank the queries inside two sets of neutral queries (QS1 and QS2) that consists of 1765 and 215 queries, respectively. We report the retrieval effectiveness as well as the level of fairness and bias (NFaiRR, ARaB) at cut-off 10 for each of the query sets in Table 3.
#### Table 3: Retrieval effectiveness and the level of fairness and bias across three neural ranking models trained on query sets QS1 and QS2 at cut-off 10.
<table class="tg">
<thead>
  <tr>
    <th class="tg-0lax" rowspan="2">Query Set</th>
    <th class="tg-0lax" rowspan="2">Neural Ranker</th>
    <th class="tg-0lax" rowspan="2">Training<br>Schema</th>
    <th class="tg-baqh" rowspan="2">MRR@10</th>
    <th class="tg-8d8j" colspan="2">NFaiRR</th>
    <th class="tg-8d8j" colspan="4">ARaB</th>
  </tr>
  <tr>
    <th class="tg-8d8j">Value</th>
    <th class="tg-8d8j">Improvement</th>
    <th class="tg-8d8j">TF</th>
    <th class="tg-8d8j">Reduction</th>
    <th class="tg-8d8j">Boolean</th>
    <th class="tg-8d8j">Reduction</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax" rowspan="6"><a href="https://github.com/navid-rekabsaz/GenderBias_IR/blob/master/resources/queries_gender_annotated.csv" target="_top"> QS1</td>
    <td class="tg-0lax" rowspan="2">BERT<br>(base uncased)</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/1765_neutral_queries/bert_base_uncased/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.3494</td>
    <td class="tg-8d8j">0.7764</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.1281</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0956</td>
    <td class="tg-8d8j">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/1765_neutral_queries/bert_base_uncased/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.3266</td>
    <td class="tg-8d8j">0.8673</td>
    <td class="tg-8d8j">11.71%</td>
    <td class="tg-8d8j">0.0967</td>
    <td class="tg-8d8j">24.51%</td>
    <td class="tg-8d8j">0.0864</td>
    <td class="tg-8d8j">9.62%</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">DistilRoBERTa <br>(base)</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/1765_neutral_queries/distilroberta_base/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.3382</td>
    <td class="tg-8d8j">0.7805</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.1178</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0914</td>
    <td class="tg-8d8j">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/1765_neutral_queries/distilroberta_base/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.3152</td>
    <td class="tg-8d8j">0.8806</td>
    <td class="tg-8d8j">12.83%</td>
    <td class="tg-8d8j">0.0856</td>
    <td class="tg-8d8j">27.33%</td>
    <td class="tg-8d8j">0.0813</td>
    <td class="tg-8d8j">11.05%</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">ELECTRA<br>(base)</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/1765_neutral_queries/electra_base/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.3265</td>
    <td class="tg-8d8j">0.7808</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.1273</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0961</td>
    <td class="tg-8d8j">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/1765_neutral_queries/electra_base/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.3018</td>
    <td class="tg-8d8j">0.8767</td>
    <td class="tg-8d8j">12.28%</td>
    <td class="tg-8d8j">0.0949</td>
    <td class="tg-8d8j">25.45%</td>
    <td class="tg-8d8j">0.0855</td>
    <td class="tg-8d8j">11.03%</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="6"><a href="https://github.com/CPJKU/FairnessRetrievalResults/blob/main/dataset/msmarco_passage.dev.fair.tsv" target="_top"> QS2</td>
    <td class="tg-0lax" rowspan="2">BERT<br>(base uncased)</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_base_uncased/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.2229</td>
    <td class="tg-8d8j">0.8779</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0275</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0157</td>
    <td class="tg-8d8j">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_base_uncased/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.2265</td>
    <td class="tg-8d8j">0.9549</td>
    <td class="tg-8d8j">8.77%</td>
    <td class="tg-8d8j">0.0250</td>
    <td class="tg-8d8j">9.09%</td>
    <td class="tg-8d8j">0.0156</td>
    <td class="tg-8d8j">0.64%</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">DistilRoBERTa <br>(base)</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/distilroberta_base/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.2198</td>
    <td class="tg-8d8j">0.8799</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0338</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0262</td>
    <td class="tg-8d8j">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/distilroberta_base/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.2135</td>
    <td class="tg-8d8j">0.9581</td>
    <td class="tg-8d8j">8.89%</td>
    <td class="tg-8d8j">0.0221</td>
    <td class="tg-8d8j">34.62%</td>
    <td class="tg-8d8j">0.0190</td>
    <td class="tg-8d8j">27.48%</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">ELECTRA<br>(base)</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/electra_base/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.2296</td>
    <td class="tg-8d8j">0.8857</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0492</td>
    <td class="tg-8d8j">-</td>
    <td class="tg-8d8j">0.0353</td>
    <td class="tg-8d8j">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/electra_base/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-8d8j">0.2081</td>
    <td class="tg-8d8j">0.9572</td>
    <td class="tg-8d8j">8.07%</td>
    <td class="tg-8d8j">0.0279</td>
    <td class="tg-8d8j">43.29%</td>
    <td class="tg-8d8j">0.0254</td>
    <td class="tg-8d8j">28.05%</td>
  </tr>
</tbody>
</table>

## Comparative Analysis
We also compare our proposed strategy with ADVBERT which is the state-of-the-art model that leverages an adversarial training process in order to remove gender-related information. Since the authors shared their trained models based on BERT-Tiny and BERT-Mini and only for QS2, we compare our work with AdvBert in Table 4 based on these two shared models and on the QS2 query set in terms of retreival effectiveness, the level of fairness, and the level of bias.
#### Table 4: Comparing AdvBert training strategy and our approach at cut-off 10.
<table class="tg">
<thead>
  <tr>
    <th class="tg-0lax" rowspan="2">Neural Ranker</th>
    <th class="tg-0lax" rowspan="2">Training<br>Schema</th>
    <th class="tg-0lax" rowspan="2">MRR@10</th>
    <th class="tg-8d8j" colspan="2">NFaiRR</th>
    <th class="tg-8d8j" colspan="4">ARaB</th>
  </tr>
  <tr>
    <th class="tg-7zrl">Value</th>
    <th class="tg-7zrl">Improvement</th>
    <th class="tg-7zrl">TF</th>
    <th class="tg-7zrl">Reduction</th>
    <th class="tg-7zrl">Boolean</th>
    <th class="tg-7zrl">Reduction</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax" rowspan="3">BERT-Tiny</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_tiny/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-7zrl">0.1750</td>
    <td class="tg-7zrl">0.8688</td>
    <td class="tg-7zrl">-</td>
    <td class="tg-2b7s">0.0356</td>
    <td class="tg-7zrl">-</td>
    <td class="tg-2b7s">0.0296</td>
    <td class="tg-7zrl">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">ADVBERT <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_tiny/ranked_list_advbert_tiny.trec" target="_top"> (Run)</td>
    <td class="tg-7zrl">0.1361</td>
    <td class="tg-7zrl">0.9257</td>
    <td class="tg-7zrl">6.55%</td>
    <td class="tg-2b7s">0.0245</td>
    <td class="tg-7zrl">31.18%</td>
    <td class="tg-2b7s">0.0236</td>
    <td class="tg-7zrl">20.27%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_tiny/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-7zrl">0.1497</td>
    <td class="tg-7zrl">0.9752</td>
    <td class="tg-7zrl">12.25%</td>
    <td class="tg-2b7s">0.0099</td>
    <td class="tg-7zrl">72.19%</td>
    <td class="tg-2b7s">0.0115</td>
    <td class="tg-7zrl">61.15%</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="3">BERT-Mini</td>
    <td class="tg-7zrl">Original <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_mini/ranked_list_original.trec" target="_top"> (Run)</td>
    <td class="tg-7zrl">0.2053</td>
    <td class="tg-7zrl">0.8742</td>
    <td class="tg-7zrl">-</td>
    <td class="tg-2b7s">0.0300</td>
    <td class="tg-7zrl">-</td>
    <td class="tg-2b7s">0.0251</td>
    <td class="tg-7zrl">-</td>
  </tr>
  <tr>
    <td class="tg-7zrl">ADVBERT <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_mini/ranked_list_advbert_mini.trec" target="_top"> (Run)</td>
    <td class="tg-7zrl">0.1515</td>
    <td class="tg-7zrl">0.9410</td>
    <td class="tg-7zrl">7.64%</td>
    <td class="tg-2b7s">0.0081</td>
    <td class="tg-7zrl">73.00%</td>
    <td class="tg-2b7s">0.0032</td>
    <td class="tg-7zrl">87.26%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">Ours <br><a href="https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/trec_runs/215_neutral_queries/bert_mini/ranked_list_fairness_aware.trec" target="_top"> (Run)</td>
    <td class="tg-7zrl">0.2000</td>
    <td class="tg-7zrl">0.9683</td>
    <td class="tg-7zrl">10.76%</td>
    <td class="tg-2b7s">0.0145</td>
    <td class="tg-7zrl">51.67%</td>
    <td class="tg-2b7s">0.0113</td>
    <td class="tg-7zrl">54.98%</td>
  </tr>
</tbody>
</table>

## Resources
 We note that due to space limitation of github, we have uploaded trained neural ranking models, original training dataset, fairness-aware training dataset, and trec run files of MS MARCO dev small [here](https://drive.google.com/file/d/1h_az0o0UNX_-6yxIzmBRNGWTykbUY3Lj/view?usp=sharing).

## Usage
##### In order to train any other neural ranking model with our proposed negative sampling strategy you can follow the process below:
1. You need to first download the fairness-aware training dataset from [here](https://drive.google.com/file/d/1h_az0o0UNX_-6yxIzmBRNGWTykbUY3Lj/view?usp=sharing) which consists of 20 negative sample documents for each query. Among these 20 negative sample documents, 60% of the documents (equivalant to 12 documents) are the ones that had the highest level of bias among the top-1000 retreived documents for that query by  BM25.
2. Followed by that, using the cross-encoder architecture, that passes two sequence (query and candidate document) to the transformer model, you can train your desired model. In order to do so, you can use the cross encoder architecture of [Sentence Transformer Library](https://github.com/UKPLab/sentence-transformers/blob/master/examples/training/ms_marco/train_cross-encoder_scratch.py) and set the training parameters of the model as well as the training dataset which would be the fairness-aware training dataset.
3. Once your model is trained, you can rerank any list of documents for a given query using the `reranker.py` script that takes the trained model latest checkpoint and rerank the list as follows:
```
python reranker.py\
     -checkpoint path to the checkpoint of the latest model \
     -queries path to the queries .tsv file \
     -run path to the run .trec file \
     -res path to the result folder
```
4. In order to calculate the MRR of re-ranked run file of the model you can use the `MRR_calculator.py` script as follows:
```
python MRR_calculator.py \
 -qrels  path to the qrels file \
 -run path to the re-ranked run file obtained from the previous step \
 -result path to result
```
5. Finally, to calculate the level of bias using ARaB metric and NFaiRR metrics for the re-ranked run files you can use the provided scripts that are taken from Navid Rekabsaz repositories ([ARaB](https://github.com/navid-rekabsaz/GenderBias_IR) and [NFaiRR](https://github.com/CPJKU/FairnessRetrievalResults)) and just have some minor changes so as to be applied for our work. In order to caluclate ARaB you frist need to run [`documents_calculate_bias.py`](https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/bias_metrics/ARaB/documents_calculate_bias.py) script to calculate the level of bias within each document. Subsequently, you need to use [`runs_calculate_bias.py`](https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/bias_metrics/ARaB/runs_calculate_bias.py) and [`model_calculate_bias.py`](https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/bias_metrics/ARaB/model_calculate_bias.py) scripts for calculating the TF ARab and TF Boolean metrics. Finally, to calculate the level of Fairness for the re-reanked runs, you need to first run [`calc_documents_neutrality.py`](https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/bias_metrics/NFaiRR/calc_documents_neutrality.py) to calucalte the level of fairness within each document and then run [`metrics_fairness.py`](https://github.com/aminbigdeli/bias_aware_neural_ranking/blob/main/bias_metrics/NFaiRR/metrics_fairness.py) to calculate NFaiRR metric over the run file.
