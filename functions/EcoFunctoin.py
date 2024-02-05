import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, Embed
from nextcord.ui import Button, View
import json	
from config import EMOJI, COLOR_EMBED, NAME, IMAGE_LINK
import random
from .Buttons import ButtonPage, ButtonFuncProfile
from .Json_files import userdata, storedata, useritems
from .ItemsFunctions import *
from .Cooldowns import CheckCooldwonItems, GetCooldwonItem


#Func Profile command
async def FuncProfile(ctx: commands.Context, user: nextcord.Member=None):
	
	if user == None:
		user = ctx.author
	userData = await userdata()
	storeData = await storedata()
	userItems = await useritems()
	
	
	Items = [name for name in userItems[str(user.id)]]
	DP = userData[str(user.id)]["DP"]
	Lv = userData[str(user.id)]["Lv"]
	LP = userData[str(user.id)]["LP"]
	LPLimit = userData[str(user.id)]["Limit-LP"]
	Rep = userData[str(user.id)]["Rep"]
	XP = userData[str(user.id)]["XP"]
	Warns = userData[str(user.id)]["Warns"]
	Tourna = userData[str(user.id)]["Tournament"]
	#Duels = userData[str(user.id)]["Duels"]
	ItemsLimit = userData[str(user.id)]["Limit-Items"]
	if "desc" in userData[str(user.id)]:
		desc = userData[str(user.id)]["desc"]
	else:
		desc = ".......?"
	if "icon" in userData[str(user.id)]:
		icon = userData[str(user.id)]["icon"]
	else:
		icon = user.avatar.url
	
	
	#embed profile user page 1
	embed_pro1 = Embed(color=COLOR_EMBED)
	embed_pro1.set_thumbnail(url=icon)
	embed_pro1.description = f"**• __{user.mention}__ •\n>>> DP: {EMOJI['DP']} `{DP:,}`\nLP: {EMOJI['LP']} `{LP}/{LPLimit}`\nTournments: {EMOJI['Tournament']} `{Tourna}`\nLV: {EMOJI['Lv']} `{Lv}`\nXP: {EMOJI['XP']} `{XP}`**"
	embed_pro1.add_field(name="**User description**", value=f">>> ```{desc}```")
	embed_pro1.set_author(name=user.display_name, icon_url="https://cdn.discordapp.com/emojis/792272103914209281.png")
	embed_pro1.set_footer(text=f"Summon by: {ctx.author.name} | Page: 1/2", icon_url=ctx.author.avatar.url)
	
	#embed profile user page 2
	embed_pro2 = Embed(color=COLOR_EMBED)
	embed_pro2.set_thumbnail(url=icon)
	embed_pro2.description = f"**• __{user.mention}__ •\n>>> Reputation: {EMOJI['Rep']} `{Rep}`\nWarns: {EMOJI['Warn']} `{Warns}`\nItems: {EMOJI['items']} `{len(Items)}/{ItemsLimit}`**"
	embed_pro2.add_field(name="**User description**", value=f">>> ```{desc}```")
	embed_pro2.set_author(name=user.display_name, icon_url="https://cdn.discordapp.com/emojis/792272103914209281.png")
	embed_pro2.set_footer(text=f"Summon by: {ctx.author.name} • Page: 2/2 ", icon_url=ctx.author.avatar.url)
	
	msg = await ctx.reply(embed=embed_pro1)
	await msg.edit(view=ButtonFuncProfile(embed_page1=embed_pro1, embed_page2=embed_pro2, msg=msg,user=user))

#func for add items in data store
async def set_items(interaction: Interaction, name: str, price: int, icon: str, amount: int, desc: str):
		
		data = await storedata()
			
		if name in data:
			await interaction.response.send_message("**Sorry this item` already its in the data list**")
		else:
			
			data[name] = {}
			data[name]["price"] = price
			data[name]["amount"] = amount
			data[name]["icon"] = icon
			data[name]["desc"] = desc
			
			embed = nextcord.Embed(title="**Done Successfully**" , color=COLOR_EMBED)
			embed.description = f"**Price: {EMOJI['DP']} `{price:,}`\nAmount: `{amount:,}`**"
			embed.add_field(name="**Description**", value=f">>> ```{desc}```")
			embed.set_thumbnail(url=icon)
			embed.set_author(name="New item Added", icon_url=IMAGE_LINK["ok"])
			with open("./data/store.json", "w") as f:
				json.dump(data, f, indent=2)
			await interaction.response.send_message(embed=embed, ephemeral=True)

