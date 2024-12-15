import json
from mitmproxy import http

def update_config(flow: http.HTTPFlow, data):
    """Reload the configuration file."""
    if "SEA [update]" in flow.request.pretty_url or "SEA [update]" in flow.request.query.values():
        reload(flowNeeded=True, flow=flow, current_data=data)
    return True

def reload(flowNeeded=False, flow=None, current_data=None):
    try:
        with open('config.json',"r") as file: #! Reload the variables
                new_data = json.load(file) 
                current_data.update(new_data)
                if flowNeeded == True:
                    flow.response = http.Response.make(
                        200, #Update the page to let the user know that we updated the page
                        b"Configuration updated successfully.",
                        {"Content-Type": "text/plain"}
                    )
                    print("Updated configuration")
    except Exception as e:
            pass    
    return True
        