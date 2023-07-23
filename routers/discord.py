from typing import List
from fastapi import Depends, APIRouter
from fastapi_discord import DiscordOAuthClient, Unauthorized, User
from fastapi_discord.models import GuildPreview
from database.whitelist_db import WhitelistDB

router = APIRouter()

discord = DiscordOAuthClient(
    "929089506316025907", "ewpzJnrHNc-ofQZisS0GEGplQoAyWk6c", "http://localhost:3000/login", ("identify", "guilds", "email")
)  # scopes

@router.on_event("startup")
async def on_startup():
    await discord.init()


@router.get("/login")
async def login():
    return {"url": discord.get_oauth_login_url()}


@router.get("/callback")
async def callback(code: str):
    token, refresh_token = await discord.get_access_token(code)
    return {"access_token": token, "refresh_token": refresh_token}


@router.get(
    "/authenticated",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def isAuthenticated(token: str = Depends(discord.get_token)):
    try:
        auth = await discord.isAuthenticated(token)
        return auth
    except Unauthorized:
        return False


@router.get("/user", dependencies=[Depends(discord.requires_authorization)], response_model=User)
async def get_user(user: User = Depends(discord.user)):
    user_data = {"id": user.id, "username": user.username}
    return user


@router.get(
    "/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
async def get_guilds(guilds: List = Depends(discord.guilds)):
    return guilds

@router.get("/servers", dependencies=[Depends(discord.requires_authorization)], response_model=List[GuildPreview])
async def get_servers(user: User = Depends(discord.user), guilds: List = Depends(discord.guilds)):
    user_servers = WhitelistDB().get_all_user_servers(userId=int(user.id))
    matching_guilds = []
    for guild in guilds:
        if int(guild.id) in user_servers:
            matching_guilds.append(guild)
    return matching_guilds