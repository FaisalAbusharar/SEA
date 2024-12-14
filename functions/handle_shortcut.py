import mitmproxy

"""Shortcut Function""" 
def shortcut_function(flow: mitmproxy.http.HTTPFlow, shortcut_map=None):      
    for keyword in shortcut_map.items():
        try:
            if keyword[0] == flow.request.query.get("q", None): #% Checks if the shortcut keyword matches the search, and if so redirects
                flow.response = mitmproxy.http.Response.make(
                    302,  #& HTTP status code for redirection
                    b"",
                    {"Location": keyword[1]}
            )
                return True;
        except Exception as e: print(f"Error occurred: {e}")

        #* Shortcut Argument Function
        if str(keyword[0]) in flow.request.pretty_url or any(keyword[0] in value for value in flow.request.query.values()):
            if flow.request.query.get("q", None) is not None and ":" in flow.request.query.get("q", None):
                if flow.request.query.get("q", None).split(":", 1)[0].strip() == keyword[0]:
                    print(flow.request.query.get("q", None).split(":", 1)[0].strip())
                    result = flow.request.query.get("q", None).split(":", 1)[1].strip() #! Remove the keyword and the : to implement the search
                    flow.response = mitmproxy.http.Response.make(
                        302,  #& HTTP status code for redirections
                        b"",
                        {"Location": keyword[1]+result}
                )
                    break;
        