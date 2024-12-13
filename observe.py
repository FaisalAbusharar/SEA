from mitmproxy import http
import json
import threading
import time
import requests

with open('config.json','r') as file:
    data = json.load(file)

blocked_keywords = data["blockedkeywords"]
shortcuts = data["shortcuts"]
shortcut_map = {key: value for item in shortcuts for key, value in item.items()} #?creates a dictionary that i can loop through, not really sure how it fully works



def auto_update_checker():
    while True:
        if data["autoUpdate"] == True:  # Check if autoUpdate is True
            try:
                reload()
            except Exception as e:
                print(f"Error during auto-update: {e}")
        time.sleep(60) 

# Start the background thread
threading.Thread(target=auto_update_checker, daemon=True).start()


def request(flow: http.HTTPFlow) -> None:
    if flow.request.method != "GET": return;
    update_config(flow)


    ##! LOG FUNCTION       
    if "google.com/search" in flow.request.pretty_url and data["logSearches"]==True:
        query = flow.request.query.get("q", None)
        if query:
            with open("./out/google_searches.log", "a") as log_file:
                log_file.write(f"{query}\n") #* Writes to the file, if logsearches is enabled.
            print(f"Logged Google Search: {query}")

    ##! BLOCK FUNCTION        
    for keyword in blocked_keywords:
        if keyword in flow.request.pretty_url or any(keyword in value for value in flow.request.query.values()): #% Checks if the blocked keyword is in the request, and if so block it
            flow.response = http.Response.make(
                    403,  # HTTP status code for Forbidden
                    f"Request blocked: Contains forbidden keyword '{keyword}'",
                    {"Content-Type": "text/plain"}
                )
            print(f"Blocked request to: {flow.request.pretty_url}")
            
            
    ##! SHORTCUT FUNCTION        
    for keyword in shortcut_map.items():
        try:
            if keyword[0] == flow.request.query.get("q", None): #% Checks if the shortcut keyword matches the search, and if so redirects
                flow.response = http.Response.make(
                    302,  #& HTTP status code for redirection
                    b"",
                    {"Location": keyword[1]}
            )
                break;
        except AttributeError: pass 
        except Exception as e: print(e)

        #* Shortcut Argument Function
        if str(keyword[0]) in flow.request.pretty_url or any(keyword[0] in value for value in flow.request.query.values()):
            if flow.request.query.get("q", None) is not None and ":" in flow.request.query.get("q", None):
                if flow.request.query.get("q", None).split(":", 1)[0].strip() == keyword[0]:
                    print(flow.request.query.get("q", None).split(":", 1)[0].strip())
                    result = flow.request.query.get("q", None).split(":", 1)[1].strip() #! Remove the keyword and the : to implement the search
                    flow.response = http.Response.make(
                        302,  #& HTTP status code for redirections
                        b"",
                        {"Location": keyword[1]+result}
                )
                    break;


    
def update_config(flow: http.HTTPFlow) -> None:
    ##* Update Function
    if "SEA [update]" in flow.request.pretty_url or any("SEA [update]" in value for value in flow.request.query.values()):
        reload(True, flow=flow)
        
def reload(flowNeeded=False, flow=None):
    try:
        with open('config.json',"r") as file: #! Reload the variables
                new_data = json.load(file) 
                global blocked_keywords, shortcut_map, shortcuts 
                blocked_keywords = new_data["blockedkeywords"] 
                shortcuts = new_data["shortcuts"]
                shortcut_map = {key: value for item in shortcuts for key, value in item.items()} 
                if flowNeeded == True:
                    flow.response = http.Response.make(
                        200, #Update the page to let the user know that we updated the page
                        b"Configuration updated successfully.",
                        {"Content-Type": "text/plain"}
                    )
                    print("Updated configuration")
    except Exception as e:
            pass