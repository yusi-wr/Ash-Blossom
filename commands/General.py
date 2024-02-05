import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import json
import random
import datetime
from functions.EcoFunctoin import set_items, FuncProfile, CreateUserData
from functions.Json_files import userdata
from functions.Cooldowns import  GetCooldwon, CheckCooldwon
from config import IMAGE_LINK, EMOJI, COLOR_EMBED, NAME, owner, GUILD_ID


class General(commands.Cog, name="General"):
    """Points commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
    
    COG_EMOJI = "<:general:1191515983815393431>"
    
    
    #Show Avatar users
    @commands.command(name="avatar", description="your avatar or user`s", pass_context=True)
    @commands.guild_only()
    async def avatar(self, ctx, member: nextcord.Member=None):
    	if member == None:
    		member = ctx.author
    	embed = nextcord.Embed(title=f"**__Avatar__: {member.mention}**", color=COLOR_EMBED)
    	if member.display_avatar:
    		embed.set_image(url=member.display_avatar)
    	else:
    		embed.set_image(url=member.avatar.url)
    	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    	await ctx.send(embed=embed)
    
    #Bot ping
    @commands.command(description="Show the current latency the bot", pass_context=True)
    @commands.guild_only()
    async def ping(self, ctx):
    	latency = round(self.bot.latency * 1000)
    	embed = nextcord.Embed(title=f"**__Latency__**: {self.bot.user.mention} 🐇", color=0xff1289)
    	embed.description = f"**<:latency:1183327015558983722> Api Latency: __{latency}__ms**"
    	embed.set_author(icon_url=ctx.author.avatar.url, name=f"{ctx.author.name}")
    	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    	await ctx.send(embed=embed)
    
    #command uptime
    @commands.command(name='uptime', aliases=['up'])
    @commands.guild_only()
    async def get_uptime(self, ctx):
        current_time = datetime.datetime.utcnow()
        uptime_duration = current_time - self.start_time
        days, hours, minutes, seconds = self.convert_timedelta(uptime_duration)
        await ctx.send(embed=nextcord.Embed(
            color=0xff1289,
            title="<:uptime:1183525212998869013> Bot Uptime",
            description=f"<:time:1183525262713958532> ** `{days}` Days, `{hours}` Hours `{minutes}` Minutes, `{seconds}` Seconds**"
        ))
    def convert_timedelta(self, duration):
        days, seconds = divmod(duration.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return int(days), int(hours), int(minutes), int(seconds)
    
    
    #command transfer DP points form user to user
    @commands.guild_only()
    @commands.command(name="transfer", descirption="Transfer DP points to user", aliases=["tr"])
    async def transfer(self, ctx: commands.Context, user: nextcord.Member, DP: int, msg: str ="Non message...."):
    
    	  data = await userdata()
    	  
    	  if str(ctx.author.id) not in data:
    	  	await ctx.send("**Your account not activated \n please run slash command: `/verifie` **")
    	  	return
    	  elif str(user.id) not in data:
    	  	await ctx.send(f"** Sorry the `{user.display_name}` account not activated**")
    	  	return
    	  elif DP > data[str(ctx.author.id)]["DP"]:
    	  	await ctx.reply(f"**Sorry you dont have {EMOJI['DP']} {DP}")
    	  	return
    	  
    	  data[str(user.id)]["DP"] += DP
    	  data[str(ctx.author.id)]["DP"] -= DP
    	  embed = nextcord.Embed(title=f"**Has been transferred**", color=COLOR_EMBED)
    	  embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
    	  embed.description = f"**Transfer: {EMOJI['DP']} `{DP:,}` to {user.mention}\nFrom: {ctx.author.mention}**"
    	  with open("./data/usersdata.json", "w") as f:
    	  	json.dump(data, f, indent=2)
    	  await ctx.send(embed=embed)
    	  
    	  msgDirect = nextcord.Embed(title="**You have a DP ext**", color=COLOR_EMBED, description=f">>> **DP: {EMOJI['DP']} `{DP:,}`\nFrom {ctx.author.mention}\nMessage: ```{msg}```**")
    	  msgDirect.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    	  await user.send(embed=msgDirect)


    #command profile
    @commands.command(name="profile", description="get user's profile", aliases=["pro"])
    @commands.guild_only()
    async def profile(self, ctx:commands.Context, user: nextcord.Member=None):
    	
    	author = ctx.author
    	
    	data = await userdata()
    	embed = nextcord.Embed(color=COLOR_EMBED)
    	embed.set_thumbnail(url=IMAGE_LINK["!"])
    	
    	if str(author.id) not in data:
    		embed.description = f">>> **Your account it`s not activated\nPlease run slash command: `/verifie` **"
    		await ctx.reply(embed=embed)
    		return
    	if user and str(user.id) not in data:
    		embed.description = f">>> **Sorry, account {user.mention} it`s not activated**"
    		await ctx.reply(embed=embed)
    		return
    	
    	await FuncProfile(ctx=ctx, user=user)
    	
    
    #command remove warns 
    @commands.command(name="rvwarn", description="pay your warns to remove from ur profile", aliases=["pw"])
    @commands.guild_only()
    async def rvwarn(self, ctx: commands.Context, points: int = None):
        
        data = await userdata()
        user = ctx.author
        
        if str(user.id) not in data:
        	return
        
        if points > data[str(user.id)]["DP"]:
        	await ctx.send(f"**Sorry, you don't have: {EMOJI['DP']} `{points}`**")
        	return
        
        if points == 150:
        	data[str(user.id)]["Warns"] -= 1
        	data[str(user.id)]["DP"] -= points
        	amount = 1
        elif points == 300:
        	if data[str(user.id)]["Warns"] < 2:
        		data[str(user.id)]["Warns"] = 0
        	else:
        		data[str(user.id)]["Warns"] -= 2
        	data[str(user.id)]["DP"] -= points
        	amount = 2
        elif points == 400:
        	if data[str(user.id)]["Warns"] < 4:
        		data[str(user.id)]["Warns"] = 0
        	else:
        		data[str(user.id)]["Warns"] -= 4
        	data[str(user.id)]["DP"] -= points
        	amount = 4
        elif points == 600:
        	if data[str(user.id)]["Warns"] < 6:
        		data[str(user.id)]["Warns"] = 0
	        else:
	        	data[str(user.id)]["Warns"] -= 6
        	data[str(user.id)]["DP"] -= points
        	amount = 6
        elif points == 800:
        	if data[str(user.id)]["Warns"] < 8:
        		data[str(user.id)]["Warns"] = 0
        	else:
        		data[str(user.id)]["Warns"] -= 8
        	data[str(user.id)]["DP"] -= points
        	amount = 8
        elif points == 1000:
        	data[str(user.id)]["Warns"] = 0
        	data[str(user.id)]["DP"] -= points
        	amount = "All"
        else:
        	embed = nextcord.Embed(color=COLOR_EMBED)
        	embed.description =f"**for example:\n150{EMOJI['DP']} == 1warn\n300{EMOJI['DP']} == 2warns\n400{EMOJI['DP']} == 4warn\n600{EMOJI['DP']} == 6warns\n800 {EMOJI['DP']} == 8warns\n1000{EMOJI['DP']} == All**"
        	embed.set_thumbnail(url=IMAGE_LINK["no"])
        	await ctx.send(embed=embed)
        	return
        
        with open('./data/usersdata.json', 'w') as f:
        	json.dump(data, f, indent=2)
        
        embed = nextcord.Embed(title=f"**SUCCESS**", color=COLOR_EMBED)
        embed.description=f"**Remove: {EMOJI['Warn']} `{amount}` warns\nForm your profile data\nFor show profile run: `?pro`**"
        embed.set_thumbnail(url=IMAGE_LINK["ok"])
        embed.set_author(name=NAME, icon_url=IMAGE_LINK['icon'])
        
        await ctx.send(embed=embed)
    
    #command daily
    @commands.command(name="daily")
    async def dailyDP(self, ctx: commands.Context):
    	
    	data = await userdata()
    	embed = nextcord.Embed(color=COLOR_EMBED)
    	user = ctx.author
    	if str(user.id) not in data:
    		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    		embed.description = f">>> **Your account it`s not activated\nPlease run slash command: `/verifie` **"
    		embed.set_thumbnail(url=IMAGE_LINK["!"])
    		await ctx.reply(embed=embed)
    		return
    	
    	cooldown = await CheckCooldwon(command="daily",user=user)
    	
    	if cooldown == True:
    		DP = random.randint(1152, 2152)
    		data[str(user.id)]["DP"] += DP
    		with open("./data/usersdata.json", "w") as f:
    			json.dump(data, f, indent=2)
    		
    		embed.title = "**daily claimed :)**"
    		embed.description = f"**You claim: {EMOJI['DP']} `{DP:,}`\nThank you ^_^**"
    		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
    		embed.set_thumbnail(url=IMAGE_LINK["icon"])
    		
    		await ctx.reply(embed=embed)
    	else:
    		Cooltime = await GetCooldwon(command="daily", user=user)
    		embed.description = f"**You've already claimed your daily DP :)\nWait for: `{Cooltime}`\nSorry and thank you ^_^**"
    		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    		embed.set_thumbnail(url=IMAGE_LINK["no"])
    		await ctx.reply(embed=embed)
    
    #command give user reputation points
    @commands.command(name="rep")
    async def Reputation(self, ctx: commands.Context, member: nextcord.Member):
    	
    	user = ctx.author
    	embed = nextcord.Embed(color=COLOR_EMBED)
    	data = await userdata()
    	
    	if str(user.id) not in data:
    		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    		embed.description = f">>> **Your account it`s not activated\nPlease run slash command: `/verifie` **"
    		embed.set_thumbnail(url=IMAGE_LINK["!"])
    		await ctx.reply(embed=embed)
    		return 
    	elif str(member.id) not in data:
    		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    		embed.description = f">>> **Account {member.mention} it`s not activated**"
    		embed.set_thumbnail(url=IMAGE_LINK["!"])
    		await ctx.reply(embed=embed)
    		return
    	elif member == user:
    		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    		embed.description = f">>> **Sorry you can do that for yourself ^_^**"
    		embed.set_thumbnail(url=IMAGE_LINK["no"])
    		await ctx.reply(embed=embed)
    		return
    	
    	cooldwon = await CheckCooldwon(command="rep", user=user)
    	
    	if cooldwon == True:
    		data[str(member.id)]["Rep"] += 1
    		with open("./data/usersdata.json", "w") as f:
    			json.dump(data, f, indent=2)
    		
    		embed.title = "**Added a new reputation points**"
    		embed.description = f"**Totel now: {EMOJI['Rep']} `{data[str(member.id)]['Rep']}`\nFrom: {user.mention}**"
    		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
    		embed.set_thumbnail(url=IMAGE_LINK["icon"])	
    		await ctx.reply(f"{member.mention}", embed=embed)
    		
    	else:
    		Cooltime = await GetCooldwon(command="rep", user=user)
    		embed.description = f"**You already used thus command :)\nWait for: `{Cooltime}`\nSorry and thank you ^_^**"
    		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    		embed.set_thumbnail(url=IMAGE_LINK["no"])
    		await ctx.reply(embed=embed)
    
    
    #command verifie user and create data
    @nextcord.slash_command(name="verifie", description="Verify and create your account", guild_ids=GUILD_ID)
    async def Verifie(self, interaction: Interaction):
    	
    	user = interaction.user
    	
    	try:
    		await CreateUserData(interaction=interaction, user=user, ep=False)
    	except ValueError as VE:
    		embed = nextcord.Embed(color=COLOR_EMBED)
    		embed.set_thumbnail(IMAGE_LINK["!"])
    		embed.title = "**Something is wrong**"
    		embed.description = f"```{VE}```"
   
def setup(bot):
    bot.add_cog(General(bot))