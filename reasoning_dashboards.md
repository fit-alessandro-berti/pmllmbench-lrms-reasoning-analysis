# Reasoning Dashboards

## Model Scores

| Model                         | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| Grok-3-beta-thinking-20250221 | **14459** |  45 |    1 |   0 | 1039 |   131 |   10 |
| QwenQwQ-32B                   | **12598** |  45 |    0 |   0 |  845 |   112 |   12 |
| DeepSeek-R1-671B-HB           | **12303** |  45 |    1 |   0 |  830 |    97 |   15 |
| Perplexity-R1-1776            | **12095** |  45 |    1 |   0 |  779 |    75 |    1 |
| DeepSeek-R1-Zero              | **9765**  |  46 |    0 |   0 |  523 |    45 |    1 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   13.5 |   31.9 |    2.8 |    2.1 |   16.8 | 17.9 | 3.9 |    1.3 |    1.4 |    8.5 |
| QwenQwQ-32B                   |   16.4 |   28.8 |    2.1 |    2.7 |   21.1 | 15.7 | 3   |    2.1 |    1.1 |    7.1 |
| DeepSeek-R1-671B-HB           |   13   |   32   |    2.2 |    4.5 |   16.9 | 19.2 | 2.1 |    1   |    1.1 |    8.2 |
| Perplexity-R1-1776            |   16.5 |   28.2 |    2.9 |    2.7 |   20.4 | 16.6 | 3.6 |    1.3 |    1.5 |    6.3 |
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
| QwenQwQ-32B                   |   91.2 |   97.8 |   95   |   92.3 |   73.5 | 88.8 | 69   |   95   |   54.5 |   78.3 |
| DeepSeek-R1-671B-HB           |   95.9 |   97.3 |   85.7 |   90.5 |   69.8 | 95.6 | 70   |   88.9 |   40   |   70.1 |
| Perplexity-R1-1776            |   96.5 |   97.5 |   96   |   78.3 |   88.5 | 93   | 67.7 |   90.9 |   30.8 |   83.3 |
| DeepSeek-R1-Zero              |   99.1 |   98.7 |  100   |   88.2 |   78.8 | 83.7 |  0   |  100   |   25   |   80.6 |
