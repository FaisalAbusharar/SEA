from mitmproxy import http
import json
import threading
import time
from functions.logger import logging_function
from functions.blocking import block_function
from functions.config_handler import reload, update_config
from functions.handle_shortcut import shortcut_function

with open('config.json','r') as file:
    data = json.load(file)

blocked_keywords = data["blockedkeywords"]
shortcuts = data["shortcuts"]
shortcut_map = {key: value for item in shortcuts for key, value in item.items()} #?creates a dictionary that i can loop through, not really sure how it fully works
                


#! AUTO UPDATE FUNCTION
def auto_update_checker():
    while True:
        if data["autoUpdate"] == True:  #% Check if autoUpdate is True
            try:
                reload(current_data=data)
            except Exception as e:
                print(f"Error during auto-update: {e}")
        time.sleep(60) 


#% Start the background thread
threading.Thread(target=auto_update_checker, daemon=True).start()



            
def request(flow: http.HTTPFlow) -> None:
    if flow.request.method != "GET": return;
    
    #! Update configuration if needed
    update_config(flow, data=data)

    #% Log Google searchesg
    logging_function(flow, data["logSearches"])

    #& Block requests with forbidden keywords
    if block_function(flow, blocked_keywords):
        return  #! Stop processing if blocked

    #* Handle shortcuts
    if shortcut_function(flow, shortcut_map=shortcut_map):
        return 

  
            
            
    

    
