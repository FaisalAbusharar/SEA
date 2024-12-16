from mitmproxy import http
import json
import threading
import time
from functions.logger import logging_function
from functions.blocking import block_function
from functions.config_handler import reload, update_config
from functions.handle_shortcut import shortcut_function
from backend.generateNewConfig import generateConfig
from backend.logStatistics import update_metric



"""LOAD VARIABLES"""

def load_config(file_path='config.json', required_keys=None):
    """Loads and validates the configuration file.""" 
    required_keys = required_keys or {"blockedkeywords", "shortcuts", "logSearches", "autoUpdate"} #!Update this regularly 
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
    except FileNotFoundError:
        print("The path to your config.json is incorrect or the file is missing.") 
        if input("Would you like to automatically generate one? (y/n): ").strip().lower() == "y": #% Reduces user error
            generateConfig(file_path)
            return load_config(file_path, required_keys)
        else:
            raise FileNotFoundError("Configuration file is missing.")
    except json.JSONDecodeError:
        raise ValueError("Configuration file contains invalid JSON.")
    
    #& Validate structure
    if not all(key in config_data for key in required_keys):
        raise ValueError(f"Configuration file is missing required keys: {required_keys}")
    
    return config_data



#! Load configuration and initialize constants, do not change.
data = load_config()
blocked_keywords = data["blockedkeywords"]
shortcuts = data["shortcuts"]
shortcut_map = {key: value for item in shortcuts for key, value in item.items()}



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

#! Run the main program
def request(flow: http.HTTPFlow) -> None:
    if flow.request.method != "GET": return;
    
    #! Update configuration if needed
    if update_config(flow, data=data) == True:
        update_metric("config_update")
        

    #% Log Google searchesg
    if logging_function(flow, data["logSearches"]) == True:
        update_metric("logged_searches")
        
        

    #& Block requests with forbidden keywords
    if block_function(flow, blocked_keywords) == True:
        update_metric("blocked_keyword")
        return  #! Stop processing if blocked

    #* Handle shortcuts
    if shortcut_function(flow, shortcut_map=shortcut_map) == True:
        update_metric("shortcuts_triggerd")
        return 

  
            
            
    

    
