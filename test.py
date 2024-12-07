import json
with open('config.json','r') as file:
    data = json.load(file)

blocked_keywords = data["blockedkeywords"]
shortcuts = data["shortcuts"]


print(shortcuts)