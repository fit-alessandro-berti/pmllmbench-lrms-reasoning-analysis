# Reasoning Dashboards

## Model Scores

| Model                        | Score    |   C |   PC |   W |   PE |   IND |   NE |
|:-----------------------------|:---------|----:|-----:|----:|-----:|------:|-----:|
| DeepSeek-R1-Distill-Qwen-14B | **6231** |  36 |   10 |   0 |  416 |    69 |   23 |
| DeepSeek-R1-Distill-Qwen-32B | **5538** |  36 |   10 |   0 |  382 |    82 |   40 |
| DeepSeek-R1-Distill-Qwen-7B  | **4160** |  30 |   15 |   1 |  353 |    90 |   29 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.
**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                        |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:-----------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| DeepSeek-R1-Distill-Qwen-14B |   18.7 |   29.3 |    6.1 |    7.1 |   10.6 | 16.1 | 2.8 |    1.8 |    1.4 |    6.1 |
| DeepSeek-R1-Distill-Qwen-32B |   18.5 |   28.6 |    8.9 |    7.1 |    9.7 | 16.5 | 2.6 |    1.4 |    3.2 |    3.6 |
| DeepSeek-R1-Distill-Qwen-7B  |   15.7 |   25.6 |    8.3 |    5.7 |   10.4 | 18.2 | 4.2 |    3   |    2.5 |    6.4 |

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

| Model                        |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |    B |   E.R. |   C.R. |   H.R. |
|:-----------------------------|-------:|-------:|-------:|-------:|-------:|-----:|-----:|-------:|-------:|-------:|
| DeepSeek-R1-Distill-Qwen-14B |   94.7 |   88.6 |   90.3 |   55.6 |   50   | 85.4 | 85.7 |   77.8 |   71.4 |   80.6 |
| DeepSeek-R1-Distill-Qwen-32B |   82.8 |   84.7 |   84.4 |   63.9 |   49   | 83.1 | 53.8 |   57.1 |   37.5 |   66.7 |
| DeepSeek-R1-Distill-Qwen-7B  |   90.5 |   83.5 |   69.2 |   66.7 |   53.1 | 83.7 | 50   |   42.9 |   33.3 |   73.3 |
