import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, Embed, ButtonStyle
from nextcord.ui import Button, View
from colorama import Fore, Back, Style
import json
from config import  COLOR_EMBED, IMAGE_LINK, NAME, EMOJI, guildID, welcome_role, ADMIN_ROLE
from itertools import cycle
from functions.YGORole import ButtonYgoRoles, ButtonUpdate
from functions.Json_files import userdata
from functions.EcoFunctoin import CreateUserData


#Class Events Cog
class Welcome(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	
	
	#event welcome user join
	@commands.Cog.listener()
	async def on_member_join(self, member):
		usersdata = await userdata()
		guild = member.guild
		 
		#channel system welcome 
		channel = guild.system_channel
		
		#role for user get
		role = guild.get_role(welcome_role)
		
		#change your guild id from config.py
		if guild.id != guildID:
			return
		
		if str(member.id) not in usersdata:
			welcome_embed = Embed(title=f"**<:Welcome:1186659969458774128> Welcome <:Welcome:1186659969458774128> **", color=COLOR_EMBED)
			welcome_embed.description = f"**We wish you a beautiful and wonderful time in our kingdom\n\n roles for games: <#1135165160772874260>\n Go to <#1183978422221938698>  download all modern Yu-Gi-Oh games**"
			welcome_embed.set_author(name=guild.name, icon_url=IMAGE_LINK["icon"])
			welcome_embed.set_thumbnail(url=member.avatar.url)
			welcome_embed.set_image(url=IMAGE_LINK["welcome"])

			button_v = nextcord.ui.Button(label="Verify", style=ButtonStyle.green, emoji=EMOJI["verified"], disabled=False)
			async def verifie_callback(interaction: Interaction):
				if interaction.user.id != member.id:
					await interaction.response.send_message(content=f"**Sorry this is for {member.mention} only**", ephemeral=True)
					return
				else:
					user = interaction.user
					await CreateUserData(interaction=interaction, user=user, ep=True)
					
					await user.add_roles(role)
					button_v.label = "Done"
					button_v.disabled = True
					await send_embed.edit(f"<a:welcome:1196124429588111513> {member.mention} <a:welcome:1196124429588111513>", embed=welcome_embed, view=view)
					
			view = View(timeout=None)
			button_v.callback = verifie_callback
			view.add_item(button_v)
			send_embed = await channel.send(f"<a:welcome:1196124429588111513> {member.mention} <a:welcome:1196124429588111513>", embed=welcome_embed, view=view)
		else:
			welcome_embed = Embed(title=f"**<:Welcome:1186659969458774128> Welcome Back <:Welcome:1186659969458774128> **", color=COLOR_EMBED)
			welcome_embed.description = f"**Glad to see you with us again. I hope you have an enjoyable time full of enthusiasm and challenge**"
			welcome_embed.set_author(name=guild.name, icon_url=IMAGE_LINK["icon"])
			welcome_embed.set_thumbnail(url=member.avatar.url)
			welcome_embed.set_image(url=IMAGE_LINK["welcome"])
			await channel.send(f"<a:welcome:1196124429588111513> {member.mention} <a:welcome:1196124429588111513>", embed=welcome_embed)
			await member.add_roles(role)
	

		

def setup(bot):
	bot.add_cog(Welcome(bot))
