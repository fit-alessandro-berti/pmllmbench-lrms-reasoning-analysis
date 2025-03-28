# Reasoning Dashboards

## Model Scores

| Model                         | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| Grok-3-beta-thinking-20250221 | **14459** |  45 |    1 |   0 | 1039 |   131 |   10 |
| QwenQwQ-32B                   | **12858** |  46 |    0 |   0 |  861 |   112 |   12 |
| exaone-deep7.8b-fp16          | **12381** |  44 |    2 |   0 |  851 |   109 |   11 |
| DeepSeek-R1-Dynamic-Quant     | **12372** |  43 |    3 |   0 |  922 |   168 |   34 |
| DeepSeek-R1-671B-HB           | **12303** |  45 |    1 |   0 |  830 |    97 |   15 |
| Perplexity-R1-1776            | **12095** |  45 |    1 |   0 |  779 |    75 |    1 |
| exaone-deep32b-fp16           | **11187** |  43 |    3 |   0 |  779 |   103 |   25 |
| exaone-deep2.4b-fp16          | **10481** |  40 |    3 |   3 |  806 |   139 |   27 |
| DeepSeek-R1-Distill-Qwen-14B  | **10433** |  42 |    4 |   0 |  697 |    97 |   12 |
| DeepSeek-R1-Distill-Llama-70B | **10153** |  40 |    5 |   1 |  717 |    57 |   13 |
| DeepSeek-R1-Distill-Qwen-32B  | **9970**  |  42 |    4 |   0 |  650 |    50 |   14 |
| DeepSeek-R1-Zero              | **9765**  |  46 |    0 |   0 |  523 |    45 |    1 |
| DeepSeek-R1-Distill-Llama-8B  | **7307**  |  33 |   10 |   3 |  726 |   153 |   75 |
| DeepSeek-R1-Distill-Qwen-7B   | **3811**  |  26 |   16 |   4 |  578 |   149 |  101 |
| DeepSeek-R1-Distill-Qwen-1.5B | **-5495** |   3 |    9 |  11 |  240 |    95 |  250 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   13.5 |   31.9 |    2.8 |    2.1 |   16.8 | 17.9 | 3.9 |    1.3 |    1.4 |    8.5 |
| QwenQwQ-32B                   |   16.4 |   29   |    2   |    2.6 |   20.9 | 15.8 | 2.9 |    2   |    1.1 |    7   |
| exaone-deep7.8b-fp16          |   14.8 |   33.2 |    3.6 |    2.9 |   19.4 | 14.4 | 5.3 |    0.8 |    0.9 |    4.7 |
| DeepSeek-R1-Dynamic-Quant     |   14   |   31.8 |    3   |    2.1 |   22   | 16.5 | 3.9 |    0.9 |    1   |    4.9 |
| DeepSeek-R1-671B-HB           |   13   |   32   |    2.2 |    4.5 |   16.9 | 19.2 | 2.1 |    1   |    1.1 |    8.2 |
| Perplexity-R1-1776            |   16.5 |   28.2 |    2.9 |    2.7 |   20.4 | 16.6 | 3.6 |    1.3 |    1.5 |    6.3 |
| exaone-deep32b-fp16           |   12.8 |   32.1 |    2.5 |    2.6 |   17.3 | 17.9 | 5.6 |    1.4 |    0.8 |    6.9 |
| exaone-deep2.4b-fp16          |   15.5 |   30.8 |    1.6 |    2.2 |   20.1 | 15.4 | 6.5 |    1.2 |    1.2 |    5.5 |
| DeepSeek-R1-Distill-Qwen-14B  |   18.6 |   30.5 |    2.6 |    1.6 |   19.7 | 15.9 | 3.3 |    0.7 |    0.7 |    6.2 |
| DeepSeek-R1-Distill-Llama-70B |   16.1 |   31.4 |    1.9 |    2.9 |   21.6 | 14.2 | 3.3 |    0.9 |    0.9 |    6.7 |
| DeepSeek-R1-Distill-Qwen-32B  |   15.5 |   34.2 |    3.5 |    2.4 |   17.8 | 14.8 | 4.5 |    0.6 |    0.4 |    6.3 |
| DeepSeek-R1-Zero              |   18.8 |   40.1 |    3.5 |    3   |   11.6 | 15.1 | 0.5 |    1.2 |    0.7 |    5.4 |
| DeepSeek-R1-Distill-Llama-8B  |   14.7 |   28.9 |    2   |    1.2 |   23.9 | 15   | 6   |    1.4 |    0.8 |    6.2 |
| DeepSeek-R1-Distill-Qwen-7B   |   15.8 |   27.1 |    2.5 |    0.6 |   21.1 | 18.7 | 5.6 |    1.1 |    1   |    6.5 |
| DeepSeek-R1-Distill-Qwen-1.5B |   15.4 |   32.1 |    0.7 |    1.5 |   22.6 | 10.9 | 8.7 |    0   |    0.9 |    7.2 |

