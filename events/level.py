import nextcord
from nextcord.ext import commands
import json
from random import randint
from config import EMOJI, COLOR_EMBED, NAME, IMAGE_LINK, guildID, ADMIN_ROLE, channel_level
from functions.Json_files import userdata


#Func add xp 
async def AddXP(user, guild, xp):
	if user.bot:
		return False
	data = await userdata()
	if not str(user.id) in data:
		return False
	
	data[str(user.id)]["XP"] += xp
	with open("./data/usersdata.json", "w") as f:
		json.dump(data, f, indent=2)

#Func level up
async def LevelUp(user, message, channel):
		
		if user.bot:
			return False
		
		data = await userdata()
		if not str(user.id) in data:
			return False
		XP = data[str(user.id)]["XP"]
		Level = data[str(user.id)]["Lv"]
		EndLevel = int(XP ** (1/4))
		
		if Level < EndLevel:
			DP = randint(270, 5700)
			embed = nextcord.Embed(title="**Congratulations on a new level**" , color=COLOR_EMBED)
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/775069709552844830.png")
			embed.description = f">>> **New level: {EMOJI['Lv']} `{EndLevel}`\nYou get: {EMOJI['DP']} `{DP}` **"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_footer(text=f"{user.display_name}", icon_url=user.avatar.url)
			
			data[str(user.id)]["DP"] += DP
			data[str(user.id)]["Lv"] = EndLevel
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f , indent=2)
				
			await channel.send(f"{user.mention}", embed=embed)
		

class LevelSystem(commands.Cog):
		def __init__(self, bot: commands.Bot):
			self.bot = bot
		
		@commands.Cog.listener()
		async def on_message(self, message):
			guild = message.guild
			channel = self.bot.get_channel(channel_level)
			author = message.author
			
			if guild.id != guildID:
				return
			await AddXP(user=author, guild=guild, xp=5)
			await LevelUp(user=author, message=message, channel=channel)				
		




def setup(bot):
	bot.add_cog(LevelSystem(bot))		
