# SEB
Search Engine Blocker, filter out what you can search on your computer

## Installation
You must download mitmproxy, and setup the SSL certificate.
You can do that through the documentation [here](https://mitmproxy.org)
Then clone this repository, using `git clone` or by downloading [here](https://github.com/FaisalAbusharar/SEB/archive/refs/heads/main.zip)

## Arguments
You can specify in the `keywords.json` the settings you'd like and what keywords you want to be blocked.
You can disable or enable the logging of searches by changing `loggingSearches=false`.
Add more blocked keywords by adding to the `blockedkeywords` variable.

## How to run
Run the command:
`mitmproxy -s observe.py`
