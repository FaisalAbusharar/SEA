import mitmproxy


"""Block Function"""
def block_function(flow: mitmproxy.http.HTTPFlow, blocked_keywords):
    for keyword in blocked_keywords:
        if keyword in flow.request.pretty_url or any(keyword in value for value in flow.request.query.values()): #% Checks if the blocked keyword is in the request, and if so block it
            flow.response = mitmproxy.http.Response.make(
                    403,  # HTTP status code for Forbidden
                    f"Request blocked: Contains forbidden keyword '{keyword}'",
                    {"Content-Type": "text/plain"}
                )
            print(f"Blocked request to: {flow.request.pretty_url}")
    return True