#Func create user data if he/she verifie
async def CreateUserData(interaction: Interaction, user: nextcord.Member, ep):
	
	data = await userdata()
	Items = await useritems()
	embed = Embed(color=COLOR_EMBED)
	if str(user.id) in data:
		embed.description = f"**Sorry, but your account is already activated**"
		embed.set_author(name="Something is wrong")
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await interaction.response.send_message(embed=embed, ephemeral=ep)
		return
	
	data[str(user.id)] = {}
	data[str(user.id)]["DP"] = 500
	data[str(user.id)]["Warns"] = 0
	data[str(user.id)]["Rep"] = 0
	data[str(user.id)]["Lv"] = 1
	data[str(user.id)]["LP"] = 100
	data[str(user.id)]["XP"] = 0
	data[str(user.id)]["Limit-LP"] = 100
	data[str(user.id)]["Tournament"] = 0
	data[str(user.id)]["Limit-Items"] = 5
	data[str(user.id)]["Duels"] = 0
	Items[str(user.id)] = {}
	
	embed.title = f"**Thanks {user.mention}**"
	embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
	embed.description = "**Your account is now activated**"
	embed.set_thumbnail(url=user.avatar.url)
	
	with open("./data/usersdata.json", "w") as f:
	   json.dump(data, f, indent=2)
	with open("./data/useritems.json", "w") as f:
	   json.dump(Items, f, indent=2)
	
	await interaction.response.send_message(embed=embed, ephemeral=ep)


# func update items  
async def update_items(interaction: Interaction, name: str, price: int=None, icon: str=None, amount: int=None, desc: str=None):
			
			data = await storedata()
				
			if price:
				data[name]["price"] = price
			if desc:
				data[name]["desc"] = desc
			if icon:
				data[name]["icon"] = icon
			if amount:
				data[name]["amount"] = amount
			
			if price or desc or icon or amount:
				with open("./data/store.json", "w") as f:
					json.dump(data, f, indent=2)
				await interaction.response.send_message("**Done the item `{name}` is updated**", ephemeral=True)
			else:
				return

# func show items from store
async def showitems(interaction: Interaction, name: str=None):
		
		data = await storedata()
		
		if name:
			embed = nextcord.Embed(title=name, color=COLOR_EMBED)
			embed.description = f"**Price: {EMOJI['DP']} `{data[name]['price']:,}`\nAmount: `{data[name]['amount']}`**"
			embed.add_field(name="**Descrption**", value=f">>> ```{data[name]['desc']}```")
			embed.set_thumbnail(url=data[name]["icon"])
			embed.set_author(name=f"{NAME} | Store", icon_url="https://cdn.discordapp.com/emojis/885875777952964668.png")
			await interaction.response.send_message(embed=embed, ephemeral=True)
		else:
			list_embeds = []
			list_names = []
			for name in data:
						icon = data[name]["icon"]
						embed = nextcord.Embed(title=name, color=COLOR_EMBED)
						embed.description = f"**Price: {EMOJI['DP']} `{data[name]['price']:,}`\nAmount: `{data[name]['amount']}`**"
						embed.add_field(name="**Descrption**", value=f">>> ```{data[name]['desc']}```")
						embed.set_thumbnail(url=icon)
						embed.set_author(name=f"{NAME} | Store", icon_url="https://cdn.discordapp.com/emojis/885875777952964668.png")
						embed.set_footer(text="run: /buy | to get it", icon_url=interaction.user.avatar.url)
						list_embeds.append(embed)
						list_names.append(name)
			
			ButtonBuy = Button(label="Buy", style=ButtonStyle.green, emoji="<:shopping:1196406209314562088>")
			async def ButtonBuyCallBack(interaction: Interaction):
				await Buy(interaction=interaction, name=list_names[view.page],user=interaction.user, ep=True)
			
			ButtonBuy.callback = ButtonBuyCallBack
			
			msg = await interaction.response.send_message(f"{interaction.user.mention}" ,embed=list_embeds[0], ephemeral=False)
			view = ButtonPage(embeds=list_embeds, msg=msg)
			view.add_item(ButtonBuy)
			await msg.edit(view=view)


