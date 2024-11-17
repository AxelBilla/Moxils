#https://discord.com/oauth2/authorize?client_id=1307728119397879912

import os
import discord
import typing
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from random import randint
from private.config import token
from datetime import datetime

owner_id=1242535080866349226
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents, owner_id = owner_id)
dir = os.path.dirname(__file__)

def addPath(ctx):
    path = dir+"/serverData/" + str(ctx.guild.id)
    if not os.path.exists(path):
        os.makedirs(path)
        file = open(path+"/settings.txt", "w", encoding='utf-8')
        word=["[ACCESS]: admin\n"]
        file.writelines(word)
        file.close()
        fileLog = open(path+"/logs.txt", "w", encoding='utf-8')
        word=[f"------------------------------------------------------------\n\n\n                    [SERVER LOGS]\n\n[ID]: {ctx.guild.id} | [NAME]: {ctx.guild.name}\n\n\n"]
        fileLog.writelines(word)
        fileLog.close()

def logging(guild, event: str, time):
    path = dir+"/serverData/" + str(guild)
    file = open(path + "/" + "logs.txt", "a", encoding='utf-8')
    file.write(f"{time}{event}\n")
    file.close()

@bot.event
async def owner_admin(ctx): #Allows me to debug stuff at will.
    addPath(ctx)
    e=f"{ctx.user.name} is trying to access a reserved ADMIN command.\n[ID]: {ctx.user.id}"
    async def predicate(ctx, e):
        logDate="------------------------------------------------------------\n\n["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]: "
        if ctx.user.guild_permissions.administrator == True:
            e=e+" - { They have administrator permissions. }"
            logging(ctx.guild.id, e, logDate)
            return True
        else:
            if ctx.user.id == owner_id:
                e=e+" - { They're this bot's owner.}"
                logging(ctx.guild.id, e, logDate)
                return True
            else:
                e=e+" - { They do not have an allowed role nor are they this bot's owner. }"
                logging(ctx.guild.id, e, logDate)
                await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)
                raise MissingPermissions(missing_permissions=['administrator'])
    a=await predicate(ctx, e)
    return app_commands.check(a) 

@bot.event
async def allowedRoleCheck(ctx): #Allows me to debug stuff at will.
    e=f"{ctx.user.name} is trying to access a reserved command.\n[ID]: {ctx.user.id}"
    addPath(ctx)
    async def predicate(ctx, e):
        file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "settings.txt", "r", encoding='utf-8')
        wordList=file.readlines()
        file.close()
        if len(wordList)==0:
            roleName="admin"
        else:
            roleName=wordList[0].strip("\n")
            roleName=roleName.replace("[ACCESS]: ", "")
        allowedRole = discord.utils.find(lambda r: r.name == roleName, ctx.guild.roles)
        if allowedRole in ctx.user.roles or ctx.user.guild_permissions.administrator == True:
            e=e+(" - { They have an allowed role. }\n\n\n")
            return True
        else:
            if ctx.user.id == owner_id:
                e=e+(" - { They're this bot's owner. }\n\n\n")
                return True
            else:
                e=e+(" - { They do not have an allowed role nor are they this bot's owner }\n\n\n")
                await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)
                raise MissingPermissions(missing_permissions=['administrator'])
    a=await predicate(ctx, e)
    logDate="------------------------------------------------------------\n\n["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]: "
    logging(ctx.guild.id, e, logDate)
    return app_commands.check(a) 





##########################################################
##                                                      ##
##                                                      ##
##                       AUTORUN                        ##
##                                                      ##
##                                                      ##
##########################################################

@bot.event
async def on_raw_reaction_add(payload):
    path = dir+"/serverData/" + str(payload.guild_id)
    file = open(path + "/" + "settings.txt", "r", encoding='utf-8')
    settingsList=file.readlines()
    file.close()
    for i in range(1,len(settingsList)):
        keyFind=settingsList[i].split()
        reactMessage=keyFind[3]
        reactEmote=keyFind[6]
        reactRole=" ".join(keyFind[9:])
        if payload.message_id == int(reactMessage):
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if str(payload.emoji) == reactEmote:
                role = discord.utils.get(guild.roles, name=reactRole)
                await member.add_roles(role)
                logDate="------------------------------------------------------------\n\n["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]: "
                e=(f'{guild.get_member(payload.user_id).name} has reacted with {reactEmote} on [{reactMessage}] to get the "{reactRole}" role.\n[ID]: {payload.user_id}\n\n')
                logging(payload.guild_id, e, logDate)

@bot.event
async def on_raw_reaction_remove(payload):
    path = dir+"/serverData/" + str(payload.guild_id)
    file = open(path + "/" + "settings.txt", "r", encoding='utf-8')
    settingsList=file.readlines()
    file.close()
    for i in range(1,len(settingsList)):
        keyFind=settingsList[i].split()
        reactMessage=keyFind[3]
        reactEmote=keyFind[6]
        reactRole=" ".join(keyFind[9:])
        if payload.message_id == int(reactMessage):
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if str(payload.emoji) == reactEmote:
                role = discord.utils.get(guild.roles, name=reactRole)
                await member.remove_roles(role)
                logDate="------------------------------------------------------------\n\n["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]: "
                e=(f'{guild.get_member(payload.user_id).name} has removed their {reactEmote} on [{reactMessage}] and lost the "{reactRole}" role.\n[ID]: {payload.user_id}\n\n')
                logging(payload.guild_id, e, logDate)




