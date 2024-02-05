import nextcord
from nextcord import Interaction
from nextcord.ext import commands, application_checks
from config import COLOR_EMBED, IMAGE_LINK, ADMIN_ROLE, NAME


class EventErreurs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_application_command_error(self, interaction: Interaction, error: nextcord.ext.application_checks.errors):
	     guild = interaction.guild
	     
	     if isinstance(error, application_checks.ApplicationMissingRole):
	     	leader_role = guild.get_role(ADMIN_ROLE)
	     	embed = nextcord.Embed(title=f"**Sorry, {interaction.user.mention}**", color=COLOR_EMBED)
	     	embed.description = f">>> **You need {leader_role.mention} role for run this command**"
	     	embed.set_thumbnail(url=IMAGE_LINK["no"])
	     	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
	     	await interaction.response.send_message(embed=embed, ephemeral=True)
	     	return 
	     	
	     elif isinstance(error, application_checks.errors.ApplicationMissingRole):
	     	leader_role = guild.get_role(ADMIN_ROLE)
	     	embed = nextcord.Embed(title=f"**Sorry, {interaction.user.mention}**", color=COLOR_EMBED)
	     	embed.description = f">>> **You need {leader_role.mention} role for run this command**"
	     	embed.set_thumbnail(url=IMAGE_LINK["no"])
	     	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
	     	await interaction.response.send_message(embed=embed, ephemeral=True)
	     	return
	     	
	     elif isinstance(error, application_checks.errors.ApplicationMissingPermissions):
	     	leader_role = guild.get_role(ADMIN_ROLE)
	     	embed = nextcord.Embed(title=f"**Sorry, {interaction.user.mention}**", color=COLOR_EMBED)
	     	embed.description = f">>> **You don't' have the permissions for do this**"
	     	embed.set_thumbnail(url=IMAGE_LINK["no"])
	     	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
	     	await interaction.response.send_message(embed=embed, ephemeral=True)
	     	return
	     	
	     elif isinstance(error, application_checks.errors.ApplicationBotMissingPermissions):
	     	leader_role = guild.get_role(ADMIN_ROLE)
	     	embed = nextcord.Embed(title=f"**Sorry, {interaction.user.mention}**", color=COLOR_EMBED)
	     	embed.description = f">>> **I don't' have the permissions for do this**"
	     	embed.set_thumbnail(url=IMAGE_LINK["no"])
	     	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
	     	await interaction.response.send_message(embed=embed, ephemeral=True)
	     	return
	     	
	     else:
	     	embed = nextcord.Embed(title=f"**Something wrong here**", color=COLOR_EMBED)
	     	embed.set_thumbnail(url=IMAGE_LINK["!"])
	     	embed.description = f">>> ```{error}```"
	     	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
	     	await interaction.response.send_message(embed=embed, ephemeral=True)
	
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		 
		 if isinstance(error, commands.MissingRole):
		 	leader_role = ctx.guild.get_role(ADMIN_ROLE)
		 	embed = nextcord.Embed(title=f"**Sorry, {ctx.author.mention}**", color=COLOR_EMBED)
		 	embed.description = f">>> **This command for {leader_role.mention} only**"
		 	embed.set_thumbnail(url=IMAGE_LINK["no"])
		 	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
		 	await ctx.send(embed=embed)
		 	
		 elif isinstance(error, commands.BotMissingPermissions):
		 	embed = nextcord.Embed(title=f"**Sorry, {ctx.author.mention}**", color=COLOR_EMBED)
		 	embed.description = f">>> **I don't have the permissions for do this**"
		 	embed.set_thumbnail(url=IMAGE_LINK["no"])
		 	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
		 	await ctx.send(embed=embed)
		 	
		 elif isinstance(error, commands.MissingPermissions):
		 	embed = nextcord.Embed(title=f"**Sorry, {ctx.author.mention}**", color=COLOR_EMBED)
		 	embed.description = f">>> **You don't' have the permissions for do this**"
		 	embed.set_thumbnail(url=IMAGE_LINK["no"])
		 	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
		 	await ctx.send(embed=embed)
		 	
		 else:
		 	embed = nextcord.Embed(title=f"**Something wrong here**", color=COLOR_EMBED)
		 	embed.set_thumbnail(url=IMAGE_LINK["!"])
		 	embed.description = f">>> ```{error}```"
		 	embed.set_author(name=NAME, icon_url=IMAGE_LINK["bot-icon"])
		 	await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(EventErreurs(bot))