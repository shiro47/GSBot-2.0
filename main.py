import discord
from fastapi import FastAPI
from routers import discord_exceptions, database_api
from routers import discord as dc
from fastapi.middleware.cors import CORSMiddleware
from discord.ext import commands
from discord import app_commands
from decouple import config
import asyncio
import uvicorn

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='>', intents=discord.Intents.all(), application_id=929089506316025907)

        self.initial_extansions = [
            #"cogs.Apex.leaderboard",
            #"cogs.Apex.embeds",
            #"cogs.Twitch.streamers_live_list",
            "cogs.adminPanel.webpage_access",
            "cogs.exception_handler",
        ]

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def setup_hook(self):
        for ext in self.initial_extansions:
            await self.load_extension(ext)
        await self.tree.sync()

bot = MyBot()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(dc.router)
discord_exceptions.include_app(app)

async def start_bot():
    await bot.start(config('TOKEN'))

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())
    await asyncio.sleep(4)  # Optional sleep for establishing a connection with Discord
    print(f"{bot.user} has connected to Discord!")
    app.include_router(database_api.router)

def get_bot():
    return bot


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")
