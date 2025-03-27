# Reasoning Dashboards

## Model Scores

| Model                         | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| Grok-3-beta-thinking-20250221 | **14459** |  45 |    1 |   0 | 1039 |   131 |   10 |
| DeepSeek-R1-671B-HB           | **12303** |  45 |    1 |   0 |  830 |    97 |   15 |
| DeepSeek-R1-Zero              | **2193**  |  11 |    0 |   0 |  110 |     7 |    0 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   13.5 |   31.9 |    2.8 |    2.1 |   16.8 | 17.9 | 3.9 |    1.3 |    1.4 |    8.5 |
| DeepSeek-R1-671B-HB           |   13   |   32   |    2.2 |    4.5 |   16.9 | 19.2 | 2.1 |    1   |    1.1 |    8.2 |
| DeepSeek-R1-Zero              |   24.8 |   44.4 |    2.6 |    8.5 |    6   |  9.4 | 0   |    0   |    0.9 |    3.4 |

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
| DeepSeek-R1-671B-HB           |   95.9 |   97.3 |   85.7 |   90.5 |   69.8 | 95.6 | 70   |   88.9 |   40   |   70.1 |
| DeepSeek-R1-Zero              |  100   |  100   |  100   |  100   |   71.4 | 72.7 |  0   |    0   |    0   |   75   |
