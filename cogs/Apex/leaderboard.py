import discord 
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
import datetime
import time
import utilities
from APIs.apex_api import Apex_API
from database.apex_db import ApexDB
from database.config_db import ConfigDB


class ApexLegends_leaderboard(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_leaderboard.start()
        
    @app_commands.command(name = "help", description = "How to register to leaderboard",)
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed= utilities.embed_help())

    
    @app_commands.describe(platform= "Choose platform", nickname="Your origin nickname")
    @app_commands.choices(platform=[
        Choice(name="PC", value="PC"),
        Choice(name="PS", value="PS4"),
        Choice(name="XBOX", value="X1"),
                                    ])
    @app_commands.command(name = "register", description = "Register to Apex leaderboard.")
    async def register(self, interaction: discord.Interaction, platform: str, nickname: str):
        await interaction.response.defer()
        platforms=('PC','PS4','X1')
        guild_id = interaction.guild_id
        apex_db = ApexDB(server_id=str(guild_id))
        if apex_db.check_existance(str(interaction.user.id))==False: 
            if platform in platforms:                   
                if Apex_API().get_rankScore(platform,nickname)!=None:
                    apex_db.add_player(platform, nickname, str(interaction.user.id))
                    await interaction.followup.send('Zarejestrowano.')
                else:
                    await interaction.followup.send('Prawidłowy zapis: `/register {platforma(PC,PS4,X1)} {nick origin}`')
            else:
                await interaction.followup.send('Źle wpisana platforma.')
        else:
            await interaction.followup.send('Jesteś już w systemie.')

    
    @app_commands.command(name = "unregister", description = "Unregister from Apex leaderboard.")
    async def unregister(self, interaction: discord.Interaction): 
        await interaction.response.defer()
        guild_id = interaction.guild_id
        apex_db = ApexDB(server_id=str(guild_id))
        if apex_db.check_existance(str(interaction.user.id)):
            apex_db.remove_player(str(interaction.user.id))
            await interaction.followup.send('Wyrejestrowano.')
            return        
        await interaction.followup.send('Nie jesteś zarejestrowany.')

    @app_commands.command(name = "configure_leaderboard", description = "Creates embeds for leaderboard.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def configure_leaderboard(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        channel_id = interaction.channel_id
        channel = self.bot.get_channel(channel_id)
        message_IDs=[]
        embeds = await utilities.create_leaderboard_embeds(str(guild_id), self.bot)
        for embed in embeds:
            message = await channel.send(embed=embed)
            message_IDs.append(message.id)
        ConfigDB(server_id=str(guild_id)).create_ids_for_apex_leaderboard(channel_id=channel_id, IDs=message_IDs)


    

    @tasks.loop(hours=1)
    async def update_leaderboard(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            config = ConfigDB(server_id=str(guild.id)).check_ids_for_apex_leaderboard()
            if config:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Updating leaderboard...')
                channel= config["channel_id"]
                channel = await self.bot.fetch_channel(channel)
                IDs = config["message_ids"]
                embeds = await utilities.create_leaderboard_embeds(guild_id=str(guild.id), bot=self.bot)
                for message,embed in zip(IDs,embeds):
                    try:        
                        message = await channel.fetch_message(message)
                        await message.edit(embed=embed)
                    except discord.errors.NotFound:
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Leaderboard messages not found.')
                        return
                    time.sleep(3)
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Leaderboard updated.')
        


async def setup(bot :commands.Bot):
    await bot.add_cog(ApexLegends_leaderboard(bot))