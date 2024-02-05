import json

#store data
async def storedata():
	with open('./data/store.json', "r") as f:
		data = json.load(f)
	return data

#oepn the json file user items
async def useritems():
	with open("./data/useritems.json", "r") as f:
		data = json.load(f)
	return data

#User data
async def userdata():
	with open("./data/usersdata.json", "r") as f:
		data = json.load(f)
	return data

#for open ticket data
async def TicketData():
	with open("./data/tickets.json", "r") as f:
		data = json.load(f)
	return data

#Get All Yugioh cards name
def cardsname():
    with open("./data/cards.json", "r") as f:
        data = json.load(f)
    cards = data["cards"]
    return cards

#Giveaways data open
async def giveawayData():
	with open("./data/giveaways.json", "r") as f:
		data = json.load(f)
	return data

async def DeckStore():
	with open("./data/deckstore.json", "r") as f:
		data = json.load(f)
	return data

#Cooldwon data get
async def Cooldwon():
	with open("./data/cooldwon.json", "r") as f:
		data = json.load(f)
	return data

#Cooldwon items
async def CooldwonItems():
	with open("./data/cooldwonitems.json", "r") as f:
		data = json.load(f)
	return data

async def YGONews():
	with open("./data/ygonews.json", "r") as f:
		data = json.load(f)
	return data


		