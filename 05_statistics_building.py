import os
import json
import pandas as pd


folder = "prel/final_abstract_steps"

results = [x for x in os.listdir(folder) if x.endswith(".json")]

timer = 100000

models = {}

"""
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
"""
activities = ["Pattern Recognition", "Deductive Reasoning", "Inductive Reasoning", "Abductive Reasoning",
              "Hypothesis Generation", "Validation", "Backtracking", "Ethical or Moral Reasoning",
              "Counterfactual Reasoning", "Heuristic Reasoning"]

for file in results:
    res = json.load(open(os.path.join(folder, file), "r", encoding="utf-8"))

    model = file.split("_cat")[0]
    if model not in models:
        models[model] = {
            "conclusion_correct": 0,
            "conclusion_partially_correct": 0,
            "conclusion_incorrect": 0,
            "step_positive_effect": 0,
            "step_indifferent": 0,
            "step_negative_effect": 0,
            "activities": {

            }
        }

        for act in activities:
            models[model]["activities"][act] = {"step_positive_effect": 0, "step_indifferent": 0,
                                                "step_negative_effect": 0}

    if res[-1]["Name"].endswith(" - C"):
        models[model]["conclusion_correct"] += 1

    if res[-1]["Name"].endswith(" - PC"):
        models[model]["conclusion_partially_correct"] += 1

    if res[-1]["Name"].endswith(" - W"):
        models[model]["conclusion_incorrect"] += 1

    i = 0
    while i < len(res) - 1:
        name = res[i]["Name"].split(" - ")

        if name[1] == "PE":
            models[model]["step_positive_effect"] += 1
            models[model]["activities"][name[0]]["step_positive_effect"] += 1
        elif name[1] == "NE":
            models[model]["step_negative_effect"] += 1
            models[model]["activities"][name[0]]["step_negative_effect"] += 1
        elif name[1] == "IND":
            models[model]["step_indifferent"] += 1
            models[model]["activities"][name[0]]["step_indifferent"] += 1

        i = i + 1

for mod in models:
    summ = 0
    for act in models[mod]["activities"]:
        models[mod]["activities"][act]["total"] = models[mod]["activities"][act]["step_positive_effect"] + models[mod]["activities"][act]["step_negative_effect"] + models[mod]["activities"][act]["step_indifferent"]
        summ += models[mod]["activities"][act]["total"]
        if models[mod]["activities"][act]["total"] > 0:
            models[mod]["activities"][act]["percentage_correct"] = round(float(models[mod]["activities"][act]["step_positive_effect"]) / float(models[mod]["activities"][act]["total"]) * 100.0, 1)
        else:
            models[mod]["activities"][act]["percentage_correct"] = 0.0

    for act in models[mod]["activities"]:
        models[mod]["activities"][act]["percentage_over_total"] = round(float(models[mod]["activities"][act]["total"]) / float(summ) * 100.0, 1)

    #del models[mod]["activities"]

    models[mod]["score"] = (100 * models[mod]["conclusion_correct"] - 100 * models[mod][
        "conclusion_partially_correct"] - 200 * models[mod]["conclusion_incorrect"]) + \
                           (10 * models[mod]["step_positive_effect"] - 1 * models[mod]["step_indifferent"] - 20 *
                            models[mod]["step_negative_effect"])

ordered_models = [(mod, models[mod]["score"]) for mod in models]
ordered_models.sort(key=lambda x: (x[1], x[0]), reverse=True)
ordered_models = [x[0] for x in ordered_models]

dataframe = [{"Model": mod, "Score": "**%d**" % (models[mod]["score"]), "C": models[mod]["conclusion_correct"], "PC": models[mod]["conclusion_partially_correct"], "W": models[mod]["conclusion_incorrect"], "PE": models[mod]["step_positive_effect"], "IND": models[mod]["step_indifferent"], "NE": models[mod]["step_negative_effect"]} for mod in ordered_models]
dataframe = pd.DataFrame(dataframe)


reasoning_score = dataframe.to_markdown(index=False)

F = open("reasoning_dashboards.md", "w")
F.write("# Reasoning Dashboards\n\n")
F.write("## Model Scores\n\n")
F.write(reasoning_score)
F.write("\n\nHere, **C**, **PC**, **W** refer to the number of correct, partially correct, and wrong conclusions. **PE**, **IND**, **NE** refer to the number of reasoning steps with positive, indifferent, and negative effect.\n\n")

F.close()
