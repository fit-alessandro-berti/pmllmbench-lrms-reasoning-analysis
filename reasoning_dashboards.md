# Reasoning Dashboards

## Model Scores

| Model                         | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| Grok-3-beta-thinking-20250221 | **13770** |  44 |    1 |   0 |  979 |   120 |   10 |
| DeepSeek-R1-671B-HB           | **489**   |   2 |    0 |   0 |   29 |     1 |    0 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   14.1 |   32.2 |      3 |    2.2 |   16.3 | 17.1 | 4.1 |    1.4 |    1.4 |    8.3 |
| DeepSeek-R1-671B-HB           |   13.3 |   26.7 |      0 |    3.3 |   20   | 30   | 0   |    0   |    0   |    6.7 |

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

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |     V |    B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|------:|-----:|-------:|-------:|-------:|
| Grok-3-beta-thinking-20250221 |   97.4 |   96.1 |   90.9 |   66.7 |   71.3 |  94.2 | 75.6 |    100 |     50 |   79.3 |
| DeepSeek-R1-671B-HB           |  100   |  100   |    0   |  100   |   83.3 | 100   |  0   |      0 |      0 |  100   |
