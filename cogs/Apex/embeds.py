import discord 
from discord import app_commands
from discord.ext import commands, tasks
from database.config_db import ConfigDB as config_db
import datetime
import utilities

class ApexLegends_embeds(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_pred.start()
        self.update_map_rotation.start()
        
    @app_commands.command(name = "configure_predator_threshold", description = "Creates embed for predator threshold.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def configure_predator_threshold(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        channel_id = interaction.channel_id
        channel = self.bot.get_channel(channel_id)
        message = await channel.send(embed= utilities.embed_pred())
        config_db(server_id=str(guild_id)).create_ids_for_pred(channel_id=channel_id, message_id=message.id)
        
    @app_commands.command(name = "configure_map_rotation", description = "Creates embed for map rotation.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def configure_map_rotation(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        channel_id = interaction.channel_id
        channel = self.bot.get_channel(channel_id)
        embeds=utilities.embed_map_rotation()
        pubs_message = await channel.send(embed= embeds[0], content="Pubs:")
        ranked_message = await channel.send(embed= embeds[1], content="Ranked:")
        config_db(server_id=str(guild_id)).create_ids_for_map_rotation(channel_id=channel_id, message_id=pubs_message.id, message_id_ranked=ranked_message.id)
        
    @tasks.loop(hours=1)
    async def update_pred(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            config = config_db(server_id=str(guild.id))
            ids = config.check_ids_for_pred()
            if ids:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f'|Server: {guild.name} | Updating predator threshold...')
                try:
                    channel = self.bot.get_channel(int(ids["channel_id"]))
                    message = await channel.fetch_message(int(ids["message_id"]))
                    await message.edit(embed=utilities.embed_pred(), content='')
                    print(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"), f'|Server: {guild.name} | Predator threshold updated.')
                except discord.errors.NotFound:
                    print(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"), f'|Server: {guild.name} | Predator threshold message not found.')

    @tasks.loop(minutes=10)
    async def update_map_rotation(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            config = config_db(server_id=str(guild.id))
            ids = config.check_ids_for_map_rotation()
            if ids:
                print(datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"), f'|Server: {guild.name} | Updating map rotations...')
                try:
                    channel = self.bot.get_channel(int(ids["channel_id"]))
                    message = await channel.fetch_message(int(ids["message_id"]))
                    await message.edit(embed=utilities.embed_map_rotation()[0], content='Pubs:')
                    print(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"), f'|Server: {guild.name} | Map rotation updated.')
                    ranked_message = await channel.fetch_message(int(ids["message_id_ranked"]))
                    await ranked_message.edit(embed=utilities.embed_map_rotation()[1], content='Ranked:')
                    print(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"), f'|Server: {guild.name} | Ranked map rotation updated.')
                except (discord.errors.NotFound, KeyError):
                    print(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"), f'|Server: {guild.name} | Map rotation message not found.')
        
async def setup(bot :commands.Bot):
    await bot.add_cog(ApexLegends_embeds(bot))