import json
import os
import asyncio
import dotenv
import traceback
from fastapi import Depends, FastAPI, HTTPException
from pyrogram import Client

from contextlib import asynccontextmanager

from pyrogram.errors import InviteHashExpired, InviteHashInvalid, PeerIdInvalid, UsernameInvalid


dotenv.load_dotenv()

clients, clients_lock = [], asyncio.Lock()
client_counter = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    global clients

    if not os.path.exists("clients.json"):
        with open("clients.json", "w", encoding="utf-8") as f:
            f.write("[]")
    
    try:
        with open('clients.json', encoding="utf-8") as f:
            cs = json.load(f)

            for c in cs:
                clients.append(Client(
                    c["name"],
                    api_id=c['api_id'],
                    api_hash=c['api_hash'],
                    session_string=c["session_string"],
                    in_memory=True,  # Prevent creating .session files
                ))
    except (json.JSONDecodeError, ValueError):
        print("Warning: clients.json is empty or invalid.")

    if not clients:
        print("Warning: No clients loaded! /check endpoint will fail.")

    for c in clients:
        try:
            await c.start()
        except Exception as e:
            print(f"Failed to start client {c.name}: {e}")

    yield

    for c in clients:
        try:
            await c.stop()
        except Exception:
            pass


app = FastAPI(lifespan=lifespan)


class LinkService:
    def __init__(self, bot: Client):
        self.bot = bot
        

    async def check_link(self, link: str):
        
        try:
            chat = await self.bot.get_chat(link)
            return {"detail": str(chat)}
        except (InviteHashExpired, InviteHashInvalid):
            return {"detail": "Expired or Invalid"}
        except (PeerIdInvalid, UsernameInvalid):
            return {"detail": "Invalid Link"}
        except Exception:
            return {"detail": f"Exception {traceback.format_exc()}"}


async def get_bot() -> Client:
    global client_counter
    
    if not clients:
        raise HTTPException(status_code=503, detail="No Telegram clients available")
        
    async with clients_lock:
        c = clients[client_counter % len(clients)]
        client_counter += 1

        return c


async def get_link_service() -> LinkService:
    bot = await get_bot()

    return LinkService(bot)


@app.get("/check")
async def check_link(link: str, link_service: LinkService = Depends(get_link_service)):
    return await link_service.check_link(link)