Dictionary of activities:
* **P.R.** -> Pattern Recognition
* **D.R.** -> Deductive Reasoning
* **I.R.** -> Inductive Reasoning
* **A.R.** -> Abductive Reasoning
* **H.G.** -> Hypothesis Generation
* **V** -> Validation
* **B** -> Backtracking
* **E.R.** -> Ethical or Moral Reasoning
* **C.R.** -> Counterfactual Reasoning
* **H.R.** -> Heuristic Reasoning


## Percentage of Correctness per Reasoning Type

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |    B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|-----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   97.5 |   96.3 |   90.9 |   68   |   72.2 | 94.3 | 76.1 |  100   |   47.1 |   75   |
| QwenQwQ-32B                   |   91.4 |   97.9 |   95   |   92.3 |   73.8 | 89.1 | 69   |   95   |   54.5 |   78.3 |
| exaone-deep7.8b-fp16          |   93.8 |   96.9 |   85.7 |   82.1 |   74.5 | 95   | 74.5 |  100   |   66.7 |   56.5 |
| DeepSeek-R1-Dynamic-Quant     |   93   |   95   |   88.2 |   79.2 |   64   | 80.5 | 72.7 |   90   |    9.1 |   70.9 |
| DeepSeek-R1-671B-HB           |   95.9 |   97.3 |   85.7 |   90.5 |   69.8 | 95.6 | 70   |   88.9 |   40   |   70.1 |
| Perplexity-R1-1776            |   96.5 |   97.5 |   96   |   78.3 |   88.5 | 93   | 67.7 |   90.9 |   30.8 |   83.3 |
| exaone-deep32b-fp16           |   91.4 |   95.5 |   91.3 |   91.7 |   73.9 | 87.7 | 66.7 |   92.3 |   57.1 |   69.8 |
| exaone-deep2.4b-fp16          |   91.4 |   91.6 |  100   |   76.2 |   68.7 | 88.7 | 69.8 |  100   |   25   |   67.9 |
| DeepSeek-R1-Distill-Qwen-14B  |   96   |   93.5 |   95.2 |  100   |   70.4 | 88.3 | 77.8 |  100   |   66.7 |   68   |
| DeepSeek-R1-Distill-Llama-70B |   98.4 |   95.1 |  100   |   82.6 |   84.1 | 92   | 88.5 |  100   |   71.4 |   79.2 |
| DeepSeek-R1-Distill-Qwen-32B  |   96.4 |   95.9 |   96   |   82.4 |   87.4 | 96.2 | 50   |  100   |   66.7 |   80   |
| DeepSeek-R1-Zero              |   99.1 |   98.7 |  100   |   88.2 |   78.8 | 83.7 |  0   |  100   |   25   |   80.6 |
| DeepSeek-R1-Distill-Llama-8B  |   92.9 |   88.8 |  100   |   81.8 |   61   | 77.6 | 42.1 |  100   |   12.5 |   59.3 |
| DeepSeek-R1-Distill-Qwen-7B   |   84.7 |   79   |   61.9 |  100   |   56   | 67.7 | 45.7 |  100   |   25   |   68.5 |
| DeepSeek-R1-Distill-Qwen-1.5B |   73.3 |   43.6 |   50   |   33.3 |   14.4 | 46.9 | 35.3 |    0   |   20   |   45.2 |
