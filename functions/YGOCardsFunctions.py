import requests
import json
from difflib import get_close_matches as gcm
from .YGODictIcons import icon
from .Json_files import cardsname
from urllib.parse import quote

async def Update():
    with open("./data/cards.json", "r") as r:
        data = json.load(r)
    
    api_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    cards = requests.get(api_url).json()["data"]
    for card in cards:
        if card["name"] in data["cards"]:
            continue
        else:
            data["cards"].append(card["name"])
   
            with open("./data/cards.json", "w") as d:
                json.dump(data, d, indent=2)

TheListName = cardsname()

class cards:
	def __init__(self, name):
		self.card = None
		self.masterdueldata = None
		self.cards_url = None
		self.name = gcm(name, TheListName, 98)[0]
	
	def Api(self):
		api_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
		
		p = {"name":self.name,"misc":"yes"}
		self.card = requests.get(api_url, params=p).json()["data"][0]
		
		self.masterdueldata = requests.get(f"https://www.masterduelmeta.com/api/v1/cards?name={quote(self.name)}").json()
		
		self.cards_url = self.card["ygoprodeck_url"]
		
	#card id
	def cards_id(self):
		id = self.masterdueldata[0]["konamiID"] if "konamiID" in self.masterdueldata[0] else self.card["id"]
		return id
		
	# cards description
	def desc(self):
		description = self.card["desc"]
		return description
			
	#get archetype
	def archetype(self):
		try:
			archetype = f"\n**Archetype:** {self.card['archetype']}"
		except:
			archetype = ""
		return archetype
		
	# Atk Def Scale
	def Atk_def_Level_Scale(self):
		
			
		if "Link" in self.masterdueldata[0]["monsterType"]:
				level = f"\n**Link:** {icon['level']['link']} {self.card['linkval']}"
				atk_def = f"\n**ATK:** {self.card['atk']}"
		elif "Xyz" in self.masterdueldata[0]["monsterType"]:
				atk_def = f"\n**ATK:** {self.card['atk']}/**DEF:**  {self.card['def']}"
				level = f"\n**Rank:** {icon['level']['rank']} {self.card['level']}"
		else:
				atk_def = f"\n**ATK:** {self.card['atk']}/**DEF:**  {self.card['def']}" if "Monster" in self.masterdueldata[0]["type"] else ""
				level = f"\n**LeveL:** {icon['level']['level']} {self.card['level']}" if "Monster" in self.masterdueldata[0]["type"] else ""
			
		scale = f" | **Scale:** {icon['scale']} {self.card['scale']}" if "Pendulum" in self.masterdueldata[0]["monsterType"] else ""
		AtkDefLevelScale = f"{level}{scale}{atk_def}"
		return AtkDefLevelScale
		
	# Type and race
	def Type_Race(self):
		mtype = " ".join(self.masterdueldata[0]['monsterType']).replace(' ', ' / ')
		if "Monster" in self.masterdueldata[0]["type"]:
				type = f"\n**Type:** {mtype} / {icon['race'][self.card['race']]}"
		elif "Spell" or "Trap" in self.masterdueldata[0]["type"]:
				type = f"\n**Type:** {icon['race'][self.card['race']]} {self.card['race']} {self.card['type'].replace('Card', '').strip()}"
		else:
				type = f"\n**Type:** {self.card['type']}"
			
		return type
		
	#Get Banlist 
	def Banlist(self):
			
		try:
			formats = self.card["misc_info"][0]["formats"]
			getbanlist = self.card["banlist_info"]  if "banlist_info" in self.card else ""
			ban_tcg = getbanlist["ban_tcg"] if "ban_tcg" in getbanlist else "Unlimited"
			ban_ocg = getbanlist["ban_ocg"] if "ban_ocg" in getbanlist else "Unlimited"
			if "TCG" or "OCG" in formats:
				banlist = f"**Limit:** TCG {icon['banlist'][ban_tcg]} | OCG {icon['banlist'][ban_ocg]}"
			else:
				banlist =""
		except:
			banlist = ""
		return banlist
		
	#Get Rarity
	def Raiity(self):
	      try:
	       	find_rarity = next((data["rarity"] for data in self.masterdueldata if "rarity" in data), None)
	      except:
	       	find_rarity = None
	       
	      rarity = f"\n**Rarity:** {icon['rarity'][find_rarity]}" if find_rarity != None else ""
	      return rarity
		
	#get icon
	def url_icon(self):
		if "Monster" in self.masterdueldata[0]["type"]:
				card_icon = f"{icon['icon_url'][self.card['attribute']]}"
		else:
				type = self.masterdueldata[0]["type"]
				card_icon = f"{icon['icon_url'][type]}"
		return card_icon
		
	# color cards for embed
	def color(self):
			
		if "Xyz" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0x081016
		elif "Normal" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0xdac332
		elif "Ritual" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0x3fc0fa
		elif "Synchro" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0xf2fafe
		elif "Link" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0x0046ea
		elif "Fusion" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0xa51ccd
		elif "Pendulum" in self.masterdueldata[0]["monsterType"]:
				color_cards = 0xaafdf1
		elif "Spell" in self.masterdueldata[0]["type"]:
				color_cards = 0x49c0aa
		elif "Trap" in self.masterdueldata[0]["type"]:
			color_cards = 0xb10076
		else:
				color_cards = 0xc56d00
		return color_cards
		
	#get cards images copy
	def CardsImage(self):
		try:
			img_art = f"https://images.ygoprodeck.com/images/cards_cropped/{self.masterdueldata[0]['konamiID'] if 'konamiID' in self.masterdueldata[0] else self.card['id']}.jpg"
		except:
			img_art = "https://cdn.discordapp.com/attachments/1166883204385480726/1176542222204796968/unknown.jpg"
		return img_art
		
	#Links
	def Links(self):
			
		metadeck = f"[Deck](https://ygoprodeck.com/deck-search/?&name={self.name.replace(' ', '%20')}&offset=0)"
		masterduel = f"[Master Duel](https://www.masterduelmeta.com/cards/{quote(self.name)})"
			
		links = f">>> **{metadeck}\n{masterduel}**"
		return links

