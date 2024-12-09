import json
with open('config.json','r') as file:
    data = json.load(file)

blocked_keywords = data["blockedkeywords"]
shortcuts = data["shortcuts"]
shortcut_map = {key: value for item in shortcuts for key, value in item.items()} #?creates a dictionary that i can loop through, not really sure how it fully works


for keyword in shortcut_map.items():
    print(keyword[0])
    try:
        result = keyword[0].split(":", 1)[1]
        print(result)
    except:
        pass