#Func Buy Items from store
async def Buy(interaction: Interaction, name, user: nextcord.Member==None, ep):
	if user == None:
		user = interaction.user
		
	data = await userdata()
	items = await useritems()
	store = await storedata()
	
	AllItems = [name for name in items[str(user.id)]]
	embed = nextcord.Embed(color=COLOR_EMBED)
	
	if len(AllItems) == data[str(user.id)]["Limit-Items"] and name not in items[str(user.id)]:
		embed.description = f"**Sorry the bag is full. Use items 1 to save space**"
		embed.set_author(name=f"Stuff bag | {user.display_name}")
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await interaction.response.send_message(embed=embed, ephemeral=ep)
		return
	
	if store[str(name)]["amount"] == 0:
		embed.description = f"**Sorry {interaction.user.mention}\nThis product is sold out in store**"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await interaction.response.send_message(embed=embed, ephemeral=ep)
		return
		
	if data[str(interaction.user.id)]["DP"] < store[str(name)]["price"]:
		embed.title = "Sorry you can't buy this item"
		embed.description = f"**Your DP: {EMOJI['DP']} `{data[str(user.id)]['DP']:,}`\nPrice this Item: {EMOJI['DP']} `{store[str(name)]['price']:,}`**"
		embed.set_thumbnail(url=IMAGE_LINK['no'])
		
		await interaction.response.send_message(embed=embed, ephemeral=ep)
	else:
		if str(user.id) not in items:
			items[str(user.id)] = {}
			
		if name in items[str(user.id)]:
			items[str(user.id)][name]["amount"] += 1
			store[str(name)]["amount"] -= 1
			data[str(user.id)]["DP"] -= store[str(name)]["price"]
			
			with open("./data/usersdata.json", "w") as d:
				json.dump(data, d, indent=2)
			with open("./data/store.json", "w") as s:
				json.dump(store, s, indent=2)
			with open("./data/useritems.json", "w") as i:
				json.dump(items, i, indent=2)
			embed.title = f"**{name}**"
			embed.description = f"**Product owner: {user.mention}\nOwns now: `{items[str(user.id)][name]['amount']}`\nProduct price: {EMOJI['DP']} `{store[name]['price']:,}`**"
			embed.set_thumbnail(url=store[name]["icon"])
			embed.set_author(name="Done successfully", icon_url=IMAGE_LINK["ok"])
			await interaction.response.send_message(embed=embed, ephemeral=ep)
		else:
			icon = store[name]["icon"]
			desc = store[name]["desc"]
			
			if str(user.id) not in items:
				items[str(user.id)] = {}
			items[str(user.id)][name] = {}
			items[str(user.id)][name]["icon"] = icon
			items[str(user.id)][name]["desc"] = desc
			items[str(user.id)][name]["amount"] = 1
			store[str(name)]["amount"] -= 1
			data[str(user.id)]["DP"] -= store[str(name)]["price"]
			
			with open("./data/usersdata.json", "w") as d:
				json.dump(data, d, indent=2)
			with open("./data/store.json", "w") as s:
				json.dump(store, s, indent=2)
			with open("./data/useritems.json", "w") as i:
				json.dump(items, i, indent=2)
			embed.title = f"**{name}**"
			embed.description = f"**Product owner: {user.mention}\nOwns now: `{items[str(user.id)][name]['amount']}`\nProduct price: {EMOJI['DP']} `{store[name]['price']:,}`**"
			embed.set_thumbnail(url=store[name]["icon"])
			embed.set_author(name="Done successfully", icon_url=IMAGE_LINK["ok"])
			await interaction.response.send_message(embed=embed, ephemeral=ep)


#Func Show users items
async def users_items_show(interaction: Interaction, user: nextcord.Member==None):
	
	if user == None:
		user = interaction.user
	
	ItemsUsers = await useritems()
	user_data = await userdata()
	embed = nextcord.Embed(color=COLOR_EMBED)
	
	get_user_items = ItemsUsers[str(user.id)]
	
	if str(user.id) not in ItemsUsers:
		embed.description = f"**Sorry i can't find items from {user.mention} data**"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif str(user.id) not in user_data:
		embed.title = "**Sorry, We have something wrong**"
		embed.description = f"**\nAccount {user.mention} its not verified\nrun slash command: `/verifie` **"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	list_embeds = []
	for items in get_user_items:
		embed = nextcord.Embed(color=COLOR_EMBED)
		embed.title = f"**{items}**"
		embed.description = f"**\nQuantity owned: `{get_user_items[items]['amount']}`**"
		embed.add_field(name="**Description**", value=f">>> ```{get_user_items[items]['desc']}```")
		embed.set_thumbnail(url=get_user_items[items]["icon"])
		embed.set_author(name=f"Storage bag | {user.display_name}", icon_url="https://cdn.discordapp.com/emojis/695306067327844415.png")
		embed.set_footer(text=f"Quantity of items: {len([name for name in get_user_items])} | By: {NAME}", icon_url=user.avatar.url)
		list_embeds.append(embed)
	
	
	if len(list_embeds) > 1:
		msg = await interaction.response.send_message(f"{interaction.user.mention}", embed=list_embeds[0], ephemeral=True)
		await msg.edit(view = ButtonPage(embeds=list_embeds, msg=msg))
	elif len(list_embeds) == 1:
		await interaction.response.send_message(f"{interaction.user.mention}", embed=embed,ephemeral=True)
	else:
		await interaction.response.send_message("**Sorry i can't find items in the data <:Think:1196170601023406126> **",ephemeral=True)

	
