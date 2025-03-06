# Reasoning Dashboards

## Model Scores

| Model                         | Score    |   C |   PC |   W |   PE |   IND |   NE |
|:------------------------------|:---------|----:|-----:|----:|-----:|------:|-----:|
| QwenQwQ-32B-Preview           | **7215** |  38 |    7 |   1 |  471 |    55 |   17 |
| DeepSeek-R1-Distill-Llama-8B  | **6334** |  34 |   12 |   0 |  455 |    76 |   17 |
| DeepSeek-R1-Distill-Llama-70B | **6239** |  35 |   11 |   0 |  427 |    71 |   18 |
| DeepSeek-R1-Distill-Qwen-14B  | **6231** |  36 |   10 |   0 |  416 |    69 |   23 |
| Grok-3-beta-thinking-20250221 | **5685** |  34 |   12 |   0 |  423 |   105 |   32 |
| DeepSeek-R1-Distill-Qwen-32B  | **5538** |  36 |   10 |   0 |  382 |    82 |   40 |
| DeepSeek-R1-Dynamic-Quant     | **5362** |  30 |   16 |   0 |  453 |    68 |   25 |
| DeepSeek-R1-671B-HB           | **5265** |  34 |   11 |   1 |  380 |    95 |   27 |
| DeepSeek-R1-Zero              | **4990** |  32 |   14 |   0 |  357 |    60 |   16 |
| Perplexity-R1-1776            | **4442** |  29 |   16 |   1 |  400 |    98 |   28 |
| DeepSeek-R1-Distill-Qwen-7B   | **4160** |  30 |   15 |   1 |  353 |    90 |   29 |
| QwenQwQ-32B                   | **3960** |  27 |   19 |   0 |  377 |   110 |   25 |
| DeepSeek-R1-Distill-Qwen-1.5B | **2957** |  25 |   18 |   3 |  350 |   103 |   27 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                         |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| QwenQwQ-32B-Preview           |   18.2 |   30.2 |   12.2 |    8.1 |    7.9 | 14.9 | 1.1 |    2   |    2.4 |    2.9 |
| DeepSeek-R1-Distill-Llama-8B  |   18.2 |   33.9 |    9.7 |    6.9 |    7.1 | 12.6 | 4.2 |    2.2 |    2.2 |    2.9 |
| DeepSeek-R1-Distill-Llama-70B |   17.8 |   32.2 |   12.6 |    8.5 |    6.6 | 11.6 | 2.7 |    2.1 |    1.6 |    4.3 |
| DeepSeek-R1-Distill-Qwen-14B  |   18.7 |   29.3 |    6.1 |    7.1 |   10.6 | 16.1 | 2.8 |    1.8 |    1.4 |    6.1 |
| Grok-3-beta-thinking-20250221 |   17.3 |   28.6 |   10.5 |    6.6 |    6.2 | 17.3 | 4.5 |    3   |    1.8 |    4.1 |
| DeepSeek-R1-Distill-Qwen-32B  |   18.5 |   28.6 |    8.9 |    7.1 |    9.7 | 16.5 | 2.6 |    1.4 |    3.2 |    3.6 |
| DeepSeek-R1-Dynamic-Quant     |   16.5 |   34.1 |   11   |    9.2 |    4.9 | 14.7 | 2.4 |    1.3 |    1.6 |    4.4 |
| DeepSeek-R1-671B-HB           |   16.9 |   30.5 |   10.4 |   10   |    6   | 16.1 | 2.4 |    1.6 |    2.2 |    4   |
| DeepSeek-R1-Zero              |   18.9 |   29.8 |   11.8 |    9.2 |    6.2 | 15.9 | 1.4 |    1.6 |    1.4 |    3.7 |
| Perplexity-R1-1776            |   18.4 |   31   |   11   |    8.9 |    6.5 | 14.8 | 2.5 |    1.3 |    2.1 |    3.4 |
| DeepSeek-R1-Distill-Qwen-7B   |   15.7 |   25.6 |    8.3 |    5.7 |   10.4 | 18.2 | 4.2 |    3   |    2.5 |    6.4 |
| QwenQwQ-32B                   |   17.4 |   26.4 |   10.2 |    8.8 |    7.6 | 16.8 | 3.7 |    1.8 |    2.9 |    4.5 |
| DeepSeek-R1-Distill-Qwen-1.5B |   20.6 |   25.8 |   14.6 |    8.5 |    5   | 13.8 | 3.1 |    1   |    2.3 |    5.2 |

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
| QwenQwQ-32B-Preview           |   96   |   91.5 |   90.9 |   65.9 |   83.7 | 87.7 | 50   |   72.7 |   46.2 |   81.2 |
| DeepSeek-R1-Distill-Llama-8B  |   94   |   90.9 |   86.8 |   65.8 |   53.8 | 88.4 | 56.5 |   75   |   50   |   68.8 |
| DeepSeek-R1-Distill-Llama-70B |   92.4 |   90.4 |   87.7 |   68.2 |   61.8 | 86.7 | 42.9 |   54.5 |   50   |   72.7 |
| DeepSeek-R1-Distill-Qwen-14B  |   94.7 |   88.6 |   90.3 |   55.6 |   50   | 85.4 | 85.7 |   77.8 |   71.4 |   80.6 |
| Grok-3-beta-thinking-20250221 |   84.5 |   83.8 |   83.1 |   54.1 |   48.6 | 78.4 | 44   |   64.7 |   60   |   73.9 |
| DeepSeek-R1-Distill-Qwen-32B  |   82.8 |   84.7 |   84.4 |   63.9 |   49   | 83.1 | 53.8 |   57.1 |   37.5 |   66.7 |
| DeepSeek-R1-Dynamic-Quant     |   92.2 |   90.3 |   75   |   76   |   63   | 86.2 | 46.2 |  100   |   22.2 |   75   |
| DeepSeek-R1-671B-HB           |   87.1 |   84.3 |   84.6 |   64   |   40   | 77.8 | 41.7 |   75   |   54.5 |   45   |
| DeepSeek-R1-Zero              |   91.5 |   90.7 |   80.4 |   72.5 |   55.6 | 79.7 | 83.3 |   85.7 |   50   |   68.8 |
| Perplexity-R1-1776            |   84.5 |   82.2 |   82.8 |   55.3 |   55.9 | 79.5 | 30.8 |   71.4 |   54.5 |   77.8 |
| DeepSeek-R1-Distill-Qwen-7B   |   90.5 |   83.5 |   69.2 |   66.7 |   53.1 | 83.7 | 50   |   42.9 |   33.3 |   73.3 |
| QwenQwQ-32B                   |   80.9 |   84.4 |   71.2 |   48.9 |   61.5 | 82.6 | 36.8 |   55.6 |   60   |   69.6 |
| DeepSeek-R1-Distill-Qwen-1.5B |   81.8 |   82.3 |   75.7 |   65.9 |   50   | 62.1 | 46.7 |   80   |   63.6 |   64   |
