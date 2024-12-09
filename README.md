# SEA
Search Engine Add-on, filter out what you can search on your computer, and add shortcuts!

## Installation
You must download mitmproxy, and setup the SSL certificate.
You can do that through the documentation [here](https://mitmproxy.org)
Then clone this repository, using `git clone` or by downloading [here](https://github.com/FaisalAbusharar/SEB/archive/refs/heads/main.zip)

## Arguments
You can specify in the `config.json` the settings you'd like and what keywords you want to be blocked, and what shortcuts to add.
You can disable or enable the logging of searches by changing `loggingSearches=false`.
Add more blocked keywords by adding to the `blockedkeywords` variable.

You can add shortcuts, by adding them to the `shortcuts` list in the json file, you must provide the `key`, for example `yt` and the value (*redirect url*) like `youtube.com`.
You can look at the examples inside of the `config.json`.

## How to run
Run the command:
`mitmproxy -s observe.py`
