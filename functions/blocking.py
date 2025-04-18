import mitmproxy


"""Block Function"""
def block_function(flow: mitmproxy.http.HTTPFlow, blocked_keywords, strictMode):
    for keyword in blocked_keywords:
        

        def block():
            flow.response = mitmproxy.http.Response.make(
                    403,  # HTTP status code for Forbidden
                    f"Request blocked: Contains forbidden keyword '{keyword}'",
                    {"Content-Type": "text/plain"}
                )
            print(f"Blocked request to: {flow.request.pretty_url}")
            return True
        
        if keyword in flow.request.pretty_url or any(keyword in value for value in flow.request.query.values()) and strictMode == True: #% Checks if the blocked keyword is in the request, and if so block it
            block()
        elif keyword == flow.request.query.values() and strictMode == False:
            block()