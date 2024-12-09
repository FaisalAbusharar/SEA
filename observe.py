from mitmproxy import http
import json


with open('config.json','r') as file:
    data = json.load(file)

blocked_keywords = data["blockedkeywords"]
shortcuts = data["shortcuts"]
shortcut_map = {key: value for item in shortcuts for key, value in item.items()} #?creates a dictionary that i can loop through, not really sure how it fully works

def request(flow: http.HTTPFlow) -> None:
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
        if keyword[0] == flow.request.query.get("q", None): #% Checks if the shortcut keyword matches the search, and if so redirects
            flow.response = http.Response.make(
                302,  # HTTP status code for redirection
                b"",
                {"Location": keyword[1]}
        )
            break;

        if str(keyword[0]) in flow.request.pretty_url or any(keyword[0] in value for value in flow.request.query.values()) and ":" in flow.request.query.get("q", None):
            result = flow.request.query.get("q", None).split(":", 1)[1] #! Remove the keyword and the : to implement the search
            flow.response = http.Response.make(
                302,  # HTTP status code for redirection
                b"",
                {"Location": keyword[1]+result}
        )
            break;
    
    
