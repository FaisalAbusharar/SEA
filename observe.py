from mitmproxy import http
import json
import threading
import time
from functions.logger import logging_function
from functions.blocking import block_function
from functions.handle_shortcut import shortcut_function
from backend.generateNewConfig import generateConfig
from backend.logStatistics import update_metric

"""LOAD VARIABLES"""
def load_config(file_path='config.json', required_keys=None):
    """Loads and validates the configuration file."""
    required_keys = required_keys or {"blockedkeywords", "shortcuts", "logSearches", "autoUpdate", "strictMode"}  # ! Update this regularly
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
    except FileNotFoundError:
        print("The path to your config.json is incorrect or the file is missing.")
        if input("Would you like to automatically generate one? (y/n): ").strip().lower() == "y":  # % Reduces user error
            generateConfig(file_path)
            return load_config(file_path, required_keys)
        else:
            raise FileNotFoundError("Configuration file is missing.")
    except json.JSONDecodeError:
        raise ValueError("Configuration file contains invalid JSON.")

    # & Validate structure
    if not all(key in config_data for key in required_keys):
        raise ValueError(f"Configuration file is missing required keys: {required_keys}")

    return config_data


class ConfigManager:
    _config = None

    @classmethod
    def load(cls, file_path='config.json', required_keys=None):
        cls._config = load_config(file_path, required_keys)

    @classmethod
    def get(cls):
        if cls._config is None:
            raise ValueError("Configuration has not been loaded.")
        return cls._config

    @classmethod
    def reload(cls, file_path='config.json', required_keys=None):
        cls.load(file_path, required_keys)


#* Initialize configuration on startup
ConfigManager.load()


def regenerate_constants():
    """Rebuild constants dependent on the configuration."""
    global blocked_keywords, shortcut_map, strict_mode
    data = ConfigManager.get()
    blocked_keywords = data["blockedkeywords"]
    shortcuts = data["shortcuts"]
    strict_mode = data["strictMode"]
    shortcut_map = {key: value for item in shortcuts for key, value in item.items()}
    update_metric("config_update")
    


# ! Load configuration and initialize constants, do not change.
regenerate_constants()


# ! AUTO UPDATE FUNCTION
def auto_update_checker():
    while True:
        try:
            data = ConfigManager.get()
            if data.get("autoUpdate", False):  # % Check if autoUpdate is True
                ConfigManager.reload()
                regenerate_constants()  # Rebuild constants after reloading
        except Exception as e:
            print(f"Error during auto-update: {e}")
        time.sleep(60)


# % Start the background thread
threading.Thread(target=auto_update_checker, daemon=True).start()


# ! Run the main program
def request(flow: http.HTTPFlow) -> None:
    if flow.request.method != "GET":
        return

    # ! Update configuration if needed
    print(flow.request.query.values())
    if "SEA [update]" in flow.request.pretty_url or "SEA [update]" in flow.request.query.values():
        ConfigManager.reload()
        regenerate_constants()
        flow.response = http.Response.make(
                        200, #Update the page to let the user know that we updated the page
                        b"Configuration updated successfully.",
                        {"Content-Type": "text/plain"}
                    )
        print("Updated configuration")
                    

    # % Log Google searches
    if logging_function(flow, ConfigManager.get()["logSearches"]) == True:
        update_metric("logged_searches")

    # & Block requests with forbidden keywords
    if block_function(flow, blocked_keywords, strict_mode) == True:
        update_metric("blocked_keyword")
        return  # ! Stop processing if blocked

    # * Handle shortcuts
    if shortcut_function(flow, shortcut_map=shortcut_map) == True:
        update_metric("shortcuts_triggered")
        return
