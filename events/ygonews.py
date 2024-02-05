import time
import feedparser
import nextcord
import json
from colorama import Fore, Style
from nextcord.ext import commands, tasks
from config import ygo_news, anime_news
from functions.Json_files import YGONews

class NewsEvents(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	
	@commands.Cog.listener()
	async def on_ready(self):
		
		await self.YGOOrgin.start()
		await self.ClearLinks.start()
		
	
	#Tasks for  ygorgian news
	@tasks.loop(seconds=600)
	async def YGOOrgin(self):
		print(Fore.LIGHTGREEN_EX + "Start " + Fore.LIGHTBLUE_EX + " • " + Fore.LIGHTMAGENTA_EX +"YGONews")
		FEED_URL = 'https://ygorganization.com/feed/'
		feed = feedparser.parse(FEED_URL)
		channel = self.bot.get_channel(ygo_news)
		SaveData = await YGONews()
		
		if "YGO" not in SaveData:
			SaveData["YGO"] = []
			json.dump(SaveData, open("./data/ygonews.json", "w"), indent=2)
		if feed.entries:
		      	feeds = feed.entries[0]
		      	title = feeds.title
		      	link = feeds.link
		      	desc = feeds.description
		      	
		      	
		      	if link not in SaveData["YGO"]:
		      		
		      		send = await channel.send(f">>> **• {title} •**\n```{desc}```\n**Link**: {link}")
		      		await send.edit(f">>> **{title}**\n```{desc}```\n**Link**: {link}\n@here")
		      	
		      		SaveData["YGO"].append(link)
		      		json.dump(SaveData, open("./data/ygonews.json", "w"), indent=2)
	
	#clear all links form news data after 48 hour	    
	@tasks.loop(minutes=60 * 48)
	async def ClearLinks(self):
		print(Fore.LIGHTGREEN_EX + "Start " + Fore.LIGHTBLUE_EX + " • " + Fore.LIGHTMAGENTA_EX + "ClearLinks")
		DataNews = await YGONews()
		
		
		if len(DataNews["YGO"]) > 200:
			DataNews["YGO"] = []
			json.dump(DataNews, open("./data/ygonews.json", "w"), indent=2)




def setup(bot: commands.Bot):
	bot.add_cog(NewsEvents(bot))