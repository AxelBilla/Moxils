#https://discord.com/oauth2/authorize?client_id=1306356201017184298

import os
import discord
import typing
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from random import randint
from private.config import token

owner_id=1242535080866349226
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, owner_id = owner_id)
dir = os.path.dirname(__file__)

def addPath(ctx):
    path = dir+"/serverData/" + str(ctx.guild.id)
    if not os.path.exists(path):
        os.makedirs(path)
        open(path+"/data.txt","w")
        file = open(path+"/data.txt", "w")
        word=["[ACCESS]: admin\n"]
        file.writelines(word)
        file.close()

def first_lower(s):
    if not s:
        return 
    else:
        return s[0].lower() + s[1:]

def first_upper(s):
    if not s:
        return 
    else:
        return s[0].upper() + s[1:]

@bot.event
async def owner_admin(ctx): #Allows me to debug stuff at will.
    print(f"\n\n\n{ctx.user.name} is trying to access a reserved ADMIN command.\n[ID]: {ctx.user.id}, [SERVER]: {ctx.guild.name}")
    addPath(ctx)
    async def predicate(ctx):
        if ctx.user.guild_permissions.administrator == True:
            print("They have administrator permissions.\n")
            return True
        else:
            if ctx.user.id == owner_id:
                print("They're this bot's owner.\n")
                return True
            else:
                print("They do not have an allowed role nor are they this bot's owner\n\n\n")
                await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)
                raise MissingPermissions(missing_permissions=['administrator'])
    a=await predicate(ctx)
    return app_commands.check(a) 

@bot.event
async def allowedRoleCheck(ctx): #Allows me to debug stuff at will.
    print(f"\n\n\n{ctx.user.name} is trying to access a reserved command.\n[ID]: {ctx.user.id}, [SERVER]: {ctx.guild.name}")
    addPath(ctx)
    async def predicate(ctx):
        file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "r")
        wordList=file.readlines()
        file.close()
        if len(wordList)==0:
            roleName="admin"
        else:
            roleName=wordList[0].strip("\n")
            roleName=roleName.replace("[ACCESS]: ", "")
        allowedRole = discord.utils.find(lambda r: r.name == roleName, ctx.guild.roles)
        if allowedRole in ctx.user.roles or ctx.user.guild_permissions.administrator == True:
            print("They have an allowed role.\n")
            return True
        else:
            if ctx.user.id == owner_id:
                print("They're this bot's owner.\n")
                return True
            else:
                print("They do not have an allowed role nor are they this bot's owner\n\n\n")
                await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)
                raise MissingPermissions(missing_permissions=['administrator'])
    a=await predicate(ctx)
    return app_commands.check(a) 

@bot.tree.command(name='sync_disk', description='| BOT OWNER ONLY |')
async def sync(ctx):
    print(f"\n\n\n{ctx.user.name} is trying to access SYNC. [ID]: {ctx.user.id}, [SERVER]: {ctx.guild.name}")
    if ctx.user.id == owner_id:
        await bot.tree.sync()
        print("They're this bot's owner.\n")
        await ctx.response.send_message('synced.', ephemeral=True)
    else:
        print("They're not this bot's owner")
        await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)

@bot.tree.command(name='default_role_disk', description='[ADMIN] Adds a default access role ("admin") to pre-existing servers.')
@app_commands.check(owner_admin)
async def default_role(ctx):
    print("[/default_role]")
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "r")
    wordList=file.readlines()
    file.close()
    if "[ACCESS]: " not in wordList[0]:
        wordList.insert(0, "[ACCESS]: admin\n")
        fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "w")
        fileWrite.writelines(wordList)
        fileWrite.close()
        await ctx.response.send_message('"admin" was made the default access role.', ephemeral=True)
        print('They made "admin" the new default role')
    else:
        rolename=wordList[0].strip("\n").replace("[ACCESS]: ", "")
        print(f'"{rolename}" was already the default role')
        await ctx.response.send_message(f'"{rolename}" has already been set up as the access role.', ephemeral=True)
        
@bot.tree.command(name='role_disk', description='[ADMIN] Setup a role to access advanced commands (i.e, "admin")')
@app_commands.check(owner_admin)
async def setupAllowedRole(ctx, role: str):
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "r")
    wordList=file.readlines()
    file.close()
    rolename=wordList[0].strip("\n").replace("[ACCESS]: ", "")
    print(f'[/role_disk]\n[ORIGINAL ROLE]: "{rolename}"\n[NEW ROLE]: "{role}"')
    wordList[0]="[ACCESS]: "+role+"\n"
    fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "w")
    fileWrite.writelines(wordList)
    fileWrite.close()
    await ctx.response.send_message(f"\"{role}\" has been made the server's only role with access to the advanced commands!", ephemeral=True)

