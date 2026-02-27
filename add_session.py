import asyncio
import os
import json
from pyrogram import Client


def load_clients() -> list[dict]:
    if os.path.exists("clients.json"):
        try:
            with open("clients.json", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []


clients = load_clients()


def check_name(name):
    for c in clients:
        if c["name"] == name:
            print("Name already exists")
            return False
    return True


def save_client(name: str, api_id: int, api_hash: str, session_string: str):
    clients.append({
        "name": name,
        "api_id": api_id,
        "api_hash": api_hash,
        "session_string": session_string,
    })

    with open("clients.json", "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2)

name = input("Enter the name of the client: ")

if not check_name(name):
    exit(1)

api_id = int(input("Enter the api_id of the client: "))
api_hash = input("Enter the api_hash of the client: ")




async def main():
    async with Client(name, api_id=api_id, api_hash=api_hash, in_memory=True) as client:
        session_string = await client.export_session_string()
        c = await client.get_me()
    
    save_client(name, api_id, api_hash, session_string)
    print(f"Client '{name}' with user id {c.id} added successfully!")

if __name__ == '__main__':
    asyncio.run(main())