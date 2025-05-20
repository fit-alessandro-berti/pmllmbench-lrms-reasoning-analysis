# pmllmbench-lrms-reasoning-analysis

This project provides a way to extract and analyze reasoning steps from textual answers (referred to as "reasoning traces") by creating a standardized JSON event log and, in addition, a **process mining event log in the XES format**. Each XES log entry corresponds to an individual reasoning activity, and each file is treated as a distinct "trace." This allows further process-mining analysis on how different activities unfold over time.

[**Pre-print** Configuring Large Reasoning Models using Process Mining: A Benchmark and a Case Study](https://www.alessandroberti.it/new_papers/2025_Berti_Configuring_LRMs.pdf) describing the benchmark available.

---

### 1. Naming of the Activities in the Event Log

Each reasoning step is stored as a JSON object with:
- **Name**: A combination of the reasoning type and its effect, in the form:
  
  ```
  <Reasoning Type> - <Effect>
  ```
  
  Where **Reasoning Type** is one of:
  - Pattern Recognition  
  - Deductive Reasoning  
  - Inductive Reasoning  
  - Abductive Reasoning  
  - Hypothesis Generation  
  - Validation  
  - Backtracking  
  - Ethical or Moral Reasoning  
  - Counterfactual Reasoning  
  - Heuristic Reasoning  

  and **Effect** is one of:
  - **PE** (positive effect on correctness)  
  - **IND** (neutral or indifferent effect)  
  - **NE** (negative effect on correctness)

- **Text**: The excerpt from the reasoning trace corresponding to that specific activity.

At the end of each sequence of steps, a special **Conclusion** entry is added:
- **Conclusion - C** (if the overall reasoning steps is correct)
- **Conclusion - PC** (if the overall reasoning steps is partially correct)
- **Conclusion - W** (if the overall reasoning steps is wrong)

This conclusion entry does not contain a text snippet; it only indicates the final correctness of the reasoning process.

---

### 2. Statistics Computed

After these event logs are produced and validated, the second script aggregates and analyzes various metrics:

1. **Conclusion Outcomes**  
   Counts how often the final conclusion of the reasoning process is:
   - **C** (correct)  
   - **PC** (partially correct)  
   - **W** (wrong)

2. **Effects of Reasoning Steps**  
   Counts the total number of steps marked as **PE**, **IND**, and **NE**.

3. **Reasoning Types Usage**  
   Tracks how frequently each of the ten reasoning types appears and calculates:
   - The **percentage** of each reasoning type over the total number of steps.
   - The **percentage of positive-effect steps** within each reasoning type.

4. **Overall Score**  
   A custom formula computes a score that weighs:
   - The count of correct, partially correct, and wrong conclusions
   - The distribution of positive, indifferent, and negative steps

5. **Result Dashboards**  
   The results are compiled into Markdown tables, which are output to a [reasoning_dashboards.md](./reasoning_dashboards.md) file.

---

### 3. Process Mining Log (XES)

In addition to the JSON logs, the reasoning steps are also exported into a **process mining event log in XES format**.  
- Each JSON file is converted into a "trace," labeled by the model and question.  
- Each reasoning activity is turned into an event in the trace, capturing both the name of the activity and its textual snippet (if present).  

This XES log enables further process-mining analyses, such as discovering typical reasoning paths, bottlenecks, or correlations among reasoning step types.

For statistics and dashboards, see: [reasoning_dashboards.md](./reasoning_dashboards.md).
