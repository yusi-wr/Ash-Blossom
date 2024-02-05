import nextcord
from nextcord.ext import commands
from nextcord import Embed
from random import choice
from config import COLOR_EMBED, NAME, IMAGE_LINK

gifs = {
    "kick": ["https://tenor.com/blQ4u.gif", "https://tenor.com/bUH4C.gif", "https://tenor.com/xhlc.gif", "https://tenor.com/brHRW.gif", "https://tenor.com/brHRW.gif", "https://tenor.com/bNcQG.gif"],
    
    "punch": ["https://tenor.com/blZV2.gif", "https://tenor.com/bSS7A.gif", "https://tenor.com/bFk9M.gif", "https://tenor.com/bOeuo.gif", "https://tenor.com/bUdox.gif"],
    
    "thanks": ["https://tenor.com/b2m3G.gif", "https://tenor.com/bSz6I.gif", "https://tenor.com/bV3Wx.gif", "https://tenor.com/bTMAh.gif"],
    
    "yes": ["https://tenor.com/be0Om.gif", "https://tenor.com/beF0j.gif", "https://tenor.com/bg2Sg.gif", "https://tenor.com/bTZUE.gif", "https://tenor.com/eeRwsOEZ91K.gif"],
    
    "kill": ["https://tenor.com/bslqe.gif", "https://tenor.com/bkYsR.gif", "https://tenor.com/bngig.gif"]
}


class AnimeFun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	COG_EMOJI = "<:image:1158014522800476242>"
	
	
	#command anime kick gif send
	@commands.command(name="a-kick")
	async def AnimeKick(self, ctx: commands.Context, user: nextcord.Member = None):
		
		
		
		if user:
			await ctx.send(f"**{user.mention}**")
			await ctx.send(choice(gifs["kick"]))
		else:
			await ctx.reply(choice(gifs["kick"]))
	
	#command anime pance gif send
	@commands.command(name="a-punch")
	async def AnimePance(self, ctx: commands.Context, user: nextcord.Member = None):
		
		if user:
			await ctx.send(f"**{user.mention}**")
			await ctx.send(choice(gifs["punch"]))
		else:
			await ctx.reply(choice(gifs["punch"]))
		
		
			
	#command anime thanks gif send
	@commands.command(name="a-thanks")
	async def AnimeThank(self, ctx: commands.Context, user: nextcord.Member = None):
		
		if user:
			await ctx.send(f"**{user.mention}**")
			await ctx.send(choice(gifs["thanks"]))
		else:
			await ctx.reply(choice(gifs["thanks"]))
	
	#command anime yes gif send
	@commands.command(name="a-yes")
	async def AnimeYes(self, ctx: commands.Context, user: nextcord.Member = None):
		
		if user:
			await ctx.send(f"**{user.mention}**")
			await ctx.send(choice(gifs["thanks"]))
		else:
			await ctx.reply(choice(gifs["thanks"]))
	
	#command anime thanks gif send
	@commands.command(name="a-kill")
	async def AnimeKill(self, ctx: commands.Context, user: nextcord.Member = None):
		
		if user:
			await ctx.send(f"**{user.mention}**")
			await ctx.send(choice(gifs["kill"]))
		else:
			await ctx.reply(choice(gifs["kill"]))
			
	
		
def setup(bot: commands.Bot):
	bot.add_cog(AnimeFun(bot))

  