@bot.tree.command(name='disk', description="Display a random line from the server's saved lines.")
async def returnHorn(ctx, mention: typing.Optional[str]=''):
    addPath(ctx)
    print(f"\n\n\n{ctx.user.name} is trying to access a command.\n[ID]: {ctx.user.id}, [SERVER]: {ctx.guild.name}\n\n[/disk] ")
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "r")
    wordList=file.readlines()
    file.close()
    print("Mention: ", mention)
    if mention != '':
        if len(wordList)<=1:
            await ctx.response.send_message(f"I don't have anything to tell, {mention}.")
        else:
            await ctx.response.send_message(f"{mention}, {first_lower(wordList[randint(1,int(len(wordList)-1))])}")
    else: 
        if len(wordList)<=1:
            await ctx.response.send_message("I don't have anything to tell you.")
        else:
            await ctx.response.send_message(first_upper(wordList[randint(1,int(len(wordList)-1))]))

@bot.tree.command(name='add_disk', description="Add a new line to the server's saved lines.")
@app_commands.check(allowedRoleCheck)
async def addHorn(ctx, txt: str):
    print("[/add_disk]")
    print(f'They added a new line.\n[CONTENT]: "{txt}"')
    path = dir+"/serverData/" + str(ctx.guild.id)
    file = open(path + "/" + "data.txt", "a")
    file.write(txt+"\n")
    file.close()
    await ctx.response.send_message(f"\"{txt}\" was successfully added!", ephemeral=True)

@bot.tree.command(name='del_disk', description="Remove a line by its content or id from the server's saved lines (* to remove every line).")
@app_commands.check(allowedRoleCheck)
async def delHorn(ctx, txt: str):
    print("[/del_disk]")
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "r")
    wordList=file.readlines()
    file.close()
    check=True
    if len(wordList)<=1:
        await ctx.response.send_message("You currently do not have any saved lines.", ephemeral=True)
    elif txt=="*":
        if ctx.user.guild_permissions.administrator == True or ctx.user.id == owner_id:
            print("They're an administrator or this bot's owner.\n")
            print(f'[USED "*"]\nEverything was deleted.')
            saved=wordList[0]
            wordList=[saved]
            fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "w")
            fileWrite.writelines(wordList)
            fileWrite.close()
            await ctx.response.send_message(f"Saved lines successfully cleared!", ephemeral=True)
        else:
            print("They do not have an allowed role nor are they this bot's owner\n\n\n")
            await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)
    else:
        for i in range(len(wordList)-1):
            if wordList[i+1]==txt+"\n" or str(i+1)==txt:
                ted=str(wordList[i+1].strip("\n"))
                print(f'They removed a line.\n[ID]: {i+1} has been deleted\n[CONTENT]: "{ted}"')
                wordList.pop(i+1)
                fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "w")
                fileWrite.writelines(wordList)
                fileWrite.close()
                await ctx.response.send_message(f"\"{txt}\" was successfully removed!", ephemeral=True)
                check=False
                break
        if check:
            await ctx.response.send_message(f"\"{txt}\" couldn't be found!", ephemeral=True)

@bot.tree.command(name='see_disk', description="Display a list of a server's saved lines.")
@app_commands.check(allowedRoleCheck)
async def checkHorn(ctx):
    print("[/see_disk]")
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.txt", "r")
    wordList=file.readlines()
    file.close()
    outString=""
    if len(wordList)<=1:
        await ctx.response.send_message("You currently do not have any saved lines.", ephemeral=True)
    else:
        rowSize=0
        for i in range(len(wordList)):
            if i != 0:
                wordList[i]=wordList[i].strip("\n")
                outString=outString+f"[{i}]: \"{wordList[i]}\"\n"
                rowSize=rowSize+1
                if rowSize == 10:
                    if i == 10:
                        await ctx.response.send_message(f'[LIST OF SAVED LINES]\n{outString}', ephemeral=True)
                    else:
                        await ctx.followup.send(outString, ephemeral=True)
                    outString=''
                    rowSize=0
        if i <= 10: 
            await ctx.response.send_message(f'[LIST OF SAVED LINES]\n{outString}', ephemeral=True)
        else:
            await ctx.followup.send(outString, ephemeral=True)

@bot.tree.error
async def on_command_error(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message('You do not have the permission(s) required to do this.', ephemeral=True)

bot.run(token)