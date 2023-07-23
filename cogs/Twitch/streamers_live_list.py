import discord 
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
import datetime
import utilities
from APIs.twitch_api import TwitchAPI
from database.twitch_db import TwitchDB
from database.config_db import ConfigDB




class Twitch_live_list(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_ttv_category.start()
        
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(streamer= "Streamer nickname")
    @app_commands.command(name = "register_ttv", description = "Register twitch streamer to database.")
    async def register_ttv(self, interaction: discord.Interaction, streamer: str):
        await interaction.response.defer()
        guild_id = interaction.guild_id
        db = TwitchDB(server_id=str(guild_id))
        if TwitchAPI().check_streamer_existence(streamer)==True:
            if db.check_existance(streamer)==False:
                db.add_streamer(streamer)
            else:
                await interaction.followup.send(f"Streamer {streamer} już istnieje w bazie danych.")
                return
        else:
            await interaction.followup.send(f"Streamer {streamer} nie istnieje.")
            return
        await interaction.followup.send("Zarejestrowano pomyślnie.")
    
    @app_commands.describe(streamer= "Streamer nickname")
    @app_commands.command(name = "unregister_ttv", description = "Unregister twitch streamer from database.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def unregister_ttv(self, interaction: discord.Interaction, streamer: str):
        await interaction.response.defer()
        guild_id = interaction.guild_id
        db = TwitchDB(server_id=str(guild_id))
        if db.check_existance(streamer)==False:
            await interaction.followup.send(f"Streamer {streamer} nie jest zarejestrowany.")
        else: 
            db.remove_streamer(streamer)
            await interaction.followup.send("Wyrejestrowano streamera.")
            
    @app_commands.command(name = "registered_streamers", description = "Display registered streamers in database.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def registered_streamers(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(embed = utilities.embed_all_streamers(server_id=str(interaction.guild_id)))
    
    @app_commands.command(name = "configure_streams_list", description = "Creates embeds for TTV streams.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def configure_streams_list(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        channel_id = interaction.channel_id
        channel = self.bot.get_channel(channel_id)
        embeds = await utilities.create_streamers_live_embeds(guild_id=str(guild_id))
        for embed in embeds:
            await channel.send(embed= embed)
        ConfigDB(server_id=str(guild_id)).create_ids_for_streams_list(channel_id=channel_id)
    

    @tasks.loop(minutes=8)
    async def update_ttv_category(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            config = ConfigDB(server_id=str(guild.id))
            ids = config.check_ids_for_streams_list()
            if ids:
                try:
                    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Updating streamers live list...')
                    channel = self.bot.get_channel(ids["channel_id"])
                    embeds = await utilities.create_streamers_live_embeds(str(guild.id))
                    await channel.purge()
                    for embed in embeds:
                        await channel.send(embed=embed)
                    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Updated streamers live list.')
                except discord.errors.NotFound:
                    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Channel id for streamers live list not found')
            
            
            
async def setup(bot :commands.Bot):
    await bot.add_cog(Twitch_live_list(bot))