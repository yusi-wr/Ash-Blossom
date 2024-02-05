from dotenv import load_dotenv
import os
import json

load_dotenv() #load dotenv: pip install python-dotenv

TOKEN = os.getenv("TOKEN") # add you bot key in .env file

#server name or samthing you want
NAME = "Ash Blossom™"

#leader role its admin
ADMIN_ROLE = 1093947368828846231

#owner bot id
owner = [1037701642356805723, 1129456838748942387]

# your guild id 
guildID = 1093889894377590804

#Level channel
channel_level = 1093914110850248714

#channel id ygorgain news
ygo_news = 1096430967708729394

#role welcome 
welcome_role = 1093976150063185970

#Ticket role id 
Ticket_id = 1093975732331491439

#Guilds id for slash command
GUILD_ID = [1176882321304072292, 1093889894377590804]

#code color for embeds
COLOR_EMBED = 0xff1289

#Roles id for ygo game role
YGORoles = {
    "EDOPro": "1134960979743096832",
    "YGOOmega": "1134961080876142652",
    "Duellink": "1134961611803742289",
    "MasterDuel": "1134961743974645871",
    "DuelBook": "1134961494535180358",
    "DuelNexus": "1134961269099741245"
}

#Link images 
IMAGE_LINK = {
  "kick": "https://cdn.discordapp.com/attachments/1180266906314346677/1183761498502348860/Picsart_23-12-11_13-16-44-496.png",
  
  "baks": "https://cdn.discordapp.com/attachments/1180266906314346677/1183761531897393233/Picsart_23-12-11_13-23-59-903.png",
  
  "no": "https://cdn.discordapp.com/attachments/1180266906314346677/1185547631586451536/Picsart_23-12-16_09-37-57-899.png",
  
  "ok": "https://cdn.discordapp.com/attachments/1180266906314346677/1185547518159892530/Picsart_23-12-16_09-35-46-990.png",
  
  "add": "https://cdn.discordapp.com/attachments/1180266906314346677/1183757450936057856/Picsart_23-12-11_12-29-42-590.png",
  
  "line": "https://cdn.discordapp.com/attachments/1180266906314346677/1181241158865797160/Picsart_23-12-04_14-27-09-677.png", 
  
  "remove": "https://cdn.discordapp.com/attachments/1180266906314346677/1183757424952356884/Picsart_23-12-11_12-27-57-304.png",
  
  "welcome": "https://cdn.discordapp.com/attachments/1180266906314346677/1180875999114706944/Picsart_23-12-03_14-16-44-637.png",
  
  "icon": "https://cdn.discordapp.com/attachments/1131256995450716293/1135128313812238377/Picsart_23-07-30_08-28-54-681.png",
  
  "bot-icon": "https://cdn.discordapp.com/attachments/1131256995450716293/1135128370779258981/Picsart_23-07-29_21-49-16-003.png",
  
  "!": "https://cdn.discordapp.com/attachments/1180266906314346677/1185547458160373820/Picsart_23-12-16_09-43-27-780.png",
  
  "profile": "https://cdn.discordapp.com/attachments/1180266906314346677/1187452925438603284/Picsart_23-12-21_17-53-43-944.png",
  
  "image-help": "https://cdn.discordapp.com/attachments/1180266906314346677/1191373170805055518/Picsart_24-01-01_13-28-41-912.png",
  "image-help2": "https://cdn.discordapp.com/attachments/1180266906314346677/1191373203285741588/Picsart_24-01-01_13-31-07-317.png",
  
  "download": "https://cdn.discordapp.com/attachments/1180266906314346677/1180266990611476551/Picsart_23-12-01_21-58-30-155.png",
  
  "ygo-role": "https://cdn.discordapp.com/attachments/1180266906314346677/1180266959485554818/Picsart_23-12-01_21-51-23-822.png",
  
  "frosty": "https://cdn.discordapp.com/emojis/1161895013697978438.png",
  
  "what": ["https://cdn.discordapp.com/attachments/1194248995321688135/1194249277761921095/77cab68227171eb7903d30e9e79de1cc.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1194249302051127406/A_beginners_guide_to_watching_anime_1676364465623_1676364465839_1676364465839.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1194249319474282547/kill_me_baby-04-yasuna-assassins-dopplegangers-confused-idiots-cute.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1201592756045365259/0_TtTELqHDT42odSvL.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1201592764425572542/202aabfd2c210c7f5d76ff42aa0ef1a7.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1201592775142035566/images.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1201592787511025814/download.jpg", "https://cdn.discordapp.com/attachments/1194248995321688135/1201592804015616000/you-know-its-awkward-when-a-side-character-and-antagonist-v0-qbtcxdpoyla81.png"],
  
  "ygorole-icon": "https://cdn.discordapp.com/attachments/1180266906314346677/1200342368491151390/Picsart_24-01-26_07-31-07-022.png"
  
}

#dic for emoji you can replace it to file json if you want
EMOJI = {
 "verified": "<a:Verified:1186618427218075699>",
 "DP": "<:DP:1198246332830335018>",
 "Lv": "<:Lv:1198246493220515951>",
 "Duel": "<:Duels:1198251092794949672>",
 "Rep": "<:Rep:1198247019530158221>",
 "Warn": "<:Warns:1198250910682464409>",
 "XP": "<:XP:1198246622648356924>",
 "LP": "<:LP:1198246783948689468>",
 "Tournament": "<:Tournaments:1198247176950796408>",
 "items": "<:backpack5:1196125848403718175>",
 "time": "<:time:1183525262713958532>"
}

#dict giveaway emojis
GEmoji = {
     "Hosted": "<:author:1144779924914327632>",
     "time": "<a:duration:1144779375187873937>",
     "giveaway": "<a:giveaway:1199084656168022017>",
     "for-title": "<:Givemanager:1144793157813407764>",
     "winners": "<:DA_Winner:1199085340154151037>",
     "Congrats": "<a:giveaways:1144792601443188756>"
}