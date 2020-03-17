""""
MIT License

Copyright (c) 2020 Dominik Büttner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
import datetime
from pytz import timezone
import traceback
import random
import asyncio
from config import CONFIG, SV_NEWS, UserInGameName
from config.GAMES import __games__, __gamesTimer__
import codecs
import os

client = discord.Client()
__version__ = '1.1.3'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
THIS_FILE = os.path.join(THIS_FOLDER, 'MIT.txt')
mit_license = codecs.open(THIS_FILE, "r", encoding="utf-8")
client.logoutMessageID = "NOTHING"

#on_ready
@client.event
async def on_ready():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                      + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    print(__printDateTime + "Der Bot wurde aktiviert")
    print(__printDateTime + f'Bot Name: {client.user.name}')
    print(__printDateTime + f'Discord Version: {discord.__version__}')
    print(__printDateTime + f'Bot Version: {__version__}')
    client.AppInfo = await client.application_info()
    print(__printDateTime + f'Owner: {client.AppInfo.owner}')
    client.gamesLoop = asyncio.ensure_future(_randomGame())
    print(__printDateTime + "Aktivität wurde aktiviert")


#on_error
@client.event
async def on_error(event, *args, **kwargs):
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                      + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    embed = discord.Embed(title=':x: Event Fehler', color=0xff0000)  # Red
    embed.add_field(name='Event', value=event)
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.timestamp = datetime.datetime.utcnow()
    try:
        await client.AppInfo.owner.send(embed=embed)
        print(__printDateTime + "ERROR:")
        traceback.print_exc()
        return
    except:
        pass
    traceback.print_exc()

#_randomGame()
@client.event
async def _randomGame():
    while True:
        guildCount = len(client.guilds)
        memberCount = len(list(client.get_all_members()))
        randomGame = random.choice(__games__)
        await client.change_presence(activity=discord.Activity(type=randomGame[0],
                                                            name=randomGame[1].format(guilds=guildCount,
                                                                                        members=memberCount)))
        await asyncio.sleep(random.choice(__gamesTimer__))
        if CONFIG.clientLogout == True:
            await client.change_presence(status=discord.Status.do_not_disturb,
                                        activity=discord.Game(name="Bot deaktiviert"))
            break

#on_guild_join
@client.event
async def on_guild_join(guild):
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    embed = discord.Embed(title=':white_check_mark: Zum Server hinzugefügt', color=0x2ecc71,
                        description="Server Name: " + str(guild.name) +
                                    "\nServer ID: " + str(guild.id) +
                                    "\nServer Besitzer: " + str(guild.owner.mention) +
                                    "\nServer Region: " + str(guild.region))
    embed.add_field(name="Mitglieder", value=str(guild.member_count) + " Mitglieder")
    CreateDateYear = str(guild.created_at)[0:4]
    CreateDateMonth = str(guild.created_at)[5:7]
    CreateDateDay = str(guild.created_at)[8:10]
    CreateDateTime = str(guild.created_at)[11:16]
    embed.add_field(name="Erstellt am",
                    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await client.AppInfo.owner.send(embed=embed)
    print(__printDateTime + "Zum Server hinzugefügt")

#on_guild_remove
@client.event
async def on_guild_remove(guild):
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    embed = discord.Embed(title=':x: Vom Server entfernt', color=0xe74c3c,
                        description="Server Name: " + str(guild.name) +
                                    "\nServer ID: " + str(guild.id) +
                                    "\nServer Besitzer: " + str(guild.owner.mention) +
                                    "\nServer Region: " + str(guild.region))
    embed.add_field(name="Mitglieder", value=str(guild.member_count) + " Mitglieder")
    CreateDateYear = str(guild.created_at)[0:4]
    CreateDateMonth = str(guild.created_at)[5:7]
    CreateDateDay = str(guild.created_at)[8:10]
    CreateDateTime = str(guild.created_at)[11:16]
    embed.add_field(name="Erstellt am",
                    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await client.AppInfo.owner.send(embed=embed)
    print(__printDateTime + "Vom Server entfernt")

#on_disconnect
@client.event
async def on_disconnect():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    logoutMessageID = ""
    print(__printDateTime + "Verbindung getrennt")

#on_resumed
@client.event
async def on_resumed():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "

    print(__printDateTime + "Verbindung wiederhergestellt")

#on_connect
@client.event
async def on_connect():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    print(__printDateTime + "Mit Discord verbunden")

#on_message
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.author.id == client.AppInfo.owner.id:
            #sv-id
                if message.content.startswith(CONFIG.PREFIX + "sv-id"):
                    args = message.content.split(" ")
                    if args == 2:
                        serverID = args[2]
                        if str.isdigit(serverID):
                            if client.get_guild(int(serverID)):
                                guildWithID = client.get_guild(int(serverID))
                                embed = discord.Embed(title=':white_check_mark: Server gefunden', color=0x2ecc71,
                                                    description="Server Name: " + str(guildWithID.name) +
                                                                "\nServer ID: " + str(guildWithID.id) +
                                                                "\nServer Besitzer: " + str(guildWithID.owner.mention) +
                                                                "\nServer Region: " + str(guildWithID.region))
                                embed.add_field(name="Mitglieder", value=str(guildWithID.member_count) + " Mitglieder")
                                CreateDateYear = str(guildWithID.created_at)[0:4]
                                CreateDateMonth = str(guildWithID.created_at)[5:7]
                                CreateDateDay = str(guildWithID.created_at)[8:10]
                                CreateDateTime = str(guildWithID.created_at)[11:16]
                                embed.add_field(name="Erstellt am",
                                                value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                                embed.set_thumbnail(url=guildWithID.icon_url)
                                embed.timestamp = datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            else:
                                embed = discord.Embed(title="", color=0xff0000, description=":x: Server nicht gefunden!")
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed)
                        else:
                            embed = discord.Embed(title="", color=0xff0000, description=":x: Das ist keine gültige ServerID")
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed)
                    else:
                        embed = discord.Embed(title="", color=0xff0000, description=":x: Bitte benutze **" + CONFIG.PREFIX + "sv-id [ServerID]**")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed)
                    
            #stop
                if message.content.startswith(CONFIG.PREFIX + 'stop'):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird gestopt...", color=0xe74c3c)
                        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
                        CONFIG.clientLogout = True
                        print(__printDateTime + "Bot gestopt")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon gestopt", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    
            #start
                if message.content.startswith(CONFIG.PREFIX + 'start'):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == True:
                        embed = discord.Embed(title="", description="Der Bot wird gestartet...", color=0x2ecc71)
                        client.gamesLoop = asyncio.ensure_future(_randomGame())
                        CONFIG.clientLogout = False
                        print(__printDateTime + "Bot gestartet")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon gestartet", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    
            #logout
                if message.content.startswith(CONFIG.PREFIX + 'logout'):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    await message.add_reaction("\U00002705")
                    await message.add_reaction("\U0000274c")
                    client.logoutMessageID = message.id
                    @client.event
                    async def on_reaction_add(reaction, user):
                        DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                        __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[
                                                                                                    17:19] + " " \
                                        + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(
                            DateTime.year) + " \xbb "
                        if reaction.message.author.id == client.AppInfo.owner.id:
                            if reaction.message.id == client.logoutMessageID:
                                if user.id == client.AppInfo.owner.id:
                                    if reaction.emoji == '\U00002705':
                                        logOut = discord.Embed(title="", color=0xe74c3c, description="Abmeldung erfolgt")
                                        await message.channel.send(embed=logOut)
                                        print(__printDateTime + "Abmeldung")
                                        client.logoutMessageID = "NOTHING"
                                        await asyncio.sleep(2)
                                        await client.change_presence(status=discord.Status.offline)
                                        await client.logout()
                                    if reaction.emoji == '\U0000274c':
                                        logOutCancel = discord.Embed(title="", color=0xe74c3c, description="Abmeldung abgebrochen")
                                        await message.channel.send(embed=logOutCancel)
                                        client.logoutMessageID = "NOTHING"
                                    
        #PrivateMessage
        else:
            embed = discord.Embed(title="", description=":x: Hey, ich bin nur ein Bot und nehme keine Privaten Nachrichten an!", color=0xff0000)
            if not message.author.bot:
                await message.channel.trigger_typing()
                await asyncio.sleep(0.5)
                await message.author.send(embed=embed)
    
    #ServerCommands
    else:
        #stop
            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                if message.author.id == client.AppInfo.owner.id:
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird gestopt...", color=0xe74c3c)
                        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
                        CONFIG.clientLogout = True
                        print(__printDateTime + "Bot gestopt")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon gestopt", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
                
        #start
            if message.content.startswith(CONFIG.PREFIX + 'start'):
                if message.author.id == client.AppInfo.owner.id:
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == True:
                        embed = discord.Embed(title="", description="Der Bot wird gestartet...", color=0x2ecc71)
                        client.gamesLoop = asyncio.ensure_future(_randomGame())
                        CONFIG.clientLogout = False
                        print(__printDateTime + "Bot gestartet")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon gestartet", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
                
        #logout
            if message.content.startswith(CONFIG.PREFIX + 'logout'):
                if message.author.id == client.AppInfo.owner.id:
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    await message.add_reaction("\U00002705")
                    await message.add_reaction("\U0000274c")
                    client.logoutMessageID = message.id
                    @client.event
                    async def on_reaction_add(reaction, user):
                        DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                        __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[
                                                                                                    17:19] + " " \
                                        + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(
                            DateTime.year) + " \xbb "
                        if reaction.message.author.id == client.AppInfo.owner.id:
                            if reaction.message.id == client.logoutMessageID:
                                if (user.id == client.AppInfo.owner.id) | (user.id == client.user.id):
                                    if user.id == client.AppInfo.owner.id:
                                        if reaction.emoji == '\U00002705':
                                            logOut = discord.Embed(title="", color=0xe74c3c, description="Abmeldung erfolgt")
                                            await message.channel.send(embed=logOut)
                                            print(__printDateTime + "Abmeldung")
                                            client.logoutMessageID = "NOTHING"
                                            await asyncio.sleep(2)
                                            await client.change_presence(status=discord.Status.offline)
                                            await client.logout()
                                        if reaction.emoji == '\U0000274c':
                                            logOutCancel = discord.Embed(title="", color=0xe74c3c, description="Abmeldung abgebrochen")
                                            await message.channel.send(embed=logOutCancel)
                                            client.logoutMessageID = "NOTHING"
                                else:
                                    if reaction.emoji == '\U00002705':
                                        await message.remove_reaction('\U00002705', user)
                                    if reaction.emoji == '\U0000274c':
                                        await message.remove_reaction('\U0000274c', user)
                                
        #BotAn
            if CONFIG.clientLogout == False:
            #sv-news
                if message.content.startswith(CONFIG.PREFIX + 'sv-news'):
                    if message.guild.id in SV_NEWS.newsID:
                        patchChannelID = SV_NEWS.newsID.get(message.guild.id)[0:18]
                        patchMessageID = SV_NEWS.newsID.get(message.guild.id)[19:37]
                        try:
                            patchChannel = message.guild.get_channel(int(patchChannelID))
                            try:
                                patchMessage = await patchChannel.fetch_message(int(patchMessageID))
                                embed = discord.Embed(title="", description="", color=0x00ff00)
                                embed.add_field(name="Neuigkeiten", value=patchMessage.content, inline=False)
                                embed.set_footer(text="Server News von " + message.guild.name, icon_url=client.user.avatar_url, )
                                embed.set_thumbnail(url=message.guild.icon_url)
                                embed.timestamp = datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(":x: Diese Nachricht wurde gelöscht!")
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Dieser Channel wurde gelöscht!")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Es wurde keine Nachricht eingestellt!")
            
            #set-news
                if message.content.startswith(CONFIG.PREFIX + 'set-news'):
                    if message.author.guild_permissions.manage_guild:
                        if len(message.content) == 47:
                            channelID = message.content[10:28]
                            messageID = message.content[29:47]
                            if str.isdigit(channelID) & str.isdigit(messageID):
                                if message.guild.get_channel(int(channelID)):
                                    try:
                                        await message.guild.get_channel(int(channelID)).fetch_message(int(messageID))
                                        try:
                                            sv_news = open(".\config\SV_NEWS.py", "w")
                                            try:
                                                try:
                                                    SV_NEWS.newsID.pop(message.guild.id)
                                                    SV_NEWS.newsID.update({message.guild.id: str(channelID) + "(" + str(messageID) + ")"})
                                                    __newDictionary = SV_NEWS.newsID.copy()
                                                    __newDictionary = str(__newDictionary).replace("{", "{\n ")
                                                    __newDictionary = str(__newDictionary).replace(",", ",\n")
                                                    __newDictionary = str(__newDictionary).replace("}", "\n}")
                                                    sv_news.write("newsID = " + str(__newDictionary))
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(":white_check_mark: Erfolgreich gesetzt")
                                                except:
                                                    SV_NEWS.newsID.update({message.guild.id: str(channelID) + "(" + str(messageID) + ")"})
                                                    __newDictionary = SV_NEWS.newsID.copy()
                                                    __newDictionary = str(__newDictionary).replace("{", "{\n ")
                                                    __newDictionary = str(__newDictionary).replace(",", ",\n")
                                                    __newDictionary = str(__newDictionary).replace("}", "\n}")
                                                    sv_news.write("newsID = " + str(__newDictionary))
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(":white_check_mark: Erfolgreich gesetzt")
                                            except:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(":x: Konfig konnte nicht gespeichert werden!")
                                        except:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(":x: Datei wurde nicht gefunden!")
                                    except:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(":x: Die Nachrichten-ID ist ungültig!")
                                else:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(":x: Die Kanal-ID ist ungültig!")
                            else:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "set-news [Kanal-ID] [Nachrichten-ID]**")
                        else:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "set-news [Kanal-ID] [Nachrichten-ID]**")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Keine Rechte!")
                        
            #bot-info
                if message.content.startswith(CONFIG.PREFIX + "bot-info"):
                    client.AppInfo = await client.application_info()
                    latency = str(client.latency)[0:4]
                    embed = discord.Embed(title="Bot Informationen",
                                        description="Bot-Name: " + client.user.name + "\nBot-ID: " + str(
                                            client.user.id) + "\nDiscord Version: " + str(discord.__version__) +
                                                    "\nBot Version: " + str(
                                            __version__) + "\nPing: " + latency + "ms" + "\nPrefix: **&**" + "\nBot Developer: " + str(
                                            client.AppInfo.owner.mention) + "\nBot-Sprache: :flag_de: German, Deutsch",
                                        color=0xffffff)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
                    
            #sv-info
                if message.content.startswith(CONFIG.PREFIX + "sv-info"):
                    if message.guild.id in CONFIG.SupportLicenseServer:
                        serverLicense = "Unterstützer Lizenz"
                    elif message.guild.id in CONFIG.AllowedServer:
                        serverLicense = "Standard Lizenz"
                    else:
                        serverLicense = "Keine Lizenz"
                    client.AppInfo = await client.application_info()
                    embed = discord.Embed(title="Server Informationen",
                                        description="Server Name: " + str(message.guild.name) + "\nServer ID: " + str(
                                            message.guild.id) +
                                                    "\nServerbesitzer: " + str(
                                            message.guild.owner.mention) + "\nServer Region: " + str(
                                            message.guild.region) + "\nLizenz: " + str(serverLicense), color=0xffffff)
                    embed.add_field(name="Mitglieder", value=str(message.guild.member_count) + " Mitglieder")
                    CreateDateYear = str(message.guild.created_at)[0:4]
                    CreateDateMonth = str(message.guild.created_at)[5:7]
                    CreateDateDay = str(message.guild.created_at)[8:10]
                    CreateDateTime = str(message.guild.created_at)[11:16]
                    embed.add_field(name="Erstellt am",
                                    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                    embed.set_footer(text="Server Info von " + message.guild.name, icon_url=client.user.avatar_url)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
            
            #whois
                if message.content.startswith(CONFIG.PREFIX + "whois"):
                    if len(message.content) == 6:
                        member = message.author
                    try:
                        if not len(message.content) == 6:
                            member = message.mentions[0]
                    except:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "whois <@User#1234>**")
                        return
                    __JoinPos__ = ""
                    if member.joined_at is None:
                        __JoinPos__ = "Ich konnte dein Beitrittdatum nicht feststellen"
                        return
                    __JoinPos__ = sum(
                        m.joined_at < member.joined_at for m in message.guild.members if m.joined_at is not None)
                    if __JoinPos__ == 0:
                        __JoinPos__ = "Besitzer"
                    AuthorGuildJoinDate = str(member.joined_at)[8:10] + "." + str(member.joined_at)[5:7] + "." + str(
                        member.joined_at)[0:4] + " um " + str(member.joined_at)[11:16] + " Uhr"
                    AuthorRegisterDate = str(member.created_at)[8:10] + "." + str(member.created_at)[5:7] + "." + str(
                        member.created_at)[0:4] + " um " + str(member.created_at)[11:16] + " Uhr"
                    role_name = [role.mention for role in member.roles]
                    role_name = role_name[1:]
                    role_name.reverse()
                    role_list = ', '.join(role_name)
                    role_amount = role_list.count("@")
                    if len(role_list) <= 25:
                        role_list = "\n:x: Keine Rollen auf dem Server"
                    
                    color = member.top_role.color
                    
                    __AllPerms = ""
                    if member.guild_permissions.administrator:
                        __AllPerms += "Administrator, "
                    if member.guild_permissions.manage_guild:
                        __AllPerms += "Server verwalten, "
                    if member.guild_permissions.manage_webhooks:
                        __AllPerms += "Webhooks verwalten, "
                    if member.guild_permissions.manage_roles:
                        __AllPerms += "Rollen verwalten, "
                    if member.guild_permissions.manage_emojis:
                        __AllPerms += "Emojis verwalten, "
                    if member.guild_permissions.manage_channels:
                        __AllPerms += "Kanäle verwalten, "
                    if member.guild_permissions.manage_messages:
                        __AllPerms += "Nachrichten verwalten, "
                    if member.guild_permissions.ban_members:
                        __AllPerms += "Mitglieder bannen, "
                    if member.guild_permissions.kick_members:
                        __AllPerms += "Mitglieder kicken, "
                    if member.guild_permissions.manage_nicknames:
                        __AllPerms += "Nicknamen verwalten, "
                    if member.guild_permissions.change_nickname:
                        __AllPerms += "Nicknamen ändern"
                    if __AllPerms == "":
                        __AllPerms = ":x: Keine Rechte auf dem Server"
                    embed = discord.Embed(title="", description="Name: " + str(member.mention) +
                                                                "\nID: " + str(member.id) +
                                                                "\nBeigetreten: " + str(AuthorGuildJoinDate) +
                                                                "\nJoin Position: " + str(__JoinPos__) +
                                                                "\nRegistriert: " + str(AuthorRegisterDate) +
                                                                f'\nRollen [{role_amount}]: {role_list}' +
                                                                f' \nBerechtigungen: \n{__AllPerms}', color=color)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(name=member, icon_url=member.avatar_url)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
            
            #ping
                if message.content.startswith(CONFIG.PREFIX + "ping"):
                    latency = str(client.latency)[0:4]
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send("Bot Ping = " + latency + "ms")
                    
            #invite
                if message.content.startswith(CONFIG.PREFIX + "invite"):
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(message.author.mention + ", der Einladungslink wurde dir zugeschickt.")
                    embed = discord.Embed(title="", description="Hier kannst du mich zu deinem Server einladen:\n"
                                                                "http://bit.ly/361uYxI\n", color=0xffffff)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    if not message.author.bot:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.author.send(embed=embed)
                        
            #src
                if message.content.startswith(CONFIG.PREFIX + "src"):
                    embed = discord.Embed(title="", description="Hier findest du meinen Source Code:"
                                                                "\nhttps://github.com/IBimsEinMystery/ServerMod"
                                                                "\n\n**Dieser Source Code steht unter Lizenz:**"
                                                                "\n```" + mit_license.read() + "```", color=0xffffff)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
            
            #kick
                if message.content.startswith(CONFIG.PREFIX + "kick"):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[
                                                                                                17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(
                        DateTime.year) + " \xbb "
                    if message.author.guild_permissions.kick_members:
                        try:
                            memberKick = message.mentions[0]
                            author = message.author
                            argsLenght = len(str(CONFIG.PREFIX) + "kick @" + str(client.user)) + 3
                            messageMention = message.content[0:argsLenght]
                            try:
                                if not str(client.user.id) in messageMention:
                                    try:
                                        if not str(message.guild.owner.id) in message.mentions:
                                            try:
                                                await memberKick.kick(reason=None)
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(":white_check_mark: Du hast " + memberKick.mention + " gekickt")
                                                print(__printDateTime + str(author) + " hat " + str(memberKick) + " von " + message.guild.name + "(" +  str(message.guild.id) + ")" + " gekickt")
                                            except:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(":x: Ich darf das nicht!")
                                        else:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(":x: Du kannst denn Besitzer dieses Servers nicht kicken!")
                                    except:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(":x: Du kannst denn Besitzer dieses Servers nicht kicken!")
                                else:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(":x: Ich kann mich nicht selber kicken!")
                            except:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(":x: Ich kann mich nicht selber kicken!")
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "kick [@User#1234]**!")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Keine Rechte!")
                
            #uplay
                if(message.content.startswith(CONFIG.PREFIX + "uplay")):
                    if len(message.content) == 6:
                            member = message.author
                    elif not len(message.content) == 6:
                        try:
                            member = message.mentions[0]
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "uplay<@User#1234>**")
                            return
                    
                    if not client.user.id == member.id:
                        if member.id in UserInGameName.uplay:
                            UserName = UserInGameName.uplay.get(member.id)
                            embed=discord.Embed(title="", description="Name: " + UserName, color=0x0070FF)
                            embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="", description=member.mention + " muss erst seinen\nAccount mit `&register uplay [Name]`\nverknüpfen", color=0x0070FF)
                            embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="", description=":x: Mich gibt es nicht auf Uplay", color=0x0070FF)
                        embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                        embed.timestamp=datetime.datetime.utcnow()
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                      
            #steam        
                if(message.content.startswith(CONFIG.PREFIX + "steam")):
                    if len(message.content) == 6:
                            member = message.author
                    elif not len(message.content) == 6:
                        try:
                            member = message.mentions[0]
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "steam <@User#1234>**")
                            return
                    
                    if not client.user.id == member.id:
                        if member.id in UserInGameName.steam:
                            UserName = UserInGameName.steam.get(member.id)
                            embed=discord.Embed(title="", description="Name: " + UserName, color=0x091936)
                            embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="", description=member.mention + " muss erst seinen\nAccount mit `&register steam [Name]`\nverknüpfen", color=0x091936)
                            embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="", description=":x: Mich gibt es nicht auf Steam", color=0x091936)
                        embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                        embed.timestamp=datetime.datetime.utcnow()
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    
            #epicgames
                if(message.content.startswith(CONFIG.PREFIX + "epicgames")):
                    if len(message.content) == 10:
                            member = message.author
                    elif not len(message.content) == 10:
                        try:
                            member = message.mentions[0]
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "epicgames <@User#1234>**")
                            return
                    if not client.user.id == member.id:
                        if member.id in UserInGameName.epicgames:
                            UserName = UserInGameName.epicgames.get(member.id)
                            embed=discord.Embed(title="", description="Name: " + UserName, color=0x2F2D2E)
                            embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="", description=member.mention + " muss erst seinen\nAccount mit `&register epicgames [Name]`\nverknüpfen", color=0x2F2D2E)
                            embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="", description=":x: Mich gibt es nicht auf Epic Games", color=0x2F2D2E)
                        embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                        embed.timestamp=datetime.datetime.utcnow()
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    
            #register
                if(message.content.startswith(CONFIG.PREFIX + "register")):
                    if len(message.content) >= 10: 
                        args = message.content.split(" ")
                        if args[1] == "uplay":
                            if len(message.content) >= 16:
                                UserName = str(args[2])
                                if len(message.content) <= 16 + len(args[2]):
                                    try:
                                        uplay = codecs.open(".\\config\\UserInGameName.py", "w")
                                        if message.author.id in UserInGameName.uplay:
                                            UserInGameName.uplay.pop(message.author.id)
                                            UserInGameName.uplay.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            uplay.write("uplay = " + newFileUplay)
                                            uplay.write("\nsteam = " + newFileSteam)
                                            uplay.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Uplay: " + args[2], icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        else:
                                            UserInGameName.uplay.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            uplay.write("uplay = " + newFileUplay)
                                            uplay.write("\nsteam = " + newFileSteam)
                                            uplay.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Uplay: " + args[2], icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description=":x: Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xe74c3c)
                                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                        embed.timestamp=datetime.datetime.utcnow()
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description=":x: Der Name darf keine Leerzeichen enthalten!", color=0xe74c3c)
                                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                    embed.timestamp=datetime.datetime.utcnow()
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description=":x: Bitte benutze **&register uplay [Name]**", color=0xe74c3c)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                                
                        elif args[1] == "steam":
                            if len(message.content) >= 16:
                                UserName = str(args[2])
                                if len(message.content) <= 16 + len(args[2]):
                                    try:
                                        steam = codecs.open(".\\config\\UserInGameName.py", "w")
                                        if message.author.id in UserInGameName.steam:
                                            UserInGameName.steam.pop(message.author.id)
                                            UserInGameName.steam.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            steam.write("uplay = " + newFileUplay)
                                            steam.write("\nsteam = " + newFileSteam)
                                            steam.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Steam: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        else:
                                            UserInGameName.steam.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            steam.write("uplay = " + newFileUplay)
                                            steam.write("\nsteam = " + newFileSteam)
                                            steam.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Steam: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description=":x: Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xe74c3c)
                                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                        embed.timestamp=datetime.datetime.utcnow()
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description=":x: Der Name darf keine Leerzeichen enthalten!", color=0xe74c3c)
                                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                    embed.timestamp=datetime.datetime.utcnow()
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description=":x: Bitte benutze **&register steam [Name]**", color=0xe74c3c)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                              
                        elif args[1] == "epicgames":
                            if len(message.content) >= 20:
                                UserName = str(args[2])
                                if len(message.content) <= 20 + len(args[2]):
                                    try:
                                        epic = codecs.open(".\\config\\UserInGameName.py", "w")
                                        if message.author.id in UserInGameName.uplay:
                                            UserInGameName.epicgames.pop(message.author.id)
                                            UserInGameName.epicgames.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            epic.write("uplay = " + newFileUplay)
                                            epic.write("\nsteam = " + newFileSteam)
                                            epic.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Epic Games: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        else:
                                            UserInGameName.epicgames.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            epic.write("uplay = " + newFileUplay)
                                            epic.write("\nsteam = " + newFileSteam)
                                            epic.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Epic Games: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description=":x: Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xe74c3c)
                                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                        embed.timestamp=datetime.datetime.utcnow()
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description=":x: Der Name darf keine Leerzeichen enthalten!", color=0xe74c3c)
                                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                    embed.timestamp=datetime.datetime.utcnow()
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description=":x: Bitte benutze **&register epicgames [Name]**", color=0xe74c3c)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                        
                        else:
                            embed=discord.Embed(title="", description=":x: Bitte benutze **&register [uplay/steam/epicgames] [Name]**", color=0xe74c3c)
                            embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                            embed.timestamp=datetime.datetime.utcnow()
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                            
            #RespondOnPing
                if client.user.mentioned_in(message) and message.mention_everyone is False:
                    if not message.author.bot:
                        if message.content.startswith((CONFIG).PREFIX + "stop"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "login"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "sv-news"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "set-news"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "bot-info"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "sv-info"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "whois"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "ping"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "invite"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "src"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "kick"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "uplay"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "steam"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "epicgames"):
                            return
                        if message.content.startswith("Hallo"):
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send('Hallo ' + message.author.mention)
                            return
                        else:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send('Meine Prefix ist **' + CONFIG.PREFIX + '** ' + message.author.mention)


client.run(CONFIG.TOKEN)
