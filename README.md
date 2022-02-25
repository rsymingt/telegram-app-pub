# Telegram Chat Streamer

This 

## Configuration
config.json must be configured with the following information
```
{
    "telegram": {
        "api_id": "<api_key>",
        "api_hash":"<api_hash>",
        "phone":"<phone_including_international_code>", 
        "database_encryption_key":"<password_for_local_store>"
    },
    "chats_to_monitor": [
        "chat1", "chat2", "chat3"
    ]
}
```

## Requirements
- python3
- telethon

## Install
`pip install -r requirements.txt`

## Usage
`python main.py -o output.json`

You will be prompted with a command line input
```
Enter code:
```
The code to enter is the code sent to the telegram phone number in the config.json file

CTRL+C to exit