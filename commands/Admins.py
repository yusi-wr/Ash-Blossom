import nextcord
from nextcord.ext import commands, tasks
from nextcord.abc import GuildChannel
from nextcord.ui import Button, View
from nextcord import Interaction, ButtonStyle
import os
import datetime
from humanfriendly import parse_timespan
import random
import json
import asyncio
from config import ADMIN_ROLE, COLOR_EMBED, IMAGE_LINK, NAME, EMOJI, welcome_role, owner
from functions.Json_files import userdata


class Admin(commands.Cog):
	"""Admins commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	COG_EMOJI = "<:ADMIN:1191514586596245594>"
	
	
	#command for add DP point to user
	@commands.command(name="addDP", description="Add DP point to users ", aliases=["adp", "DP"])
	@commands.guild_only()
	async def addDP(self, ctx:commands.Context, user: nextcord.Member, *,DP: int, reason: str="Non reason added"):
	   		
	   if ctx.author.id not in owner:
	   	await ctx.reply("**Sorry this command not for you**")
	   data = await userdata()
	   if str(user.id) not in data:
	   	await ctx.send(f"** Sorry the `{user.display_name}` account its not verified**")
	   	return
	   data[str(user.id)]["DP"] += DP
	   with open("./data/usersdata.json", "w") as f:
	   	json.dump(data, f, indent=2)
	   
	   embed = nextcord.Embed(color=COLOR_EMBED)
	   embed.description = f"**Add `{DP:,}`{EMOJI['DP']} to {user.mention} **"
	   embed.title = "**Done successfuly**"
	   embed.set_thumbnail(url=IMAGE_LINK['ok'])
	   embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
	   
	   await ctx.send(embed=embed)
	   
	   msgDirect = nextcord.Embed(title="**A new DP has been added to your account**", color=COLOR_EMBED,description=f"**DP: {EMOJI['DP']} `{DP}`\nFrom: {ctx.author.mention}\nReason: ```{reason}```**")
	   msgDirect.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
	   await user.send(embed=msgDirect)
	
	
	@commands.command(name="kick", description="kick a users")
	@commands.guild_only()
	@commands.has_any_role(ADMIN_ROLE)
	async def kick(self, ctx: commands.Context, member: nextcord.Member, *, reason=None):
		embed = nextcord.Embed(color=COLOR_EMBED)
		
		if reason == None:
			reason = "None reason....."
		if member == None:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I need you to mention a user for kick it\please mention @user**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
		elif ctx.author.top_role.position <= member.top_role.position:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I can't kick {member.mention}\nThe role is higher or equal to your role**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
			
		await member.kick(reason=reason)
		embed.title="**New user kicked !!**"
		embed.description=f">>> **The user: `{member.display_name}`\nFrom: {ctx.author.mention}\nReason: ```{reason}```**"
		embed.set_image(url=IMAGE_LINK['kick'])
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		await ctx.send(embed=embed)
	
	# ban command
	@commands.command(name="ban", description="ban user`s")
	@commands.guild_only()
	@commands.has_any_role(ADMIN_ROLE)
	async def ban(self, ctx, member: nextcord.Member, *,reason=None):
		embed = nextcord.Embed(color=COLOR_EMBED)
		
		if reason == None:
			reason = "None reason....."
		
		if member == None:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I need you to mention a user for ban it\please mention @user**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
		elif ctx.author.top_role.position <= member.top_role.position:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I can't ban {member.mention}\nThe role is higher or equal to your role**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
			
		await member.ban(reason=reason)
		embed.title="**New user banned !!**"
		embed.description=f"**The user: {member.mention} \nFrom: {ctx.author.mention}\nReason: ```{reason}```**"
		embed.set_thumbnail(url=IMAGE_LINK["baks"])
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		await ctx.send(embed=embed)
	
	# unban command
	@commands.command(name="unban", description="unban user`s from server bans")
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def unban(self, ctx, userID: int, *, reason: str=None):
		if reason == None:
			reason = "None reason....."
		
		user = nextcord.Object(id=userID)
		
		await ctx.guild.unban(user)
		embed = nextcord.Embed(title="**New user unbanned !!**",description=f"**The user: <@{user.id}> \nFrom: {ctx.author.mention}\nReason: ```{reason}```**", color=COLOR_EMBED)
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["icon"])
		
		await ctx.send(embed=embed)
	
	# command luck channel 
	@commands.command(name="lock", description="lock channel")
	@commands.guild_only()
	@commands.has_any_role(ADMIN_ROLE)
	async def lock(self, ctx: commands.Context, channel: nextcord.channel.TextChannel = None):
		if channel == None:
			channel = ctx.channel
		
		await channel.set_permissions(ctx.guild.default_role, send_messages=False)
		await channel.set_permissions(ctx.guild.get_role(welcome_role), send_messages=False)
		
		embed = nextcord.Embed(description=f"the channel {channel.mention} has been locked", color=COLOR_EMBED)
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["icon"])
		await ctx.send(embed=embed)
	
	# command unluck channel
	@commands.command(name="unlock", description="unlock channel")
	@commands.guild_only()
	@commands.has_any_role(ADMIN_ROLE)
	async def unlock(self, ctx, channel: nextcord.channel.TextChannel = None):
		if channel == None:
			channel = ctx.channel
		await channel.set_permissions(ctx.guild.default_role, send_messages=True)
		await channel.set_permissions(ctx.guild.get_role(welcome_role), send_messages=True)
		
		embed = nextcord.Embed(description=f"the channel {channel.mention} has been unlocked", color=COLOR_EMBED)
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["icon"])
		await ctx.send(embed=embed)
	
	# command clear message spams
	@commands.command(name="clear", description="Clear spam message")
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def clear(self, ctx, amount: int = None):
		if amount == None:
			amount = 100
		
		await ctx.channel.purge(limit=amount+1)
		embed = nextcord.Embed(description=f"**delete `{amount}` messages **", color=COLOR_EMBED)
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["icon"])
		send = await ctx.send(embed=embed)
		await asyncio.sleep(2)
		await send.delete()
		
	# command add role or remove it form users
	@commands.command(name="role", descriotion="add or remove role form user`s ")
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def role(self, ctx, user: nextcord.Member, role: nextcord.Role, *, reason: str = None):
		if reason == None:
			reason = "None reason....."
		
		if role in user.roles:
			await user.remove_roles(role, reason=reason)
			embed = nextcord.Embed(title=f"**Remove role from {user.mention}**", color=COLOR_EMBED)
			embed.description = f">>> **The role: {role.mention}\nFrom: {ctx.author.mention}\nReason: ```{reason}```**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=IMAGE_LINK["icon"])
			await ctx.send(embed=embed)
			
		else:
			await user.add_roles(role, reason=reason)
			embed = nextcord.Embed(title=f"**New role added to {user.mention}**", color=COLOR_EMBED)
			embed.description = f">>> **The role: {role.mention}\nFrom: {ctx.author.mention}\nReason: ```{reason}```**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=IMAGE_LINK["icon"])
			await ctx.send(embed=embed)
		
	# warn command'
	@commands.command(name="warn", description="add warn to users")
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def warn(self, ctx, user: nextcord.Member=None, amount: int = None):
		embed = nextcord.Embed(color=COLOR_EMBED)
		
		data = await userdata()
			
		if amount == None:
			amount = 1
		
		if user == None:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I need you to mention a user for warning \please mention @user**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
		elif str(user.id) not in data:
			embed.title = f"**Something is wrong**"
			embed.description = f"**Account {user.mention} is not activated**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
		
		data[str(user.id)]["Warns"] += amount
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
			
		embed.title="**New warning added to your data**"
		embed.description = f">>> **: {amount}\nTotal: {EMOJI['Warn']} {data[str(user.id)]['Warns']}\n`---(to remove)---`\n Please run: `?pw` **"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["icon"])
		await ctx.send(f"{user.mention}", embed=embed)
					
	
	# mute command
	@commands.command(name="mute", description="mute member")
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def mute(self, ctx: commands.Context, user: nextcord.Member, *, reason: str = None):
			if reason == None:
				reason = "None reason....."
			
			guild = ctx.guild
			embed = nextcord.Embed(color=COLOR_EMBED)
			if ctx.author.top_role.position <= user.top_role.position:
				embed.title = f"**Something is wrong**"
				embed.description = f"**I can't mute {user.mention}\nThe role is higher or equal to your role**"
				embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
				embed.set_thumbnail(url=IMAGE_LINK["!"])
				await ctx.send(embed=embed)
				return
			try:
				MuteRole = nextcord.utils.get(guild.roles, name="Muted")
			except:
				MuteRole = await guild.create_role(name="Muted", reason="Role for give user muted")
				for channel in guild.text_channels:
					await channel.set_permissions(MuteRole, send_messages=False, speak=False, read_message_history=True)
			
			await user.add_roles(MuteRole)
			embed.title = f"**New user muted !!**"
			embed.description =f">>> **The user: {user.mention}\nFrom: {ctx.author.mention}\nReason: ```{reason}```**"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=IMAGE_LINK["icon"])
			await ctx.send(embed=embed)
			await user.send(f">>> You have been muted from: **{guild.name}**\nReason: ```{reason}```")
            
	
	# unmute command
	@commands.command(name="unmute", description="unmute member")
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def unmute(self, ctx: commands.Context, user: nextcord.Member, *,reason: str = None):
			if reason == None:
				reason = "None reason....."
			
			guild = ctx.guild
			embed = nextcord.Embed(color=COLOR_EMBED)
			MuteRole = nextcord.utils.get(guild.roles, name="Muted")
			
			await user.remove_roles(MuteRole)
			embed.title = f"**User unmuted :D**"
			embed.description =f">>> **The user: {user.mention}\nFrom: {ctx.author.mention}\nReason: ```{reason}``` **"
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.set_thumbnail(url=IMAGE_LINK["icon"])
			await ctx.send(embed=embed)


	#command timeout
	@commands.command(name="timeout", aliases=["tout"])
	@commands.guild_only()
	@commands.has_role(ADMIN_ROLE)
	async def timeout(self, ctx: commands.Context, member: nextcord.Member, time, *, reason: str=None):
		if reason == None:
			reason = "None reason....."
		
		embed = nextcord.Embed(color=COLOR_EMBED)
		if member == None:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I need you to mention a user for give timeout\please mention @user**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
		elif ctx.author.top_role.position <= member.top_role.position:
			embed.title = f"**Something is wrong**"
			embed.description = f"**I can't give {member.mention} timeout\nThe role is higher or equal to your role**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await ctx.send(embed=embed)
			return
			
		times = parse_timespan(time)
		timeout = nextcord.utils.utcnow()+datetime.timedelta(seconds=times)
		await member.edit(timeout=timeout)
		embed.title = f"**timeout to {member.mention}**"
		embed.description = f"**Ends in: <t:{int(timeout)}:R>\nFrom: {ctx.author.mention}\nReason: {reason}**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["icon"])
		
		await ctx.send(f"{member.mention}", embed=embed)
		


def setup(bot):
	bot.add_cog(Admin(bot))
