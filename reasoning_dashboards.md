# Reasoning Dashboards

## Model Scores

| Model                                            | Score    |   C |   PC |   W |   PE |   IND |   NE |
|:-------------------------------------------------|:---------|----:|-----:|----:|-----:|------:|-----:|
| Qwen3-235B-A22B-Thinking-2507                    | **7984** |  44 |    2 |   0 |  394 |    76 |    4 |
| Qwen3-30B-A3B-2507-Thinking                      | **7527** |  42 |    4 |   0 |  389 |    63 |    5 |
| nvidiallama-3.1-nemotron-ultra-253b-v1-thinkenab | **7052** |  41 |    5 |   0 |  359 |    58 |    4 |
| nousresearchhermes-4-70b                         | **6180** |  38 |    7 |   0 |  337 |    70 |   11 |
| DeepSeek-V3.1-Reasoner                           | **6170** |  42 |    4 |   0 |  250 |    50 |    4 |
| r1-1776                                          | **5721** |  35 |   11 |   0 |  363 |    89 |   11 |
| qwen38b                                          | **5073** |  32 |   13 |   1 |  386 |    87 |   20 |
| phi4-reasoningplus                               | **4384** |  26 |    6 |   0 |  263 |    66 |    9 |
| exaone-deep2.4b-fp16                             | **2678** |  28 |   14 |   4 |  284 |   102 |   33 |
| grok-code-fast-1                                 | **950**  |  16 |   29 |   1 |  259 |    80 |    3 |
| deepseekdeepseek-r1-distill-qwen-7b              | **622**  |  19 |   23 |   4 |  259 |    68 |   35 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                                            |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |    B |   E.R. |   C.R. |   H.R. |
|:-------------------------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|-----:|-------:|-------:|-------:|
| Qwen3-235B-A22B-Thinking-2507                    |   17.1 |   18.4 |   11   |    9.1 |   14.6 | 16.2 |  1.3 |    1.9 |    2.1 |    8.4 |
| Qwen3-30B-A3B-2507-Thinking                      |   14   |   17.5 |   12   |    8.5 |   15.8 | 15.5 |  4.4 |    2.6 |    1.3 |    8.3 |
| nvidiallama-3.1-nemotron-ultra-253b-v1-thinkenab |   14.3 |   19.7 |   12.8 |    7.1 |   20   | 12.4 |  3.8 |    2.9 |    1.2 |    5.9 |
| nousresearchhermes-4-70b                         |   15.3 |   19.9 |   10   |    8.6 |   16.5 | 14.1 |  6.7 |    1.7 |    1   |    6.2 |
| DeepSeek-V3.1-Reasoner                           |   19.7 |   18.1 |   11.8 |    6.9 |   13.5 |  9.2 |  3.9 |    2.3 |    1.3 |   13.2 |
| r1-1776                                          |   13.6 |   18.6 |   13.2 |    9.5 |   17.3 | 11.9 |  6.9 |    2.2 |    0.9 |    6   |
| qwen38b                                          |   14.8 |   20.7 |   12.8 |    7.9 |   15.4 | 12.2 |  7.3 |    3.2 |    1.4 |    4.3 |
| phi4-reasoningplus                               |   15.7 |   18.6 |   10.4 |    9.8 |   13.6 | 13.3 |  8.3 |    0.6 |    0.3 |    9.5 |
| exaone-deep2.4b-fp16                             |   16.2 |   15.8 |   10.3 |    8.1 |   16   | 13.6 | 11   |    2.9 |    1.2 |    5   |
| grok-code-fast-1                                 |   20.8 |   21.3 |   19.3 |   11.7 |   12.6 |  7.3 |  0.9 |    0.6 |    0   |    5.6 |
| deepseekdeepseek-r1-distill-qwen-7b              |   17.4 |   16.6 |   14.1 |   11   |   13.8 |  9.9 |  6.1 |    2.5 |    1.1 |    7.5 |

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

| Model                                            |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |    B |   E.R. |   C.R. |   H.R. |
|:-------------------------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|-----:|-------:|-------:|-------:|
| Qwen3-235B-A22B-Thinking-2507                    |   88.9 |   96.6 |   86.5 |   65.1 |   81.2 | 84.4 | 66.7 |   88.9 |   40   |   70   |
| Qwen3-30B-A3B-2507-Thinking                      |   85.9 |   98.8 |   85.5 |   82.1 |   81.9 | 85.9 | 70   |  100   |   66.7 |   68.4 |
| nvidiallama-3.1-nemotron-ultra-253b-v1-thinkenab |   88.3 |   92.8 |   88.9 |   66.7 |   85.7 | 94.2 | 50   |   91.7 |   40   |   76   |
| nousresearchhermes-4-70b                         |   92.2 |   94   |   81   |   72.2 |   81.2 | 84.7 | 32.1 |   71.4 |  100   |   61.5 |
| DeepSeek-V3.1-Reasoner                           |   88.3 |   89.1 |   83.3 |   71.4 |   80.5 | 92.9 | 66.7 |  100   |   25   |   70   |
| r1-1776                                          |   85.7 |   90.7 |   88.5 |   70.5 |   80   | 76.4 | 31.2 |   90   |   50   |   67.9 |
| qwen38b                                          |   83.6 |   91.2 |   87.3 |   71.8 |   82.9 | 85   | 25   |   62.5 |   42.9 |   61.9 |
| phi4-reasoningplus                               |   83   |   95.2 |   91.4 |   72.7 |   80.4 | 75.6 | 21.4 |   50   |  100   |   75   |
| exaone-deep2.4b-fp16                             |   77.9 |   84.8 |   79.1 |   70.6 |   61.2 | 78.9 | 26.1 |   75   |   40   |   38.1 |
| grok-code-fast-1                                 |   71.8 |   89   |   69.7 |   75   |   69.8 | 64   | 66.7 |  100   |    0   |   89.5 |
| deepseekdeepseek-r1-distill-qwen-7b              |   88.9 |   86.7 |   82.4 |   47.5 |   78   | 63.9 | 31.8 |  100   |   50   |   37   |
