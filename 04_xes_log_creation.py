import os
import json
import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
from datetime import datetime
from file_utils import read_file_with_fallback

folder = "prel/final_abstract_steps"

results = [x for x in os.listdir(folder) if x.endswith(".json")]

log = EventLog()

timer = 100000

for file in results:
    res = json.loads(read_file_with_fallback(os.path.join(folder, file)))

    trace = Trace()
    trace.attributes["model"] = file.split("_cat")[0]
    trace.attributes["question"] = file.split("_cat")[1].split(".")[0]
    trace.attributes["concept:name"] = file

    log.append(trace)

    for el in res:
        event = Event()
        event["concept:name"] = el["Name"]
        if "Text" in el:
            event["text"] = el["Text"]
            pass
        event["time:timestamp"] = datetime.fromtimestamp(timer)
        timer += 1

        trace.append(event)

pm4py.write_xes(log, "xes/output_"+datetime.now().strftime("%Y%m%d")+".xes.gz")
