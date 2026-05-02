# Reasoning Dashboards

## Model Scores

| Model                                   | Score     |   C |   PC |   W |   PE |   IND |   NE |
|:----------------------------------------|:----------|----:|-----:|----:|-----:|------:|-----:|
| deepseekdeepseek-v3.2-speciale-thinking | **19497** |  46 |    0 |   0 |  806 |    43 |    1 |
| moonshotaikimi-k2.6                     | **18565** |  45 |    1 |   0 |  770 |    55 |    4 |
| qwenqwen3.6-27b                         | **18427** |  45 |    1 |   0 |  749 |    43 |    1 |
| mistral-medium-3.5-thinkhigh            | **18339** |  42 |    4 |   0 |  904 |   121 |    4 |
| deepseekdeepseek-v4-flash               | **17638** |  46 |    0 |   0 |  618 |    42 |    0 |
| deepseekdeepseek-v4-pro                 | **17529** |  44 |    2 |   0 |  716 |    71 |    3 |
| qwenqwen3.6-plusfree                    | **17481** |  46 |    0 |   0 |  604 |    59 |    0 |
| qwenqwen3.6-35b-a3b                     | **16903** |  43 |    3 |   0 |  704 |    77 |    3 |
| z-aiglm-5.1                             | **16900** |  44 |    2 |   0 |  654 |    80 |    3 |
| minimaxminimax-m2.7                     | **16550** |  44 |    2 |   0 |  623 |    80 |    5 |
| qwenqwen3.6-flash                       | **16493** |  43 |    3 |   0 |  657 |    57 |    1 |
| xiaomimimo-v2.5-pro                     | **16184** |  43 |    3 |   0 |  632 |    76 |    3 |

Here, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.

**Score formula: (100*C -100*PC -200*W) + (10*PE -1*IND -20*NE)**

## Percentage per Reasoning Type over Total

| Model                                   |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |    V |   B |   E.R. |   C.R. |   H.R. |
|:----------------------------------------|-------:|-------:|-------:|-------:|-------:|-----:|----:|-------:|-------:|-------:|
| deepseekdeepseek-v3.2-speciale-thinking |   17.3 |   28.1 |    4   |   10.9 |   13.4 | 16.6 | 1.3 |    1.4 |    0.7 |    6.2 |
| moonshotaikimi-k2.6                     |   13.9 |   28.3 |    3.7 |    7.8 |   11.7 | 21.8 | 3.7 |    1.6 |    1.3 |    6   |
| qwenqwen3.6-27b                         |   14.8 |   25.3 |    2.8 |    6.4 |   13.6 | 21.6 | 7.7 |    0.8 |    0.8 |    6.3 |
| mistral-medium-3.5-thinkhigh            |   13.1 |   25.7 |    3.9 |    9.1 |   13.8 | 19.5 | 5.4 |    1.7 |    2.2 |    5.5 |
| deepseekdeepseek-v4-flash               |   16.4 |   31.8 |    7.3 |    9.1 |    9.1 | 13.9 | 0.6 |    1.1 |    1.5 |    9.2 |
| deepseekdeepseek-v4-pro                 |   16.3 |   29.6 |    2.5 |    8.1 |   17.5 | 15.3 | 1   |    0.8 |    2.7 |    6.2 |
| qwenqwen3.6-plusfree                    |   15.4 |   23.8 |    4.4 |    7.2 |    9.5 | 22.6 | 8.4 |    0.6 |    0.6 |    7.4 |
| qwenqwen3.6-35b-a3b                     |   13.4 |   27.4 |    2.3 |    8.7 |   11.2 | 18.9 | 8.7 |    1.1 |    1.4 |    6.9 |
| z-aiglm-5.1                             |   13.7 |   25.1 |    3.7 |    7.3 |   12.3 | 20.9 | 6.9 |    0.8 |    2.7 |    6.5 |
| minimaxminimax-m2.7                     |   14.4 |   37.4 |    3.5 |    7.3 |   12.6 | 13.1 | 1.3 |    1.1 |    0.6 |    8.6 |
| qwenqwen3.6-flash                       |   14.4 |   26   |    4.6 |    6.2 |    9.7 | 21.3 | 6.4 |    1.4 |    1.5 |    8.5 |
| xiaomimimo-v2.5-pro                     |   14.2 |   30   |    3.1 |    9.4 |   12.1 | 19.5 | 1.7 |    1   |    1   |    8   |

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

| Model                                   |   P.R. |   D.R. |   I.R. |   A.R. |   H.G. |     V |     B |   E.R. |   C.R. |   H.R. |
|:----------------------------------------|-------:|-------:|-------:|-------:|-------:|------:|------:|-------:|-------:|-------:|
| deepseekdeepseek-v3.2-speciale-thinking |  100   |   97.5 |   97.1 |   86   |   88.6 |  99.3 |  90.9 |  100   |   33.3 |   90.6 |
| moonshotaikimi-k2.6                     |  100   |  100   |   93.5 |   80   |   80.4 |  96.1 |  87.1 |  100   |   63.6 |   80   |
| qwenqwen3.6-27b                         |   95.7 |   98.5 |  100   |   86.3 |   91.7 |  97.7 |  95.1 |  100   |   83.3 |   76   |
| mistral-medium-3.5-thinkhigh            |   98.5 |   97.7 |   97.5 |   72.3 |   76.1 |  88.6 |  89.3 |  100   |   21.7 |   84.2 |
| deepseekdeepseek-v4-flash               |   97.2 |   99   |   95.8 |   83.3 |   78.3 | 100   | 100   |  100   |   40   |   90.2 |
| deepseekdeepseek-v4-pro                 |  100   |   99.6 |  100   |   75   |   84.1 |  89.3 |  75   |   83.3 |   52.4 |   81.6 |
| qwenqwen3.6-plusfree                    |   99   |   99.4 |   93.1 |   79.2 |   77.8 |  98.7 |  85.7 |  100   |   50   |   61.2 |
| qwenqwen3.6-35b-a3b                     |   99   |   99.1 |   94.4 |   79.4 |   61.4 |  93.9 |  95.6 |   88.9 |   72.7 |   77.8 |
| z-aiglm-5.1                             |   97   |   98.4 |   88.9 |   85.2 |   64.8 |  96.8 |  92.2 |   83.3 |   50   |   70.8 |
| minimaxminimax-m2.7                     |   98   |   96.6 |   92   |   73.1 |   75.3 |  90.3 |  77.8 |   87.5 |    0   |   67.2 |
| qwenqwen3.6-flash                       |   98.1 |   98.9 |   93.9 |   88.6 |   72.5 |  96.1 |  95.7 |   90   |   36.4 |   80.3 |
| xiaomimimo-v2.5-pro                     |   98   |   99.5 |   45.5 |   77.6 |   84.9 |  89.2 |  91.7 |   85.7 |   71.4 |   70.2 |
