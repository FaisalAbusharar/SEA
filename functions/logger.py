import mitmproxy



"""Log Function"""
def logging_function(flow: mitmproxy.http.HTTPFlow, data):
    if "google.com/search" in flow.request.pretty_url and data==True:
        query = flow.request.query.get("q", None)
        if query:
            with open("out\google_searches.log", "a") as logfile:
                logfile.write(f"{query}\n")
            print(f"Logged Google Search: {query}")
    return True