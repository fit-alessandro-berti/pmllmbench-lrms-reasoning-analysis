import os
import json
from pm4py.objects.ocel.obj import OCEL
from datetime import datetime
import pandas as pd
import pm4py

folder = "prel/final_abstract_steps"

results = [x for x in os.listdir(folder) if x.endswith(".json")]

timer = 100000

events = []
objects = []
relations = []

obj_ids = set()

for file in results:
    res = json.load(open(os.path.join(folder, file), "r", encoding="utf-8"))

    model = "MOD_" + file.split("_cat")[0]
    question = "QUE_" + file.split("_cat")[1].split(".")[0]
    model_question = "MODQUE_" + file

    print(model, question, model_question)

    if model not in obj_ids:
        obj_ids.add(model)
        objects.append({'ocel:oid': model, 'ocel:type': 'MOD'})

    if question not in obj_ids:
        obj_ids.add(question)
        objects.append({"ocel:oid": question, "ocel:type": "QUE"})

    if model_question not in obj_ids:
        obj_ids.add(model_question)
        objects.append({"ocel:oid": model_question, "ocel:type": "MODQUE"})

    for el in res:
        timer += 1

        evid = "EV_" + str(timer).zfill(8)
        ocel_timestamp = datetime.fromtimestamp(timer)
        event = {"ocel:eid": evid, "ocel:activity": el["Name"], "ocel:timestamp": ocel_timestamp}
        if "Text" in el:
            event["text"] = el["Text"]
            pass
        events.append(event)

        ev1 = {"ocel:eid": evid, "ocel:activity": el["Name"], "ocel:timestamp": ocel_timestamp, "ocel:oid": model, "ocel:type": "MOD"}
        ev2 = {"ocel:eid": evid, "ocel:activity": el["Name"], "ocel:timestamp": ocel_timestamp, "ocel:oid": model, "ocel:type": "QUE"}
        ev3 = {"ocel:eid": evid, "ocel:activity": el["Name"], "ocel:timestamp": ocel_timestamp, "ocel:oid": model_question, "ocel:type": "MODQUE"}

        relations.append(ev1)
        relations.append(ev2)
        relations.append(ev3)

events = pd.DataFrame(events)
objects = pd.DataFrame(objects)
relations = pd.DataFrame(relations)

ocel = OCEL(events=events, objects=objects, relations=relations)
print(ocel)

pm4py.write_ocel2(ocel, "prova.jsonocel")
