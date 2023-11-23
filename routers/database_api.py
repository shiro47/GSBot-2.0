from typing import List
from fastapi import Depends, APIRouter
from routers.discord import discord
from database.twitch_db import TwitchDB
from database.apex_db import ApexDB
import pydantic
from bson import ObjectId
from APIs.discord_api import DiscordAPI
from APIs.twitch_api import TwitchAPI

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter()

class apexPlayer(pydantic.BaseModel): 
    playerName: str 
    discordID: int
    platform: str


@router.get(
    "/streamers/{server_id}",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=list,
)
async def getStreamers(server_id: str):
    streamers = TwitchDB(server_id).get_all_streamers()
    twitch_api = TwitchAPI()
    streamers_with_info = []
    
    for streamer in streamers:
        try:
            streamer_data = twitch_api.get_user_info_by_name(streamer["streamer_name"])[0]
        
            streamer.update({"avatar": streamer_data["profile_image_url"]})
            streamer.update({"display_name": streamer_data["display_name"]})
            streamers_with_info.append(streamer)
        except IndexError:
            continue
    return streamers_with_info

@router.delete(
    "/streamers/{server_id}/{streamer_name}",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def removeStreamer(server_id: str, streamer_name: str):
    return TwitchDB(server_id).remove_streamer(streamer_name)

@router.put(
    "/streamers/{server_id}/add-streamers",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def addStreamer(server_id: str, streamers: List[str]):
    return TwitchDB(server_id).add_streamer(streamers)

@router.get(
    "/apex_db/{server_id}",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=list,
)
async def getPlayers(server_id: str):
    players = ApexDB(server_id).get_all_players()
    discord = DiscordAPI()
    for player in players:
            user_data = await discord.get_user_info_by_id(player["DiscordID"])
            player.update({"avatar": user_data["avatar"]})
            player.update({"display_name": user_data["global_name"]})
    return players

@router.delete(
    "/apex_db/{server_id}/{player_name}",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def removePlayer(server_id: str, player_name: str):
    return ApexDB(server_id).remove_player_by_name(player_name)

@router.put(
    "/apex_db/{server_id}/add-player",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def addStreamer(server_id: str, player: apexPlayer):
    return ApexDB(server_id).add_player(player.platform, player.playerName, player.discordID)
