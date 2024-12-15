import json

#! Update this structure on a regular basis
data = {
    "blockedkeywords": [
        "example"
    ],
    "logSearches": True,
    "autoUpdate": True,
    "logStatistics": True,
    "shortcuts": [
        {"example": "https://example.com"}
    ]
}


def generateConfig(file_path):
    """Generates a default configuration file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Default configuration file created at: {file_path}")
