# Reasoning Dashboards

## Model Scores

| Model                         | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| Grok-3-beta-thinking-20250221 | **14459** |  45 |    1 |   0 | 1039 |   131 |   10 |
| QwenQwQ-32B                   | **12858** |  46 |    0 |   0 |  861 |   112 |   12 |
| exaone-deep7.8b-fp16          | **12381** |  44 |    2 |   0 |  851 |   109 |   11 |
| DeepSeek-R1-671B-HB           | **12303** |  45 |    1 |   0 |  830 |    97 |   15 |
| Perplexity-R1-1776            | **12095** |  45 |    1 |   0 |  779 |    75 |    1 |
| exaone-deep32b-fp16           | **11187** |  43 |    3 |   0 |  779 |   103 |   25 |
| DeepSeek-R1-Dynamic-Quant     | **10658** |  35 |    3 |   0 |  830 |   162 |   34 |
| exaone-deep2.4b-fp16          | **10481** |  40 |    3 |   3 |  806 |   139 |   27 |
| DeepSeek-R1-Zero              | **9765**  |  46 |    0 |   0 |  523 |    45 |    1 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   13.5 |   31.9 |    2.8 |    2.1 |   16.8 | 17.9 | 3.9 |    1.3 |    1.4 |    8.5 |
| QwenQwQ-32B                   |   16.4 |   29   |    2   |    2.6 |   20.9 | 15.8 | 2.9 |    2   |    1.1 |    7   |
| exaone-deep7.8b-fp16          |   14.8 |   33.2 |    3.6 |    2.9 |   19.4 | 14.4 | 5.3 |    0.8 |    0.9 |    4.7 |
| DeepSeek-R1-671B-HB           |   13   |   32   |    2.2 |    4.5 |   16.9 | 19.2 | 2.1 |    1   |    1.1 |    8.2 |
| Perplexity-R1-1776            |   16.5 |   28.2 |    2.9 |    2.7 |   20.4 | 16.6 | 3.6 |    1.3 |    1.5 |    6.3 |
| exaone-deep32b-fp16           |   12.8 |   32.1 |    2.5 |    2.6 |   17.3 | 17.9 | 5.6 |    1.4 |    0.8 |    6.9 |
| DeepSeek-R1-Dynamic-Quant     |   13.1 |   32.5 |    2.9 |    2   |   22.1 | 17.1 | 4.2 |    0   |    1   |    5.2 |
| exaone-deep2.4b-fp16          |   15.5 |   30.8 |    1.6 |    2.2 |   20.1 | 15.4 | 6.5 |    1.2 |    1.2 |    5.5 |
| DeepSeek-R1-Zero              |   18.8 |   40.1 |    3.5 |    3   |   11.6 | 15.1 | 0.5 |    1.2 |    0.7 |    5.4 |

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
| DeepSeek-R1-671B-HB           |   95.9 |   97.3 |   85.7 |   90.5 |   69.8 | 95.6 | 70   |   88.9 |   40   |   70.1 |
| Perplexity-R1-1776            |   96.5 |   97.5 |   96   |   78.3 |   88.5 | 93   | 67.7 |   90.9 |   30.8 |   83.3 |
| exaone-deep32b-fp16           |   91.4 |   95.5 |   91.3 |   91.7 |   73.9 | 87.7 | 66.7 |   92.3 |   57.1 |   69.8 |
| DeepSeek-R1-Dynamic-Quant     |   91.8 |   94.6 |   86.7 |   76.2 |   61.7 | 80   | 74.4 |    0   |    0   |   71.7 |
| exaone-deep2.4b-fp16          |   91.4 |   91.6 |  100   |   76.2 |   68.7 | 88.7 | 69.8 |  100   |   25   |   67.9 |
| DeepSeek-R1-Zero              |   99.1 |   98.7 |  100   |   88.2 |   78.8 | 83.7 |  0   |  100   |   25   |   80.6 |
