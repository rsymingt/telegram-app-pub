
from json import dumps, dump, load
import os
import argparse
from pysondb import db

if not os.path.exists("config.json"):
    exit("Error: missing config.json file")

config = {}
with open("config.json", "r") as f:
    config = load(f)
    
from telethon import TelegramClient, events, sync

# Remember to use your own values from my.telegram.org!
api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
client = TelegramClient('test', config["telegram"]["api_id"], config["telegram"]["api_hash"])

async def main(db):
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    async for chat in client.iter_dialogs():
        event = chat
        try:
            if chat.is_user:
                chat.name=chat.entity.phone 
            if chat.name and (chat.name).strip() in config["chats_to_monitor"]:
                sender = await chat.message.get_sender()
                username = sender.username if hasattr(sender, 'username') else None
                full_name = f"{sender.first_name if hasattr(sender, 'first_name') else None} {sender.last_name if hasattr(sender, 'last_name') else None}"
                db.add({
                            "username": username,
                            "full_name": full_name,
                            "chat": chat.name,
                            "message": event.message.message
                        })
        except Exception as e:
            print(e)
            pass

        # async for message in client.iter_messages(d.id):
        #     print(message.sender_id, ':', message.text)

    # You can send messages to yourself...
    # await client.send_message('Test', 'Hello, myself!')

    @client.on(events.NewMessage(pattern='.*'))
    async def handler(event):
        try:
            chat = await event.get_chat()
            chat = chat.to_dict()
            if 'title' not in chat:
                chat["title"] = chat["phone"]

            sender = await event.get_sender()

            username = sender.username if hasattr(sender, 'username') else None
            full_name = f"{sender.first_name if hasattr(sender, 'first_name') else None} {sender.last_name if hasattr(sender, 'last_name') else None}"
            if (chat["title"]).strip() in config["chats_to_monitor"]:
                db.add({
                            "username": username,
                            "full_name": full_name,
                            "chat": chat["title"],
                            "message": event.message.message
                        })
        except Exception as e:
            print(e)
            pass
       
    await client.run_until_disconnected()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output-file", required=True, help="json file to output messages to")
    
    args = vars(ap.parse_args())

    outputFile = args["output_file"]
    db = db.getDb(outputFile)
    
    with client:
        client.loop.run_until_complete(main(db))