##########################################################
##                                                      ##
##                                                      ##
##                       COMMANDS                       ##
##                                                      ##
##                                                      ##
##########################################################

@bot.tree.command(name='sync_moxils', description='| BOT ONLY |')
async def sync(ctx):
    logDate="------------------------------------------------------------\n\n["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]: "
    e=(f"{ctx.user.name} is trying to access SYNC.\n[ID]: {ctx.user.id}")
    if ctx.user.id == owner_id:
        await bot.tree.sync()
        e=e+(" - { They're this bot's owner. }\n\n\n")
        logging(ctx.guild.id, e, logDate)
        await ctx.response.send_message('synced.', ephemeral=True)
    else:
        e=e+("- { They're not this bot's owner }\n\n\n")
        logging(ctx.guild.id, e, logDate)
        await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)


@bot.tree.command(name='default_role_moxils', description='[ADMIN] Adds a default access role ("admin") to pre-existing servers.')
@app_commands.check(owner_admin)
async def default_role(ctx):
    e="\n[/default_role] - "
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "settings.txt", "r", encoding='utf-8')
    wordList=file.readlines()
    file.close()
    if "[ACCESS]: " not in wordList[0]:
        wordList.insert(0, "[ACCESS]: admin\n")
        fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "settings.txt", "w", encoding='utf-8')
        fileWrite.writelines(wordList)
        fileWrite.close()
        await ctx.response.send_message('"admin" was made the default access role.', ephemeral=True)
        e=e+('"admin" was made the new default role')
    else:
        rolename=wordList[0].strip("\n").replace("[ACCESS]: ", "")
        e=e+(f'"{rolename}" was already the default role')
        await ctx.response.send_message(f'"{rolename}" has already been set up as the access role.', ephemeral=True)
    e=e+"\n\n\n"
    logDate=""
    logging(ctx.guild.id, e, logDate)

@bot.tree.command(name='role_moxils', description='[ADMIN] Setup a role to access advanced commands (i.e, "admin")')
@app_commands.check(allowedRoleCheck)
async def setupAllowedRole(ctx, role: str):
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "settings.txt", "r", encoding='utf-8')
    wordList=file.readlines()
    file.close()
    rolename=wordList[0].strip("\n").replace("[ACCESS]: ", "")
    logDate=""
    e=(f'\n[/role_moxils]\n[ORIGINAL ROLE]: "{rolename}"\n[NEW ROLE]: "{role}"\n\n\n')
    logging(ctx.guild.id, e, logDate)
    wordList[0]="[ACCESS]: "+role+"\n"
    fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "settings.txt", "w", encoding='utf-8')
    fileWrite.writelines(wordList)
    fileWrite.close()
    await ctx.response.send_message(f"\"{role}\" has been made the server's only role with access to the advanced commands!", ephemeral=True)


@bot.tree.command(name='set_react', description='[ADMIN] Gives a message a verification attribute.')
@app_commands.check(owner_admin)
async def react_msg(ctx, id: str, role: str, react: str):
    path = dir+"/serverData/" + str(ctx.guild.id)
    file = open(path + "/" + "settings.txt", "r", encoding='utf-8')
    settingsList=file.readlines()
    file.close()
    try:
        id = int(id)
    except ValueError:
        await ctx.response.send_message('Invalid message ID, please try again.', ephemeral=True)
        return
    react=react.replace(" ","")
    for i in range(len(settingsList)):
        keyFind=settingsList[i].split()
        if len(keyFind)>=3:
            if str(id)==keyFind[3] and react==keyFind[6]:
                fileReplace = open(path + "/" + "settings.txt", "w", encoding='utf-8')
                settingsList[i]=f'[Ver. #{len(settingsList)-1}]= (Message_ID): {id} | (Emote): {react} | (Role): {role}\n'
                fileReplace.writelines(settingsList)
                fileReplace.close()
                msg=await ctx.channel.fetch_message(id)
                await msg.add_reaction(react)
                await ctx.response.send_message(f'[https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}] Replaced the "{keyFind[9]}" role with the "{role}" role using the "{react}" reaction', ephemeral=True)
                break
            elif str(id)==keyFind[3]:
                fileReplace = open(path + "/" + "settings.txt", "w", encoding='utf-8')
                settingsList[i]=f'[Ver. #{len(settingsList)-1}]= (Message_ID): {id} | (Emote): {react} | (Role): {role}\n'
                fileReplace.writelines(settingsList)
                fileReplace.close()
                msg=await ctx.channel.fetch_message(id)
                await msg.add_reaction(react)
                await ctx.response.send_message(f'[https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}] Added  the "{role}" role using the "{react}" reaction', ephemeral=True)
                break
        if i==len(settingsList)-1:
            fileAdd = open(path + "/" + "settings.txt", "a", encoding='utf-8')
            txt=f'[Ver. #{len(settingsList)}]= (Message_ID): {id} | (Emote): {react} | (Role): {role}'
            fileAdd.write(txt+"\n")
            fileAdd.close()
            msg=await ctx.channel.fetch_message(id)
            await msg.add_reaction(react)
            await ctx.response.send_message(f'[https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}] Added the "{role}" role using the "{react}" reaction', ephemeral=True)
            
            


@bot.tree.error
async def on_command_error(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)

bot.run(token)