import json



def update_metric(event):
    with open("out/statistics.json", "r") as file:
        metric = json.load(file)
    metric[event] += 1
    with open("out/statistics.json", "w") as dumpfile:
        json.dump(metric, dumpfile)
    
