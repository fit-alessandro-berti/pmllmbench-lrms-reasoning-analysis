# Reasoning Dashboards

## Model Scores

| Model                         | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| Grok-3-beta-thinking-20250221 | **13770** |  44 |    1 |   0 |  979 |   120 |   10 |
| DeepSeek-R1-671B-HB           | **12303** |  45 |    1 |   0 |  830 |    97 |   15 |
| DeepSeek-R1-Zero              | **140**   |   1 |    0 |   0 |    4 |     0 |    0 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   14.1 |   32.2 |    3   |    2.2 |   16.3 | 17.1 | 4.1 |    1.4 |    1.4 |    8.3 |
| DeepSeek-R1-671B-HB           |   13   |   32   |    2.2 |    4.5 |   16.9 | 19.2 | 2.1 |    1   |    1.1 |    8.2 |
| DeepSeek-R1-Zero              |   25   |   25   |    0   |    0   |   25   |  0   | 0   |    0   |    0   |   25   |

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
| Grok-3-beta-thinking-20250221 |   97.4 |   96.1 |   90.9 |   66.7 |   71.3 | 94.2 | 75.6 |  100   |     50 |   79.3 |
| DeepSeek-R1-671B-HB           |   95.9 |   97.3 |   85.7 |   90.5 |   69.8 | 95.6 | 70   |   88.9 |     40 |   70.1 |
| DeepSeek-R1-Zero              |  100   |  100   |    0   |    0   |  100   |  0   |  0   |    0   |      0 |  100   |
