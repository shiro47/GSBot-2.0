import discord 
from discord import app_commands
from discord.ext import commands, tasks
from database.whitelist_db import WhitelistDB

class webpageAccess(commands.Cog):
    
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    @app_commands.command(name = "add_access_to_admin_panel", description = "Add access to login into admin panel webpage.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(user= "User discord id")
    @app_commands.describe(guild_id= "Guild id")
    async def add_access_to_webpage(self, interaction: discord.Interaction, user: str, guild_id: str):
        await interaction.response.defer()
        db = WhitelistDB()
        user_info = await self.bot.fetch_user(int(user))
        if db.add_user(userName=user_info.display_name, userId=user, avatarUrl="", serverId=int(guild_id)):
            await interaction.followup.send("Added.")
            return
        await interaction.followup.send("Something gone wrong.")
            
            
    
    @app_commands.command(name = "remove_access_to_admin_panel", description = "Remove access to login into admin panel webpage.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(user= "User discord id")
    async def remove_access_to_webpage(self, interaction: discord.Interaction, user: str):
        await interaction.response.defer()
        db = WhitelistDB()
        if db.remove_user(user):
            await interaction.followup.send("Removed.")
            return
        await interaction.followup.send("Something gone wrong.")
    
    @app_commands.command(name = "check_accesses_to_admin_panel", description = "Check accesses to login into admin panel webpage.",)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def check_accesses_to_webpage(self, interaction: discord.Interaction):
        await interaction.response.defer()
        db = WhitelistDB()
        db.get_all_users()
        await interaction.followup.send(db.get_all_users())
    
        
async def setup(bot :commands.Bot):
    await bot.add_cog(webpageAccess(bot))