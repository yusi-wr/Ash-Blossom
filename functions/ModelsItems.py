from nextcord import Embed, Interaction
from nextcord.ext import commands
from nextcord.ui import Modal, TextInput
import nextcord
import json
from .Json_files import userdata, useritems, storedata
from config import NAME, COLOR_EMBED, IMAGE_LINK


class Starbackground(Modal):
	def __init__(self):
		super().__init__(title="Add icon in your profile", timeout=None)
		
		self.icon = TextInput(
		      label="icon url",
		      placeholder="paste the image link here",
		      min_length=2,
		      max_length=100,
		      required=True,
		      #style=nextcord.TextInputStyle.paragraph
		)
		self.add_item(self.icon)
	
	async def callback(self, interacton: Interaction):
		
		data = await userdata()
		Items = await useritems()
		store = await storedata()
		embed = Embed(color=COLOR_EMBED)
		user = interacton.user
		
		if self.icon.value.endswith((".png", ".jpg")):
			data[str(user.id)]["icon"] = self.icon.value
			
			if Items[str(user.id)]["Star-background"]["amount"]  == 1:
				del Items[str(user.id)]["Star-background"]
			else:
				Items[str(user.id)]["Star-background"]["amount"] -= 1
			embed.description = "**Your icon profile has been added\run: `?pro` for show your profile**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=store["Star-background"]["icon"])
			
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			
			await interacton.response.send_message(embed=embed)
		
		else:
			await interacton.response.send_message("**Please add your url image - icon \nend `.png` or .`jpg` non link dwonload or other**", ephemeral=True)


class AmuletDescription(Modal):
	def __init__(self):
		super().__init__(title="Add your descrption in profile", timeout=None)
		
		self.description = TextInput(
		      label="The description",
		      placeholder="your descripton text",
		      min_length=5,
		      max_length=100,
		      required=True,
		      style=nextcord.TextInputStyle.paragraph
		)
		self.add_item(self.description)
	
	async def callback(self, interacton: Interaction):
		
		data = await userdata()
		Items = await useritems()
		store = await storedata()
		embed = Embed(color=COLOR_EMBED)
		user = interacton.user
		
		if self.description.value != "":
			data[str(user.id)]["desc"] = self.description.value
			if Items[str(user.id)]["Amulet-Description"]["amount"] == 1:
				del Items[str(user.id)]["Amulet-Description"]
			else:
				Items[str(user.id)]["Amulet-Description"]["amount"] -= 1
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
			with open("./data/useritems.json", "w") as f:
				json.dump(Items, f, indent=2)
			
			embed.description =f"**Your desc has been added\nDescription:\n>>> ```{self.description.value}```**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=store["Amulet-Description"]["icon"])
			
			await interacton.response.send_message(embed=embed)
		else:
			await interacton.response.send_message("**Please add your text description**")

