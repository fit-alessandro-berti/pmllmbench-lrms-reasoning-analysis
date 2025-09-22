# Reasoning Dashboards

## Model Scores

| Model                    | Score    |   C |   PC |   W |   PE |   IND |   NE |
|:-------------------------|:---------|----:|-----:|----:|-----:|------:|-----:|
| nousresearchhermes-4-70b | **6180** |  38 |    7 |   0 |  337 |    70 |   11 |
| exaone-deep2.4b-fp16     | **551**  |  13 |    7 |   4 |  132 |    49 |   26 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                    |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |    B |   E.R. |   C.R. |   H.R. |
|:-------------------------|-------:|-------:|-------:|-------:|-------:|-----:|-----:|-------:|-------:|-------:|
| nousresearchhermes-4-70b |   15.3 |   19.9 |   10   |    8.6 |   16.5 | 14.1 |  6.7 |    1.7 |    1   |    6.2 |
| exaone-deep2.4b-fp16     |   17.4 |   15   |   10.6 |    9.2 |   13.5 | 13   | 15.5 |    1.4 |    0.5 |    3.9 |

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

| Model                    |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |    B |   E.R. |   C.R. |   H.R. |
|:-------------------------|-------:|-------:|-------:|-------:|-------:|-----:|-----:|-------:|-------:|-------:|
| nousresearchhermes-4-70b |   92.2 |   94   |   81   |   72.2 |   81.2 | 84.7 | 32.1 |   71.4 |    100 |   61.5 |
| exaone-deep2.4b-fp16     |   83.3 |   83.9 |   81.8 |   63.2 |   39.3 | 74.1 | 21.9 |   66.7 |    100 |   62.5 |
