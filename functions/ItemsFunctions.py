import nextcord
from nextcord import Interaction, ButtonStyle, Embed
import json
from config import COLOR_EMBED, NAME, EMOJI,  IMAGE_LINK
import random
from .Json_files import userdata, useritems, storedata
from .ModelsItems import Starbackground,AmuletDescription


#Func Items Box-randoms
async def Box_randoms(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	
	random_get = random.choice(["items", "DP"])
	embed = Embed(color=COLOR_EMBED)
	if user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	if "Box-randoms" in Items[str(author.id)]:
		if random_get == "DP":
			Won = random.randint(500, 800)
			if user:
				data[str(user.id)]["DP"] += Won
				embed.description= f"**{user.mention} won: {EMOJI['DP']} `{Won}`\nFrom: {author.mention}**"
			else:
				data[str(author.id)]["DP"] += Won
				embed.description= f"**You won: {EMOJI['DP']} `{Won}`**"
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.title = "Use - Box-randoms"
			embed.set_footer(text=f"Owner of the item: {interaction.user.display_name}")
			if Items[str(author.id)]["Box-randoms"]["amount"] == 1:
				del Items[str(author.id)]["Box-randoms"]
			else:
				Items[str(author.id)]["Box-randoms"]["amount"] -= 1
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			await interaction.response.send_message(embed=embed)
		else:
			list_name = []
			for names in store:
				list_name.append(names)
			
			Won = random.choice(list_name)
			icon = store[Won]["icon"]
			desc = store[Won]["desc"]
			if user:
				if Won in Items[str(user.id)]:
					Items[str(user.id)][Won]["amount"] += 1
				else:
					Items[str(user.id)][Won] = {}
					Items[str(user.id)][Won]["amount"] = 1
					Items[str(user.id)][Won]["desc"] = desc
					Items[str(user.id)][Won]["icon"] = icon
					
				with open("./data/useritems.json", "w") as f:
					json.dump(Items, f, indent=2)
			else:
				if Won in Items[str(author.id)]:
					Items[str(user.id)][Won]["amount"] += 1
				else:
					Items[str(author.id)][Won] = {}
					Items[str(author.id)][Won]["amount"] = 1
					Items[str(author.id)][Won]["desc"] = desc
					Items[str(author.id)][Won]["icon"] = icon
					
				with open("./data/useritems.json", "w") as f:
					json.dump(Items, f, indent=2)
				if user:
					embed.description = f"**{user.mention} won: {Won} Item**"
				else:
					embed.description = f"**You won: {Won} Item**"
				embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
				embed.title = "Use - Box-randoms"
				embed.set_footer(text=f"Owner of the item: {interaction.user.display_name}")
				embed.set_thumbnail(url=icon)
				
				if Items[str(author.id)]["Box-randoms"]["amount"] == 1:
					del Items[str(author.id)]["Box-randoms"]
				else:
					Items[str(author.id)]["Box-randoms"]["amount"] -= 1
				store[Won]["amount"] -= 1
				
				with open("./data/store.json", "w") as f:
					json.dump(store, f, indent=2)
				with open("./data/useritems.json", "w") as f:
					json.dump(Items, f, indent=2)
				await interaction.response.send_message(embed=embed)
	else:
			embed.description = "**Sorry you don't have this item**"
			embed.set_thumbnail(url=IMAGE_LINK["no"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
			
					
# Func item Health-evolution
async def Health_evolution(interaction: Interaction , user: nextcord.Member=None):
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	
	embed = Embed(color=COLOR_EMBED)	
	if "Health-evolution" in Items[str(author.id)]:
		if user != None:
			if str(user.id) not in data:
				embed.description = f"**Sorry, account {user.mention} is not  verifie**"
				embed.set_thumbnail(url=IMAGE_LINK["no"])
				await interaction.response.send_message(embed=embed, ephemeral=True)
				return
			elif data[str(user.id)]["Limit-LP"] == 500:
				embed.description = f"**Accept my apologies {author.mention}\nHealth level: {user.mention}\nIt has reached its limit**"
				embed.set_thumbnail(url=IMAGE_LINK["!"])
				embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
				await interaction.response.send_message(embed=embed)
				return
				
			data[str(user.id)]["Limit-LP"] += 20
			data[str(user.id)]["LP"] = data[str(user.id)]["Limit-LP"]
			if Items[str(author.id)]["Health-evolution"]["amount"] == 1:
				del Items[str(author.id)]["Health-evolution"]
			else:
				Items[str(author.id)]["Health-evolution"]["amount"] -= 1
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			embed.description = f"**New evolution LP: {user.mention}\nMaximum now: {EMOJI['LP']} `{data[str(user.id)]['Limit-LP']}` **"
			embed.title = "**Use - Health-evolution**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_footer(text=f"Owner of the item: {interaction.user.display_name}")
			embed.set_thumbnail(url=store["Health-evolution"]["icon"])
			await interaction.response.send_message(embed=embed)
		else:
			if data[str(author.id)]["Limit-LP"] == 500:
				embed.description = f"**Accept my apologies {author.mention}\nYour LP level\nIt has reached its limit**"
				embed.set_thumbnail(url=IMAGE_LINK["!"])
				embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
				await interaction.response.send_message(embed=embed)
				return
			data[str(author.id)]["Limit-LP"] += 20
			data[str(author.id)]["LP"] = data[str(author.id)]["Limit-LP"]
			if Items[str(author.id)]["Health-evolution"]["amount"] == 1:
				del Items[str(author.id)]["Health-evolution"]
			else:
				Items[str(author.id)]["Health-evolution"]["amount"] -= 1
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			embed.description = f"**You have a new evolution LP\n\nMaximum now: {EMOJI['LP']} `{data[str(author.id)]['Limit-LP']}` **"
			embed.title = "**Use - Health-evolution**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=store["Health-evolution"]["icon"])
			await interaction.response.send_message(embed=embed)
	else:
			embed.description = "**Sorry you don't have this item**"
			embed.set_thumbnail(url=IMAGE_LINK["no"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)

		
#Func item Rare-gold
async def Rare_gold(interaction: Interaction , user: nextcord.Member=None):
			
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	
	get_DP = random.randint(10000, 15000)
	embed = Embed(color=COLOR_EMBED)
	
	if "Rare-gold" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	if user:
		if user and str(user.id) not in data:
			embed.description = f"**Sorry account {user.mention} its not verifie**"
			embed.set_thumbnail(url=IMAGE_LINK["no"])
			await interaction.response.send_message(embed=embed)
			return
			
		data[str(user.id)]["DP"] += get_DP
		embed.title = "Use - Rare-gold"
		embed.description = f"**You've got it: {EMOJI['DP']} `{get_DP:,}`\nFrom: {author.mention}\n`Tell him thank you`**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=store["Rare-gold"]["icon"])
		
		if Items[str(author.id)]["Rare-gold"]["amount"] == 1:
			del Items[str(author.id)]["Rare-gold"]
		else:
			Items[str(author.id)]["Rare-gold"]["amount"] -= 1
		
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		await interaction.response.send_message(f"{user.mention}", embed=embed)
	else:
		data[str(author.id)]["DP"] += get_DP
		embed.title = "Use - Rare-gold"
		embed.description = f"**You've got it: {EMOJI['DP']} `{get_DP:,}`**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=store["Rare-gold"]["icon"])
		
		if Items[str(author.id)]["Rare-gold"]["amount"] == 1:
			del Items[str(author.id)]["Rare-gold"]
		else:
			Items[str(author.id)]["Rare-gold"]["amount"] -= 1
		
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		await interaction.response.send_message(embed=embed)


#Func item Chocolate-era
async def Chocolate_era(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if "Chocolate-era" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return

	if user:
		if str(user.id) not in data:
			embed.description = f"**Sorry account {user.mention} its not verifie**"
			embed.set_thumbnail(url=IMAGE_LINK["no"])
			await interaction.response.send_message(embed=embed)
			return
		if data[str(user.id)]["LP"] == data[str(user.id)]["Limit-LP"]:
			embed.description = f"**LP: {user.mention}\nActually: {EMOJI['LP']} `100%` complete**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
		else:
			data[str(user.id)]["LP"] += 20
			if Items[str(author.id)]["Chocolate-era"]["amount"] == 1:
				del Items[str(author.id)]["Chocolate-era"]
			else:
				Items[str(author.id)]["Chocolate-era"]["amount"] -= 1
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			embed.description = f"**Increase LP: {user.mention}\nAmount: {EMOJI['LP']} `20`\nFull LP: {EMOJI['LP']} `{data[str(user.id)]['LP']}`\nFrom: {author.mention}**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=store["Chocolate-era"]["icon"])
			await interaction.response.send_message(f"{user.mention}" ,embed=embed)
	else:
		if data[str(author.id)]["LP"] == data[str(author.id)]["Limit-LP"]:
			embed.description = f"**Your LP\nActually: {EMOJI['LP']} `100%` complete**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
		else:
			data[str(author.id)]["LP"] += 20
			if Items[str(author.id)]["Chocolate-era"]["amount"] == 1:
				del Items[str(author.id)]["Chocolate-era"]
			else:
				Items[str(author.id)]["Chocolate-era"]["amount"] -= 1
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			embed.description = f"**Increase LP\nAmount: {EMOJI['LP']} `20`\nFull health points: {EMOJI['LP']} `{data[str(author.id)]['LP']}`**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=store["Chocolate-era"]["icon"])
			await interaction.response.send_message(embed=embed)


#Func item Sushi-plate
async def Sushi_plate(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if "Sushi-plate" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	if user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	
	if user:
		if data[str(user.id)]["LP"] == data[str(user.id)]["Limit-LP"]:
			embed.description = f"**LP: {user.mention}\nActually: {EMOJI['LP']} `100%` complete**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
			return
			
		data[str(user.id)]["LP"] = data[str(user.id)]["Limit-LP"]
		if Items[str(author.id)]["Sushi-plate"]["amount"] == 1:
			del Items[str(author.id)]["Sushi-plate"]
		else:
			Items[str(author.id)]["Sushi-plate"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
			
		embed.description = f"**Increase LP: {user.mention}\nThe ratio: {EMOJI['LP']} `100%`\nFrom: {author.mention}**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.title = "**Use - Sushi-plate**"
		embed.set_thumbnail(url=store["Sushi-plate"]["icon"])
		await interaction.response.send_message(f"{user.mention}", embed=embed)
	else:
		if data[str(author.id)]["LP"] == data[str(author.id)]["Limit-LP"]:
			embed.description = f"**Your LP\nActually: {EMOJI['LP']} `100%` complete**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
			return
			
		data[str(author.id)]["LP"] = data[str(author.id)]["Limit-LP"]
		if Items[str(author.id)]["Sushi-plate"]["amount"] == 1:
			del Items[str(author.id)]["Sushi-plate"]
		else:
			Items[str(author.id)]["Sushi-plate"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
			
		embed.description = f"**Increase your LP \nThe ratio: {EMOJI['LP']} `100%`**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.title = "**Use - Sushi-plate**"
		embed.set_thumbnail(url=store["Sushi-plate"]["icon"])
		await interaction.response.send_message(embed=embed)


#Func item Energy-shield
async def Energy_shield(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if "Energy-shield" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	if user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif user:
		embed.description = f"**Sorry, but this item cannot be shared with another member\nif you want do that run `/buy` and select {user.mention}**"
		embed.title = f"**Hi {author.mention}**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	embed.description = f"**Item: `Energy-shield`\n>>> ```In fact, this item automatically reacts when items that reduce your HP are used on you```\nQuantity you have: `{Items[str(author.id)]['Energy-shield']['amount']}` **"
	embed.set_thumbnail(url=store["Energy-shield"]["icon"])
	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
	await interaction.response.send_message(f"Hi {author.mention}",embed=embed)
			

#Func item Bottle-scam
async def Bottle_scam(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif user == None or user == author:
		embed.description = f"**Wait, you can't use this on yourself. Do you want to reduce your LP points?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Bottle-scam"]["icon"])
		embed.title = f"**Use - Bottle-scam**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return	
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Bottle-scam" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Bottle-scam**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Bottle-scam"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(author.id)]["Bottle-scam"]["amount"] == 1:
			del Items[str(author.id)]["Bottle-scam"]
		else:
			Items[str(author.id)]["Bottle-scam"]["amount"] -= 1
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
		
	else:
		if data[str(user.id)]["LP"] < 50:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 50
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Bottel-scam`\nFrom: {author.mention}\nDamage: `50`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Bottle-scam"]["icon"])
		if Items[str(author.id)]["Bottle-scam"]["amount"] == 1:
			del Items[str(author.id)]["Bottle-scam"]
		else:
			Items[str(author.id)]["Bottle-scam"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/userdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


#Func item Super-sword
async def Super_sword(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
		
	elif user == None or user == author:
		embed.description = f"**Are you sure stabbing yourself in the sword is a good idea?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Super-sword"]["icon"])
		embed.title = f"**Use - Super-sword**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Super-sword" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Super-sword**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Bottle-scam"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Super-sword"]["amount"] == 1:
			del Items[str(author.id)]["Super-sword"]
		else:
			Items[str(author.id)]["Super-sword"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
		
	else:
		if data[str(user.id)]["LP"] < 40:
			 data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 40
		
		if Items[str(author.id)]["Super-sword"]["amount"] == 1:
			del Items[str(author.id)]["Super-sword"]
		else:
			Items[str(author.id)]["Super-sword"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Super-sword`\nFrom: {author.mention}\nDamage: `40`\nHealth points now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Super-sword"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


# Func item Rescue-bottle
async def Rescue_bottle(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif "Rescue-bottle" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	if user:
		if data[str(user.id)]["LP"] == data[str(user.id)]["Limit-LP"]:
			embed.description = f"**LP: {user.mention}\nActually: {EMOJI['LP']} `100%` complete**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
			return
		
		data[str(user.id)]["LP"] = data[str(user.id)]["Limit-LP"]
		if Items[str(author.id)]["Rescue-bottle"]["amount"] == 1:
			del Items[str(author.id)]["Rescue-bottle"]
		else:
			Items[str(author.id)]["Rescue-bottle"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
			
		embed.description = f"**Increase LP: {user.mention}\nThe ratio: {EMOJI['LP']} `100%`\nFrom: {author.mention}**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.title = "**Use - Rescue-bottle**"
		embed.set_thumbnail(url=store["Rescue-bottle"]["icon"])
		await interaction.response.send_message(f"{user.mention}", embed=embed)
	
	else:
			if data[str(author.id)]["LP"] == data[str(author.id)]["Limit-LP"]:
				embed.description = f"**Your LP Actually: {EMOJI['LP']} `100%` complete**"
				embed.set_thumbnail(url=IMAGE_LINK["!"])
				await interaction.response.send_message(embed=embed, ephemeral=True)
				return
			
			data[str(author.id)]["LP"] = data[str(author.id)]["Limit-LP"]
			if Items[str(author.id)]["Rescue-bottle"]["amount"] == 1:
				del Items[str(author.id)]["Rescue-bottle"]
			else:
				Items[str(author.id)]["Rescue-bottle"]["amount"] -= 1
			
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			
			embed.description = f"**Increase your LP\nThe ratio: {EMOJI['LP']} `100%`**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.title = "**Use - Rescue-bottle**"
			embed.set_thumbnail(url=store["Rescue-bottle"]["icon"])
			await interaction.response.send_message(embed=embed)


#Func item Deadly-missile
async def Deadly_missile(interaction: Interaction , user: nextcord.Member=None):
	
	author = interaction.user
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()

	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
		
	elif user == None or user == author:
		embed.description = f"**Wait a minute, are you going to fire a missile at yourself?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Deadly-missile"]["icon"])
		embed.title = f"**Use - Deadly-missile**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Deadly-missile" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Deadly-missiler**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Deadly-missile"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Deadly-missile"]["amount"] == 1:
			del Items[str(author.id)]["Deadly-missile"]
		else:
			Items[str(author.id)]["Deadly-missile"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
	
	else:
		if data[str(user.id)]["LP"] < 90:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 90
		if Items[str(author.id)]["Deadly-missile"]["amount"] == 1:
			del Items[str(author.id)]["Deadly-missile"]
		else:
			Items[str(author.id)]["Deadly-missile"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Deadly-missile`\nFrom: {author.mention}\nDamage: `90`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Deadly-missile"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


#Func Ticket-Super
async def Super_Ticket(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if user:
		embed.description = f"**Sorry, this item cannot be shared. To do this, please make a purchase and specify the desired user.\nfor do it run: `/buy`**"
		embed.set_thumbnail(url=store["Super-Ticket"]["icon"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif "Super-Ticket" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	embed.title = f"**Use - Super-Ticket**"
	embed.description = f"**To use this item, create a ticket\nRun slash command: `/tickets`**"
	embed.set_thumbnail(url=store["Super-Ticket"]["icon"])
	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
	
	await interaction.response.send_message(embed=embed, ephemeral=True)
	

async def Energy_monster(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	
	elif user == None or user == author:
		embed.description = f"**Wait a minute, are you going to make a monster unleash a huge wave of destructive energy on you?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Energy-monster"]["icon"])
		embed.title = f"**Use - Energy-monster**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Energy-monster" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Deadly-missiler**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Energy-monster"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Energy-monster"]["amount"] == 1:
			del Items[str(author.id)]["Energy-monstere"]
		else:
			Items[str(author.id)]["Energy-monster"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
	
	else:
		if data[str(user.id)]["LP"] < 200:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 200
		if Items[str(author.id)]["Energy-monster"]["amount"] == 1:
			del Items[str(author.id)]["Energy-monster"]
		else:
			Items[str(author.id)]["Energy-monster"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Energy-monster`\nFrom: {author.mention}\nDamage: `200`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Energy-monster"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


#Func Ash Blossom card
async def Ash_Blossom_card(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif "Ash-Blossom-card" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	if user:
		if "Energy-shield" in Items[str(user.id)]:
			Items[str(user.id)]["Energy-shield"]["amount"] += 4
		else:
			Items[str(user.id)]["Energy-shield"] = {}
			Items[str(user.id)]["Energy-shield"]["icon"] = store["Energy-shield"]["icon"]
			Items[str(user.id)]["Energy-shield"]["icon"] = store["Energy-shield"]["desc"]
			Items[str(user.id)]["Energy-shield"]["amount"] = 4
		
		DP = 1000
		LP = 100
		Warns = 0
		data[str(user.id)]["DP"] += 1000
		if data[str(user.id)]["LP"] == 500:
			LP = "Your LP actually is in fact at max"
		else:
			data[str(user.id)]["LP"] += LP
		if data[str(user.id)]["Warns"] == 0:
			Warns = "You actually not have a warns\nBecause of this, I was replaced with 2000 DP**"
			DP += 2000
		else:
			data[str(user.id)]["Warns"] = 0
		
	
		embed.title = f"**Used - Ash-Blossom-card**"
		embed.description = f">>> **You get: {EMOJI['DP']} `{DP}`\nLP: {EMOJI['LP']} `{LP}`\nRemove warns: `{Warns}`\n\nUsed by: {author.mention} **"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Ash-Blossom-card"]["icon"])
		
		if Items[str(author.id)]["Ash-Blossom-card"]["amount"]== 1:
			del Items[str(author.id)]["Ash-Blossom-card"]
		else:
			Items[str(author.id)]["Ash-Blossom-card"]["amount"] -= 1
		
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		await interaction.response.send_message(f"{user.mention}", embed=embed)
	
	else:
		
		if "Energy-shield" in Items[str(user.id)]:
			Items[str(user.id)]["Energy-shield"]["amount"] += 4
		else:
			Items[str(user.id)]["Energy-shield"] = {}
			Items[str(user.id)]["Energy-shield"]["icon"] = store["Energy-shield"]["icon"]
			Items[str(user.id)]["Energy-shield"]["icon"] = store["Energy-shield"]["icon"]
			Items[str(user.id)]["Energy-shield"]["amount"] = 4
			Items[str(user.id)]["Energy-shield"]["desc"] = store["Energy-shield"]["desc"]
		
		DP = 1000
		LP = 100
		Warns = 0
		data[str(user.id)]["DP"] += 1000
		if data[str(user.id)]["LP"] >= 500:
			LP = "Your LP actually is in fact at max"
		else:
			data[str(author.id)]["LP"] += LP
		if data[str(author.id)]["Warns"] == 0:
			Warns = "You actually not have a warns\nBecause of this, I was replaced with 2000 DP**"
			DP += 2000
		else:
			data[str(author.id)]["Warns"] = 0
		
	
		embed.title = f"**Used - Ash-Blossom-card**"
		embed.description = f">>> **You get: {EMOJI['DP']} `{DP}`\nLP: {EMOJI['LP']} `{LP}`\nRemove warns: `{Warns}`**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Ash-Blossom-card"]["icon"])
		
		if Items[str(author.id)]["Ash-Blossom-card"]["amount"]== 1:
			del Items[str(author.id)]["Ash-Blossom-card"]
		else:
			Items[str(author.id)]["Ash-Blossom-card"]["amount"] -= 1
		
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		await interaction.response.send_message(embed=embed)

#Func Ash-Bombe
async def Ash_Bombe(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	
	elif user == None or user == author:
		embed.description = f"**Wait a minute, are you going to bomb yourself like this?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Ash-Bombe"]["icon"])
		embed.title = f"**Use - Ash-Bombe**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Ash-Bombe" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Ash-Bombe**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Ash-Bombe"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Ash-Bombe"]["amount"] == 1:
			del Items[str(author.id)]["Ash-Bombe"]
		else:
			Items[str(author.id)]["Ash-Bombe"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
	
	else:
		if data[str(user.id)]["LP"] < 60:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 60
		if Items[str(author.id)]["Ash-Bombe"]["amount"] == 1:
			del Items[str(author.id)]["Ash-Bombe"]
		else:
			Items[str(author.id)]["Ash-Bombe"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Ash-Bombe`\nFrom: {author.mention}\nDamage: `60`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Ash-Bombe"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)

#Func Blue-flame-dragon
async def Blue_flame_dragon(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	
	elif user == None or user == author:
		embed.description = f"**Take a moment, are you going to use the dragon to burn yourself with its blazing blue fire?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Blue-flame-dragon"]["icon"])
		embed.title = f"**Use - Blue-flame-dragon**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Blue-flame-dragon" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Blue-flame-dragon**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Blue-flame-dragon"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Blue-flame-dragon"]["amount"] == 1:
			del Items[str(author.id)]["Blue-flame-dragon"]
		else:
			Items[str(author.id)]["Blue-flame-dragon"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
	
	else:
		if data[str(user.id)]["LP"] < 150:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 150
		if Items[str(author.id)]["Blue-flame-dragon"]["amount"] == 1:
			del Items[str(author.id)]["Blue-flame-dragon"]
		else:
			Items[str(author.id)]["Blue-flame-dragon"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Blue-flame-dragon`\nFrom: {author.mention}\nDamage: `150`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Blue-flame-dragon"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


#Func Golden-gun
async def Golden_gun(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	
	elif user == None or user == author:
		embed.description = f"**Wait a minute, are you going to shoot yourself?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Golden-gun"]["icon"])
		embed.title = f"**Use - Golden-gun**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Golden-gun" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Golden-gun**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Golden-gun"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Golden-gun"]["amount"] == 1:
			del Items[str(author.id)]["Golden-gun"]
		else:
			Items[str(author.id)]["Golden-gun"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
	
	else:
		if data[str(user.id)]["LP"] < 100:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 100
		if Items[str(author.id)]["Golden-gun"]["amount"] == 1:
			del Items[str(author.id)]["Golden-gun"]
		else:
			Items[str(author.id)]["Golden-gun"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Golden-gun`\nFrom: {author.mention}\nDamage: `100`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Golden-gun"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


#Func Destruction-gun
async def Destruction_gun(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if data[str(author.id)]["LP"] == 0:
		embed.description = f"**Your LP is: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, you are frozen, you cannot attack anyone**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	
	elif user == None or user == author:
		embed.description = f"**Wait a minute, are you going to shoot yourself?\nSelect a member**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=store["Destruction-gun"]["icon"])
		embed.title = f"**Use - Destruction-gun**"
		embed.set_image(url=random.choice(IMAGE_LINK["what"]))
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	elif data[str(user.id)]["LP"] == 0:
		embed.description = f"**LP: {user.mention}\nIs: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.title = f"**Sorry, this user is frozen**"
		embed.set_thumbnail(url=IMAGE_LINK["frosty"])
		embed.set_author(name=author.display_name, icon_url=author.avatar.url)
		await interaction.response.send_message(embed=embed)
		return
	elif "Destruction-gun" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
		
	if "Energy-shield" in Items[str(user.id)]:
		embed.title = f"**Use - Destruction-gun**"
		embed.description = f"**Your attack is automatically stopped\nBecause {user.mention} owns: `Energy-shield` **"
		embed.set_author(name=f"{user.display_name} used automatically", icon_url=store["Energy-shield"]["icon"])
		embed.set_thumbnail(url=store["Destruction-gun"]["icon"])
		embed.set_image(url="https://cdn.discordapp.com/attachments/1194248995321688135/1194249231704277043/energy_shield.jpg")
		
		if Items[str(user.id)]["Energy-shield"]["amount"] == 1:
			del Items[str(user.id)]["Energy-shield"]
		else:
			Items[str(user.id)]["Energy-shield"]["amount"] -= 1
		
		if Items[str(author.id)]["Destruction-gun"]["amount"] == 1:
			del Items[str(author.id)]["Destruction-gun"]
		else:
			Items[str(author.id)]["Destruction-gun"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		
		await interaction.response.send_message(embed=embed)
	
	else:
		if data[str(user.id)]["LP"] < 200:
			data[str(user.id)]["LP"] = 0
		else:
			data[str(user.id)]["LP"] -= 200
		if Items[str(author.id)]["Destruction-gun"]["amount"] == 1:
			del Items[str(author.id)]["Destruction-gun"]
		else:
			Items[str(author.id)]["Destruction-gun"]["amount"] -= 1
		with open("./data/useritems.json", "w") as f:
			json.dump(Items, f, indent=2)
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		embed.title = f"**You have received damage**"
		embed.description = f"**The item used: `Destruction-gun`\nFrom: {author.mention}\nDamage: `200`\nYour LP now: {EMOJI['LP']} `{data[str(user.id)]['LP']}`**"
		embed.set_thumbnail(url=store["Destruction-gun"]["icon"])
		
		await interaction.response.send_message(f"**Hi {user.mention}**", embed=embed)


#Func Evolution-of-the-bag
async def Evolution_of_the_bag(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if "Evolution-of-the-bag" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user and str(user.id) not in data:
		embed.description = f"**Sorry account {user.mention} its not verifie**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed)
		return
	
	if user:
		if data[str(user.id)]["Limit-Items"] == 15:
			embed.description = f"**Sorry, you cannot upgrade this user's storage bag. Because it has reached its limit**"
			embed.set_thumbnail(url=store["Evolution-of-the-bag"]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed)
		else:
			data[str(user.id)]["Limit-Items"] += 1
			if Items[str(author.id)]["Evolution-of-the-bag"]["amount"] == 1:
				del Items[str(author.id)]["Evolution-of-the-bag"]
			else:
				Items[str(author.id)]["Evolution-of-the-bag"]["amount"] -= 1
			
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			
			embed.title = "**The storage bag has been successfully developed**"
			embed.description = f"**By: {author.mention}\nTo: {user.mention}\nMaximum now: {data[str(user.id)]['Limit-Items']}**"
			embed.set_thumbnail(url=store["Evolution-of-the-bag"]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			
			await interaction.response.send_message(f"{user.mention}", embed=embed)
	
	else:
		if data[str(author.id)]["Limit-Items"] == 15:
			embed.description = f"**Sorry, your storage bag has reached its limit**"
			embed.set_thumbnail(url=store["Evolution-of-the-bag"]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed)
		else:
			data[str(author.id)]["Limit-Items"] += 1
			if Items[str(author.id)]["Evolution-of-the-bag"]["amount"] == 1:
				del Items[str(author.id)]["Evolution-of-the-bag"]
			else:
				Items[str(author.id)]["Evolution-of-the-bag"]["amount"] -= 1
			
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			
			embed.title = "**The storage bag has been successfully developed**"
			embed.description = f"**Maximum now: {data[str(author.id)]['Limit-Items']}**"
			embed.set_thumbnail(url=store["Evolution-of-the-bag"]["icon"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			
			await interaction.response.send_message(embed=embed)

#Func Star-background
async def Star_background(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if "Star-background" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user:
		embed.description = f"**Sorry, this item cannot be shared. To do this run: `/buy` and select this user if you want**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	await interaction.response.send_modal(Starbackground())

#Func Amulet-Description
async def Amulet_Description(interaction: Interaction , user: nextcord.Member=None):
	
	store = await storedata()
	Items = await useritems()
	data = await userdata()
	author = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if "Amulet-Description" not in Items[str(author.id)]:
		embed.description = "**Sorry you don't have this item**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif user:
		embed.description = f"**Sorry, this item cannot be shared. To do this run: `/buy` and select this user if you want**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	await interaction.response.send_modal(AmuletDescription())

