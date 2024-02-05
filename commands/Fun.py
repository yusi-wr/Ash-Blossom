import nextcord
from nextcord import  Embed
from nextcord.ext import commands
import random
import aiohttp
from PIL import Image
import giphy_client
from  giphy_client.rest import  ApiException
from googleapiclient.discovery import build
from config import  COLOR_EMBED, NAME, IMAGE_LINK




class Fun(commands.Cog):
    """Fun commands"""
    def __init__(self, bot):
        self.bot = bot
    
    COG_EMOJI = "<:fun:1191516216448258179>"
    
    
    #drake meme command
    @commands.command()
    @commands.guild_only()
    async def drake(self, ctx: commands.Context, msg1, msg2):
    	embed =Embed(title="**Drake Meme**", color=COLOR_EMBED)
    	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    	embed.set_image(url=f"https://api.popcat.xyz/drake?text1={msg1}&text2={msg2}")
    	await ctx.send(embed=embed)
    
    #oog meme command
    @commands.command()
    @commands.guild_only()
    async def oog(self, ctx: commands.Context, msg):
    	embed =Embed(title="**Oogway Meme**", color=COLOR_EMBED)
    	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    	embed.set_image(url=f"https://api.popcat.xyz/oogway?text={msg}")
    	await ctx.send(embed=embed)
    
    #pooh meme command
    @commands.command()
    @commands.guild_only()
    async def pooh(self, ctx: commands.Context, msg1, msg2):
    	embed =Embed(title="**Pooh Meme**", color=COLOR_EMBED)
    	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
    	embed.set_image(url=f"https://api.popcat.xyz/pooh?text1={msg1}&text2={msg2}")
    	await ctx.send(embed=embed)
    
    
    #Command gif 
    @commands.command(name="gif")
    @commands.guild_only()
    async def gif(self,ctx: commands.Context, *,text="smile"):
    	
	    api_key = "aTQbzmnHBWXX17EJcMVuSBptYsxtZli7"
	    api_instance = giphy_client.DefaultApi()
	    
	    api_responce = api_instance.gifs_search_get(api_key, text, limit=5, rating="g")
	    List = list(api_responce.data)
	    gifs = random.choice(List)
	    
	    embed = Embed(title=f"**{text}**", color=COLOR_EMBED)
	    embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
	    embed.set_image(url=f"https://media.giphy.com/media/{gifs.id}/giphy.gif")
	    embed.set_footer(text=f"By: {ctx.author.name}", icon_url=ctx.author.avatar.url)
	    
	    await ctx.send(embed=embed)
    
    
    #command meme
    @commands.command("meme")
    @commands.guild_only()
    async def meme(self, ctx: commands.Context):
    	async with aiohttp.ClientSession() as cd:
    		async with cd.get("https://www.reddit.com/r/memes.json") as r:
    			memes = await r.json()
    			
    			embed = Embed(color=COLOR_EMBED)
    			embed.set_image(url=memes["data"]["children"][random.randint(0, 10)]["data"]["url"])
    			embed.set_author(name=NAME + " | Meme", icon_url=IMAGE_LINK["icon"])
    			embed.set_footer(text=f"Send by: {ctx.author.name}", icon_url=ctx.author.avatar.url)
    			
    			await ctx.send(embed=embed)
    
    
    #command image search
    @commands.command(aliases=["img"])
    async def images(self, ctx: commands.Context, *, search):
    	
    	api_key = "AIzaSyDId_oN6acZT-UMHTfYEZUgIcl4GVn1s6g"
    	
    	ran = random.randint(0, 5)
    	resource = build("customsearch", "v1", developerKey=api_key).cse()
    	
    	result = resource.list(q=f"{search}", cx="2166875ec165a6c21", searchType="image").execute()
    	url = result["items"][ran]["link"]
    	embed = Embed(title=f"**Here Your Image ({search}) **", color=COLOR_EMBED)
    	embed.set_author(name=NAME + " | Search Images", icon_url=IMAGE_LINK["icon"])
    	embed.set_image(url=url)
    	embed.set_footer(text=f"Search By: {ctx.author.name}", icon_url=ctx.author.avatar.url)
    	
    	await ctx.send(embed=embed)    
    
    
    

def setup(bot):
    bot.add_cog(Fun(bot))
