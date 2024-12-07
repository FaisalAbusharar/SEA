from mitmproxy import http
import json

with open('keywords.json','r') as file:
    data = json.load(file)

blocked_keywords = data["blockedkeywords"]

def request(flow: http.HTTPFlow) -> None:
    if "google.com/search" in flow.request.pretty_url and data["logSearches"]==True:
        query = flow.request.query.get("q", None)
        if query:
            with open("./out/google_searches.log", "a") as log_file:
                log_file.write(f"{query}\n")
            print(f"Logged Google Search: {query}")

    for keyword in blocked_keywords:
        if keyword in flow.request.pretty_url or any(keyword in value for value in flow.request.query.values()):
            flow.response = http.Response.make(
                    403,  # HTTP status code for Forbidden
                    f"Request blocked: Contains forbidden keyword '{keyword}'",
                    {"Content-Type": "text/plain"}
                )
            print(f"Blocked request to: {flow.request.pretty_url}")
    
