import discord 
import datetime
from APIs.apex_api import Apex_API
from APIs.twitch_api import TwitchAPI
from database.twitch_db import TwitchDB as twitch_database
from database.apex_db import ApexDB as apex_database
from tqdm import tqdm
import json
import typing
import functools
import asyncio

twitch_api = TwitchAPI()
apex_api = Apex_API()

def jprint(obj):        # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

def embed_help():
    embed= discord.Embed(title='Dostępne komendy ', timestamp= datetime.datetime.utcnow(), color=discord.Color.purple())
    embed.add_field(name="Zarejestrowanie do leaderboard'a", value='`/register {platforma(PC,PS4,X1)} {nick origin}`', inline=False)
    embed.add_field(name="Wyrejestrowanie", value='`/unregister`', inline=False)
    return embed

def embed_pred():
    values=apex_api.pred_threshold()
    embed = discord.Embed(title='BR Predator Threshold: '+str(values[0])+' RP\n`Total Masters and Preds:` '+str(values[1]), color=discord.Color.dark_red(),timestamp= datetime.datetime.utcnow())
    embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/apexpredator1.png")
    return embed

@to_thread
def creating_rank_dict(guild_id):
    players={}
    db = apex_database(server_id=guild_id)
    for player in db.get_all_players():
        playerID=player['DiscordID']
        platform1=player['platform']
        data = apex_api.get_rankScore(platform1,player['ID'])
        if data!=None: 
            players.update({playerID: data})                   
    return sorted(players.items(), key=lambda x: x[1][1], reverse=True)


async def create_leaderboard_embeds(guild_id, bot):
    ranks={
                'Apex Predator': discord.Color.dark_red(),
            'Master':discord.Color.purple(),
            'Diamond':discord.Color.dark_blue(),
            'Platinum':discord.Color.blue(),
            'Gold':discord.Color.from_rgb(199, 158, 12),
            'Silver':discord.Color.light_grey(),
            'Bronze':discord.Color.from_rgb(184, 115, 51),
            }
    players = await creating_rank_dict(guild_id)
    db = apex_database(server_id=guild_id)
    var=0
    embeds=[]
    for rank in ranks:        
            embed = discord.Embed(title=f"__**{rank}**__", timestamp= datetime.datetime.utcnow(), color=ranks[rank])
            if rank=='Apex Predator':
                embed.set_thumbnail(url="https://api.mozambiquehe.re/assets/ranks/apexpredator1.png")
            else:
                embed.set_thumbnail(url=f"https://api.mozambiquehe.re/assets/ranks/{rank.casefold()}.png")
            pos=1
            for y in players:
                if y[1][0]==rank:
                    player = y[0]
                    user = await bot.fetch_user(player)
                    player = db.get_player(player)["ID"]
                    RP=y[1][1]
                    if rank=='Apex Predator':
                        embed.add_field(name=str(pos)+f'**. {user.name}**', value=player+' | RP '+str(RP), inline=False)
                    else:
                        embed.add_field(name=str(pos)+f'**. {user.name}**', value='```'+player+' | '+f'{rank} {y[1][2]}'+'\n'+rank_progress_bar(RP,rank,y[1][2])+'```', inline=False)
                    pos+=1
            var+=1
            embeds.append(embed)
    return embeds

def embed_map_rotation():
    values=apex_api.map_rotation_data()
    embeds=[]
    for mode in values.values():
        embed = discord.Embed(title=f'Aktualna mapa to: `{mode[0]}`', timestamp= datetime.datetime.utcnow())
        embed.set_image(url=mode[5])
        embed.add_field(name='Pozostały czas: ', value=f'`{mode[1]}`',inline=False)
        embed.add_field(name='Następna mapa: ', value=f'`{mode[2]}`', inline=False)
        time = datetime.datetime.strptime(mode[3], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
        embed.add_field(name='Start: ', value=f'`{time.strftime("%H:%M:%S")}`')
        time = datetime.datetime.strptime(mode[4], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
        embed.add_field(name='Koniec: ', value=f'`{time.strftime("%H:%M:%S")}`')
        embeds.append(embed)
    return embeds



def rank_progress_bar(RP,rank, rank_division):
    if rank=='Master':
        pred_rp=apex_api.pred_threshold()[0]
        return tqdm.format_meter(RP-24000,pred_rp-24000,0,bar_format='{desc} RP  |{bar}|  {postfix} RP', ncols=40, prefix=f"{RP}", postfix=pred_rp )
    ranks = {
        'Diamond': list(range(20000, 24000, 1000)),
        'Platinum': list(range(16000, 20000, 1000)),
        'Gold': list(range(12000, 16000, 1000)),
        'Silver': list(range(8000, 12000, 1000)),
        'Bronze': list(range(4000, 8000, 1000))
    }
    rank_divisions={
        4:0,
        3:1,
        2:2,
        1:3,
        }
    total_rank_rp = ranks[rank][1]-ranks[rank][0]
    rank_number = rank_divisions.get(rank_division)
    return tqdm.format_meter(RP-ranks[rank][rank_number],total_rank_rp,0,bar_format='{desc} RP  |{bar}|  {postfix} RP', ncols=40, prefix=f"{RP}", postfix=ranks[rank][rank_number]+total_rank_rp)

@to_thread
def create_streamers_list(server_id):
    streamers={}
    db = twitch_database(server_id=server_id)
    for x in db.get_all_existing_streamers():
            for streamer in x.items():
                if streamer[0]=='streamer_name':
                    status=twitch_api.check_stream_status(streamer[1])
                    if status!=False:
                        streamers.update({streamer[1]: [status[1],status[2], status[3]]})
                    else:
                        continue
    return streamers

def embed_all_streamers(server_id):
    embed = discord.Embed(title="Registered streamers in database:" ,color=discord.Color.dark_purple(),timestamp= datetime.datetime.utcnow())
    text="```"
    pos=1
    db = twitch_database(server_id=server_id)
    for streamer in db.get_all_streamers():
        text+=f"{str(pos)}. {streamer['streamer_name']}\n"
        pos+=1
    text+="```"
    embed.add_field(name="\u200b", value=text)
    return embed

async def create_streamers_live_embeds(guild_id):
    streamers = await create_streamers_list(server_id=guild_id)
    categories = {streamers[streamer][1]: streamers[streamer][2] for streamer in streamers}
    embeds = []
    for category in categories:
        embed = discord.Embed(title=f"__**{category}**__", timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=f'{categories[category]}')
        streamers_in_category = {streamer: streamers[streamer][0] for streamer in streamers if streamers[streamer][1] == category}
        streamers_in_category = sorted(streamers_in_category.items(), key=lambda x: x[1], reverse=True)
        pos = 1
        for streamer in streamers_in_category:
            embed.add_field(name=f'{pos}. 🟢 {streamer[0].capitalize()} \n👤: ≈ {streamer[1]}', value=f'https://www.twitch.tv/{streamer[0].casefold()}', inline=False)
            pos += 1
        embeds.append(embed)
    return embeds

def is_owner(interaction: discord.Interaction):
    if interaction.user.id == 33253250299015987:
        return True
    return False