#Func use items
async def ItemsUse(interaction: Interaction, name, user: nextcord.Member==None):
	
	Items = await useritems()
	data = await userdata()
	store = await storedata()
	embed = Embed(color=COLOR_EMBED)
	author = interaction.user
	if user and str(user.id) not in data:
		embed.description = f"**Sorry about this but account {user.mention} its not verified**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed)
		return
		
	if name == "Box-randoms":
		cooldwon = await CheckCooldwonItems(item=name, user=author)
		if cooldwon == True:
			await Box_randoms(interaction=interaction, user=user)
		else:
			time_end = await GetCooldwonItem(item=name, user=author)
			embed.description = f"**This item has a reuse timer\nThe remaining time: {EMOJI['time']} `{time_end}`**"
			embed.set_thumbnail(url=store[name]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed)
	elif name == "Health-evolution":
		cooldwon = await CheckCooldwonItems(item=name, user=author)
		if cooldwon == True:
			await Health_evolution(interaction=interaction, user=user)
		else:
			time_end = await GetCooldwonItem(item=name, user=author)
			embed.description = f"**This item has a reuse timer\nThe remaining time: {EMOJI['time']} `{time_end}`**"
			embed.set_thumbnail(url=store[name]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed)
	elif name == "Rare-gold":
		cooldwon = await CheckCooldwonItems(item=name, user=author)
		if cooldwon == True:
			await Rare_gold(interaction=interaction, user=user)
		else:
			time_end = await GetCooldwonItem(item=name, user=author)
			embed.description = f"**This item has a reuse timer\nThe remaining time: {EMOJI['time']} `{time_end}`**"
			embed.set_thumbnail(url=store[name]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed)
	elif name == "Chocolate-era":
		await Chocolate_era(interaction=interaction, user=user)
	elif name == "Sushi-plate":
		await Sushi_plate(interaction=interaction, user=user)
	elif name == "Energy-shield":
		await Energy_shield(interaction=interaction, user=user)
	elif name == "Bottle-scam":
		await Bottle_scam(interaction=interaction, user=user)
	elif name == "Super-sword":
		await Super_sword(interaction=interaction, user=user)
	elif name == "Rescue-bottle":
		await Rescue_bottle(interaction=interaction, user=user)
	elif name == "Deadly-missile":
		await Deadly_missile(interaction=interaction, user=user)
	elif name == "Super-Ticket":
		await Super_Ticket(interaction=interaction, user=user)
	elif name == "Energy-monster":
		await Energy_monster(interaction=interaction, user=user)
	elif name == "Ash-Blossom-card":
		cooldwon = await CheckCooldwonItems(item=name, user=author)
		if cooldwon == True:
			await Ash_Blossom_card(interaction=interaction, user=user)
		else:
			time_end = await GetCooldwonItem(item=name, user=author)
			embed.description = f"**This item has a reuse timer\nThe remaining time: {EMOJI['time']} `{time_end}`**"
			embed.set_thumbnail(url=store[name]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed)
	elif name == "Ash-Bombe":
		await Ash_Bombe(interaction=interaction, user=user)
	elif name == "Destruction-gun":
		await Destruction_gun(interaction=interaction, user=user)
	elif name == "Golden-gun":
		await Golden_gun(interaction=interaction, user=user)
	elif name == "Blue-flame-dragon":
		await Blue_flame_dragon(interaction=interaction, user=user)
	elif name == "Evolution-of-the-bag":
		await Evolution_of_the_bag(interaction=interaction, user=user)
	elif name == "Star-background":
		await Star_background(interaction=interaction, user=user)
	elif name == "Amulet-Description":
		await Amulet_Description(interaction=interaction, user=user)
	elif name == "":
		pass
	#elif name == "Amulet-of-titles":
#		await Amulet_of_titles(interaction=interaction, user=user)
#	else:
#		await interaction.response.send_message(f"**`{name}`\nnot in data sorry**")