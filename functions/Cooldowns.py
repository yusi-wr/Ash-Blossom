import nextcord
import json
from datetime import datetime, timedelta
from .Json_files import Cooldwon, CooldwonItems


#---------(↓ Cooldwon commands ↓)---------

#Check and add cooldwon
async def CheckCooldwon(command:str, user: nextcord.Member):
	
	cooldwon = await Cooldwon()
	
	if command not in cooldwon:
		cooldwon[command] = {}
		with open("./data/cooldwon.json", "w") as f:
			json.dump(cooldwon, f, indent=2)
			
	if not str(user.id) in cooldwon[command]:
		cooldwon[command][str(user.id)] = {}
		cooldwon[command][str(user.id)]["date"] = str(datetime.utcnow())
		
		with open("./data/cooldwon.json", "w") as f:
			json.dump(cooldwon, f, indent=2)
		return True
	else:
		dateNow = cooldwon[command][str(user.id)]["date"]
		date = datetime.strptime(dateNow, "%Y-%m-%d %H:%M:%S.%f")
		diff = datetime.utcnow() - date
		
		if (diff.total_seconds() / 3600) >= 24:
			cooldwon[command][str(user.id)]["date"] = str(datetime.utcnow())
			with open("./data/cooldwon.json", "w") as f:
				json.dump(cooldwon, f, indent=2)
			return True
		else:
			return False

#Get users cooldwon
async def GetCooldwon(command: str, user: nextcord.Member):
	
	cooldwon = await Cooldwon()
	
	UserDate = cooldwon[command][str(user.id)]["date"]
	getdate = datetime.strptime(UserDate, "%Y-%m-%d %H:%M:%S.%f")
	diff = datetime.utcnow() - getdate
	date = str(timedelta(seconds=86400 - diff.total_seconds())).split(".")[0]
	
	return date


#---------(↓ Cooldwon Items ↓)---------

#Check and add cooldwon item
async def CheckCooldwonItems(item: str, user: nextcord.Member):
	
	cooldwon = await CooldwonItems()
	
	if item not in cooldwon:
		cooldwon[item] = {}
		with open("./data/cooldwonitems.json", "w") as f:
			json.dump(cooldwon, f, indent=2)
			
	if not str(user.id) in cooldwon[item]:
		cooldwon[item][str(user.id)] = {}
		cooldwon[item][str(user.id)]["date"] = str(datetime.utcnow())
		
		with open("./data/cooldwonitems.json", "w") as f:
			json.dump(cooldwon, f, indent=2)
		return True
	else:
		dateNow = cooldwon[item][str(user.id)]["date"]
		date = datetime.strptime(dateNow, "%Y-%m-%d %H:%M:%S.%f")
		diff = datetime.utcnow() - date
		
		if (diff.total_seconds() / 3600) >= 24:
			cooldwon[item][str(user.id)]["date"] = str(datetime.utcnow())
			with open("./data/cooldwonitems.json", "w") as f:
				json.dump(cooldwon, f, indent=2)
			return True
		else:
			return False

#Get cooldwon users
async def GetCooldwonItem(item: str, user: nextcord.Member):
	
	cooldwon = await CooldwonItems()
	
	UserDate = cooldwon[item][str(user.id)]["date"]
	getdate = datetime.strptime(UserDate, "%Y-%m-%d %H:%M:%S.%f")
	diff = datetime.utcnow() - getdate
	date = str(timedelta(seconds=86400 - diff.total_seconds())).split(".")[0]
	
	return date