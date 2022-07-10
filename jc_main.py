hallo
import discord
import asyncio
import functools
import itertools
import math
import random
from random import randrange
import requests
import json
import urllib
import os
import re
import logging
import youtube_dl
import DiscordUtils
from discord import guild
from discord import Guild
from discord import Member
from discord import Intents
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops, ImageColor
from io import BytesIO
from datetime import datetime
from datetime import timedelta, timezone
from discord import colour, Spotify
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType, Select, SelectOption, Interaction
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

wartungsarbeiten = False

TOKEN = 'Der Token steht normalerweise hier'
client = commands.Bot(command_prefix = commands.when_mentioned_or(','), help_command=None, case_insensitive=True, intents=Intents.all())
slash = SlashCommand(client, sync_commands=True)


guild_ids = [776912251944435723]


@client.event
async def on_ready():
    DiscordComponents(client)
    print('Der JOBCENTER Bot ist jetzt online und startklar!')
    client.loop.create_task(status_task())
    client.loop.create_task(server_stats())
    client.loop.create_task(server_team())
    botuser = client.get_guild(776912251944435723).get_member(client.user.id)
    if not botuser.guild_permissions.administrator:
        amin = client.get_user(753009216767393842)
        kj = client.get_user(796503415021633586)
        try:
            await amin.send("**An Error has occured:**\r\ndiscord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions")
            print(f"Alert sent to {amin}")
        except:
            try:
                await kj.send("**An Error has occured:**\r\ndiscord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions")
                print(f"Alert sent to {kj}")
            except:
                pass
    channel = client.get_channel(868012543287918683)
    user = client.get_user(515602740500627477)
    await channel.set_permissions(user, send_messages=True, view_channel=True)
    logchannel = client.get_channel(884507838645428224)
    embed = discord.Embed(title='Bot online', description='Der Bot ist jetzt online.\r\nAktueller Ping: __**{0}s**__'.format(round(client.latency, 3)), timestamp=datetime.now(), color=0xE31316)
    embed.set_thumbnail(url=client.user.avatar_url)


async def status_task():
    while True:
        mainserver = client.get_guild(776912251944435723)
        #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="DM for ModMail"))
        #await asyncio.sleep(15)
        if wartungsarbeiten != True:
            await client.change_presence(activity=discord.Game(',help'), status=discord.Status.online)
            await asyncio.sleep(15)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{mainserver.member_count} Usern"))
            await asyncio.sleep(15)
            await client.change_presence(activity=discord.Game('Developed by Luca.'), status=discord.Status.online)
            await asyncio.sleep(15)
        else:
            await client.change_presence(activity=discord.Game('WARTUNGSARBEITEN'), status=discord.Status.dnd)


async def server_stats():
    server = client.get_guild(776912251944435723)
    channel = client.get_guild(776912251944435723).get_channel(868012515072811028)
    chat = client.get_channel(868012618214944788)
    msg = await channel.fetch_message(868044479607746591)
    while True:
        gesamt = 0
        online = 0
        for allmembers in server.members:
            if str(allmembers.status) == 'online':
                online += 1
                gesamt += 1
        idle = 0
        for allmembers in server.members:
            if str(allmembers.status) == 'idle':
                idle += 1
                gesamt += 1
        dnd = 0
        for allmembers in server.members:
            if str(allmembers.status) == 'dnd':
                dnd += 1
                gesamt += 1
        offline = 0
        for allmembers in server.members:
            if str(allmembers.status) == 'offline':
                offline += 1
        bots = 0
        for allmembers in server.members:
            if allmembers.bot:
                bots += 1
        teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
        sicherheitsrole = client.get_guild(776912251944435723).get_role(868012491672784907)
        embed = discord.Embed(title='**JOBCENTER - Serverstats**',
                              timestamp=datetime.now(timezone.utc), color=0xE31316)
        embed.add_field(name=f'Member `{server.member_count}`', value=f'> <a:JC_smoke:837039353342459916> Insgesamt Online: **{gesamt}**\r\n'
                                                                                                       f'> <:JC_online:855064789294383134> Online: **{online}**\r\n'
                                                                                                       f'> <:JC_idle:855064789490204712> Abwesend: **{idle}**\r\n'
                                                                                                       f'> <:JC_dnd:855064789443936256> Nicht stören: **{dnd}**\r\n'
                                                                                                       f'> <:JC_offline:855064789314699284> Offline: **{offline}**\r\n'
                                                                                                       '\r\n'
                                                                                                       f'> <:JC_team:854758876574384128> Team Member: **{len(teamrole.members)}**\r\n'
                                                                                                       f'> :no_entry: Sicherheitskontrolle: **{len(sicherheitsrole.members)}**\r\n'
                                                                                                       f'> <:JC_bot:854748828287893514> Bots: **{bots}**\r\n'
                                                                                                       f'> <:JC_ban:854761493215576064> Bans: **{len(str(server.bans))}**\r\n'
                                                                                                       '** **\r\n** **')
        embed.add_field(name='<:JC_nitroboost:855065705103491072> Booster', value=f'> <a:JC_booster:828812485150244875> Server Booster: **{str(len(server.premium_subscribers))}**\r\n'
                                                                             f'> <a:JC_boosts:830342355587956756> Boosts: **{server.premium_subscription_count}**\r\n'
                                                                              '** **\r\n** **', inline=False)
        embed.add_field(name='Channel', value=f'> Textkanäle: **{str(len(server.text_channels))}**\r\n'
                                                                                f'> Sprachkanäle: **{str(len(server.voice_channels))}**'
                                                                                 '\r\n** **\r\n** **')
        rolecount = 0
        for allroles in server.roles:
            if len(allroles.members) == 0:
                rolecount += 1
        embed.add_field(name='Rollen', value=f'> Anzahl: **{str(len(server.roles))}**\r\n'
                                                                           f'> Ohne Member: **{rolecount}**')
        embed.set_thumbnail(url=server.icon_url)
        embed.set_footer(text='Aktueller Stand')
        await msg.edit(embed=embed)

        background = Image.open("./JOBCENTER/Serverbanner.png")
        font = ImageFont.truetype("./JOBCENTER/HotBleb.ttf", 14)
        W, H = (256, 143)

        draw = ImageDraw.Draw(background)
        text = str(server.member_count)
        text2 = str(server.premium_subscription_count)

        w, h = draw.textsize(text)
        draw.text(((W-w)/2 - 80,(H-h)/2 + 55), text, (255, 255, 255), font=font)
        w, h = draw.textsize(text2)
        draw.text(((W-w)/2 + 85,(H-h)/2 + 55), text2, (255, 255, 255), font=font)
        background.save("./JOBCENTER/newServerBanner.png")

        with open('./JOBCENTER/newServerBanner.png', 'rb') as f:
            banner = f.read()

        await server.edit(banner=banner)

        await asyncio.sleep(600)


async def server_team():
    while True:
        server = client.get_guild(776912251944435723)
        coowner = server.get_role(886420174859816970)
        serverleitung = server.get_role(868390084389519380)
        teamleitung = server.get_role(841759555927015435)
        admin = server.get_role(841759557206540298)
        developer = server.get_role(884886593628954624)
        srmod = server.get_role(868012368163119144)
        mod = server.get_role(868012369324965919)
        sup = server.get_role(868012370188963860)
        embed = discord.Embed(title='〉 𝐉𝐎𝐁𝐂𝐄𝐍𝐓𝐄𝐑 𝐓𝐄𝐀𝐌 〈',
                              description=f'**➥ 🔱  》Owner\r\n'
                                          f'\r\n'
                                          f'⮩ <@!753009216767393842>  \r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {coowner.name}\r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in coowner.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {serverleitung.name} \r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in serverleitung.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {teamleitung.name} \r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in teamleitung.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {admin.name} \r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in admin.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {developer.name} Team\r\n'
                                          f'\r\n'
                                          f'⮩ <@!515602740500627477> `Developer Leitung`\r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in developer.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {srmod.name} \r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in srmod.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {mod.name} \r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in mod.members) + '\r\n'
                                          f'\r\n'
                                          f'⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷\r\n'
                                          f'\r\n'
                                          f'➥ {sup.name} \r\n'
                                          f'\r\n'
                                          f'⮩ ' + "\r\n\r\n⮩ ".join(m.mention for m in sup.members) + '**\r\n',
                              timestamp=datetime.now(),
                              color=0x4D0000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/798960532680998912/830869323773509652/image4.gif')
        embed.set_image(url='https://i.ibb.co/PWkkZhZ/itachired-jobecenter.gif')
        embed.set_footer(text='Aktueller Stand')
        channel = client.get_guild(776912251944435723).get_channel(868012610912681994)
        msg = await channel.fetch_message(868044820470456340)
        await msg.edit(embed=embed)
        await asyncio.sleep(86400)


def is_not_pinned(mess):
    return not mess.pinned


def check_team(ctx):
    return client.get_guild(776912251944435723).get_role(868012376946004059) in ctx.author.roles
    

@client.command()
async def antiwick(ctx):
    if ctx.author.id == 776912251944435723:
        role = ctx.guild.get_role(873978926026879017)
        await role.edit(position=100)
        

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Komm mal runter bro!",description=f"Du bist zu schnell!\r\nVersuche es erneut in **{error.retry_after:.0f}s**.", color=0xff0000)#{error.retry_after:.2f}s
        await ctx.send(embed=em, delete_after=10)
    else:
        logchannel = client.get_channel(884507596059455538)
        embed = discord.Embed(title='Fehler aufgetreten!', description=f'```{error}```', timestamp=datetime.now(), color=0xff0000)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text='Server: ' + ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.add_field(name='Content:', value=f'```{ctx.message.content}```\r\n[Zur Nachricht springen]({ctx.message.jump_url})', inline=False)
        embed.add_field(name='Member:', value=f'{ctx.author}', inline=False)
        embed.add_field(name='Ping:', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='UserID:', value=f'{ctx.author.id}', inline=False)
        embed.add_field(name='GuildID:', value=f'{ctx.guild.id}', inline=False)
        embed.add_field(name='Channel:', value=f'{ctx.channel.mention}', inline=False)
        await logchannel.send(embed=embed)


### Variables

bw_offen = False
mod_enabled = True
rp_enabled = True
fun_enabled = True
vc_enabled = True
casino_enabled = True
welcome_enabled = True
lvl_enabled = False

###


@client.command()
async def getallcommands(ctx):
    if ctx.author.id == 515602740500627477:
        url = f"https://discord.com/api/v8//applications/{client.user.id}/guilds/{ctx.guild.id}/commands"
        
        headers = {
            "Authorization": f"Bot {TOKEN}"
        }

        r = requests.get(url, headers=headers)
        response = r.json()
        embed = discord.Embed(description=str(response), color=0xE31316)
        await ctx.send(embed=embed)

@client.command()
async def addcommand(ctx, type: int, name: str):
    if ctx.author.id == 515602740500627477:
        url = f"https://discord.com/api/v8//applications/{client.user.id}/guilds/{ctx.guild.id}/commands"
        
        headers = {
            "Authorization": f"Bot {TOKEN}"
        }

        json = {
            "name": f"{name}",
            "type": int(type)
        }

        r = requests.post(url, headers=headers, json=json)
        await ctx.send('Command added successfuly!')

@client.command()
async def removecommand(ctx, id):
    if ctx.author.id == 515602740500627477:
        url = f"https://discord.com/api/v8//applications/{client.user.id}/guilds/{ctx.guild.id}/commands/{id}"
        
        headers = {
            "Authorization": f"Bot {TOKEN}"
        }

        r = requests.delete(url, headers=headers)
        await ctx.send('Command removed successfuly!')


@client.command()
async def toggle(ctx, toggle=None):
    if ctx.author.guild_permissions.administrator:
        if toggle != None:
            if toggle == 'bw':
                global bw_offen
                if bw_offen == False:
                    bw_offen = True
                    await ctx.send('<:JC_check:826282165423046666> **Bewerbungen geöffnet.**')
                else:
                    bw_offen = False
                    await ctx.send('<:JC_check:826282165423046666> **Bewerbungen geschlossen.**')
            elif toggle == 'mod':
                global mod_enabled
                if mod_enabled == False:
                    mod_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **Moderationsbefehle aktiviert.**')
                else:
                    mod_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **Moderationsbefehle deaktiviert.**')
            elif toggle == 'rp':
                global rp_enabled
                if rp_enabled == False:
                    rp_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **RP-Befehle aktiviert.**')
                else:
                    rp_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **RP-Befehle deaktiviert.**')
            elif toggle == 'fun':
                global fun_enabled
                if fun_enabled == False:
                    fun_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **Fun-Befehle aktiviert.**')
                else:
                    fun_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **Fun-Befehle deaktiviert.**')
            elif toggle == 'vc':
                global vc_enabled
                if vc_enabled == False:
                    vc_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **Das Custom-VC System wurde aktiviert.**')
                else:
                    vc_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **Das Custom-VC System wurde deaktiviert.**')
            elif toggle == 'casino':
                global casino_enabled
                if casino_enabled == False:
                    casino_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **Das Casinosystem wurde aktiviert.**')
                else:
                    casino_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **Das Casinosystem wurde deaktiviert.**')
            elif toggle == 'welcome':
                global welcome_enabled
                if welcome_enabled == False:
                    welcome_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **Das Willkommenssystem wurde aktiviert.**')
                else:
                    welcome_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **Das Willkommenssystem wurde deaktiviert.**')
            elif toggle == 'lvl':
                global lvl_enabled
                if lvl_enabled == False:
                    lvl_enabled = True
                    await ctx.send('<:JC_check:826282165423046666> **Das Levelsystem wurde aktiviert.**')
                else:
                    lvl_enabled = False
                    await ctx.send('<:JC_check:826282165423046666> **Das Levelsystem wurde deaktiviert.**')
        else:
            if bw_offen == True:
                bw_offen = 'Offen'
            else:
                bw_offen = 'Geschlossen'
            if mod_enabled == True:
                mod_enabled = 'Aktiviert'
            else:
                mod_enabled = 'Deaktiviert'
            if rp_enabled == True:
                rp_enabled = 'Aktiviert'
            else:
                rp_enabled = 'Deaktiviert'
            if fun_enabled == True:
                fun_enabled = 'Aktiviert'
            else:
                fun_enabled = 'Deaktiviert'
            if vc_enabled == True:
                vc_enabled = 'Aktiviert'
            else:
                vc_enabled = 'Deaktiviert'
            if casino_enabled == True:
                casino_enabled = 'Aktiviert'
            else:
                casino_enabled = 'Deaktiviert'
            if lvl_enabled == True:
                lvl_enabled = 'Aktiviert'
            else:
                lvl_enabled = 'Deaktiviert'
            await ctx.send('**Du kannst folgende Systeme togglen:**\r\n\r\n'
                           f'`bw` - *Bewerbungen* ({bw_offen})\r\n'
                           f'`mod` - *Moderation* ({mod_enabled})\r\n'
                           f'`fun` - *Fun commands* ({mod_enabled})\r\n'
                           f'`vc` - *Custom-Voice* ({mod_enabled})\r\n'
                           f'`casino` - *Casino* ({mod_enabled})\r\n'
                           f'`lvl` - *Level* ({mod_enabled})\r\n'
                           f'`rp` - *Roleplay* ({rp_enabled})\r\n\r\n'
                           '`Nutze ,toggle <system> um die Systeme zu togglen.`')
    else:
        await ctx.reply('<:JC_xmark:826282095566913537> **Du du verfügst nicht über die notwendigen Berechtigungen.**')


#afk_list = []

last_counter = None
last_negative = None
last_num = 0
one_word_counter = 0
last_sender = None
sentence = []
guessthenumber = 0

with open("./JOBCENTER/jc_afk.json") as f:
    afk_list = json.load(f)
@client.event
async def on_message(message):
    logchannel = client.get_channel(884507838645428224)
    global wartungsarbeiten
    if wartungsarbeiten == True:
        if message.author.id != 515602740500627477 and message.author.id != 753009216767393842:
            if message.content.startswith(','):
                await message.reply("<:JC_xmark:826282095566913537> Derzeit kann der Bot aufgrund von Wartungsarbeiten nur von auserwählten Personen verwendet werden.")
                return
    if message.author.bot:
        return
    if message.guild.id != 776912251944435723 or not message.guild:
        if message.content.startswith(','):
            await message.channel.send('<:JC_xmark:826282095566913537> Der Bot funktioniert nur auf dem **JOBCENTER** Discord Server und ist nur auf ihn spezialisiert.')
            return
    if message.channel.id == 889926544510832640:
        global guessthenumber
        if message.content != '0':
            if message.content == str(guessthenumber):
                role = client.get_guild(776912251944435723).get_role(868012490871697448)
                await message.reply(f'{message.author.mention} **hat die richtige Zahl erraten!**\r\n*Sie lautete*: `{guessthenumber}`')
                await message.channel.set_permissions(role, send_messages=False, view_channel=True)
                guessthenumber = 0
    if message.channel.id == 841759769643581492:
        if not message.attachments:
            await message.delete()
    ### Ticket-System Add-On
    if message.channel.category_id == 868012518658965574:
        with open("./JOBCENTER/jc_tickets.json") as f:
            data = json.load(f)
        with open("./JOBCENTER/jc_ticket_claimed.json") as f:
            data2 = json.load(f)
        if message.channel.name.startswith('ticket-'):
            if message.author.guild_permissions.manage_messages:
                logchannel = client.get_channel(868012587936268369)
                await message.channel.set_permissions(message.author, read_messages=True, send_messages=True)
                await message.channel.set_permissions(message.guild.default_role, read_messages=False, send_messages=False)
                embed = discord.Embed(description=f'{message.author.mention} wird sich ab jetzt um dich kümmern.', color=discord.Color.gold())
                ticket_number = int(data["ticket-counter"])
                await message.channel.edit(name=f'claimed-{ticket_number}')
                msg = await message.channel.send(embed=embed)
                if not str(message.author.id) in data2:
                    data2[str(message.author.id)] = 1
                    with open("./JOBCENTER/jc_ticket_claimed.json", 'w') as f:
                        json.dump(data2, f, indent=4)
                else:
                    data2[str(message.author.id)] += 1
                    with open("./JOBCENTER/jc_ticket_claimed.json", 'w') as f:
                        json.dump(data2, f, indent=4)
                logembed = discord.Embed(title='Log - Ticket übertragen', description=f'Das Ticket **#{message.channel.name}** ({message.channel.mention}) wurde an **{message.author}** übertragen.', color=discord.Colour.gold())
                await logchannel.send(embed=logembed)
    ### Ticket-System Add-On Ende
    if message.channel.id == 859769240163844136:
        if fun_enabled != False:
            global last_counter
            global last_num
            try:
                if message.author != last_counter:
                    if int(message.content) > last_num and int(message.content) < last_num+2:
                        last_num += 1
                        last_counter = message.author
                    else:
                        await message.add_reaction('a:denied:859772905024651294')
                        await message.channel.send('Falsche Nummer. Restart!')
                        last_num = 0
                        last_counter = None
                else:
                    await message.add_reaction('a:denied:859772905024651294')
                    await message.channel.send('Du kannst nicht meherere Zahlen hintereinander zählen. Restart!')
                    last_num = 0
                    last_counter = None
            except:
                if not message.author.guild_permissions.manage_channels:
                    await message.delete()
                    last_negative = message.author
                    try:
                        if last_negative == message.author:
                            await message.channel.set_permissions(message.author, send_messages=False)
                            await message.author.send(f'**Du bist mit sofortiger Wirkung aus {message.channel.mention} ausgeschlossen.**')
                        else:
                            await message.author.send(f'**Bitte sende in {message.channel.mention} nur Nummern.**')
                    except:
                        await message.channel.send(f'{message.author.mention}, **Bitte sende in {message.channel.mention} nur Nummern.**', delete_after=10)
    if message.channel.id == 868012625353654283:
        if fun_enabled != False:
            global one_word_counter
            global last_sender
            global sentence
            args = message.content.split(' ')
            if len(args) == 1:
                if '@' in message.content:
                    await message.channel.send('Bitte vermeide das erwähnen von Rollen oder Membern.', delete_after=10)
                    await message.delete()
                elif 'http' in message.content:
                    await message.channel.send('Bitte verwende keine Links.', delete_after=10)
                    await message.delete()
                elif 'discord.gg/' in message.content:
                    await message.channel.send('Bitte verwende keine Discord Invites.', delete_after=10)
                    await message.delete()
                elif message.author != last_sender:
                    ### Savings
                    one_word_counter += 1
                    last_sender = message.author
                    sentence.append(message.content)
                    ### Endings
                    if message.content.endswith('.'):
                        if one_word_counter > 3:
                            await message.channel.send('**(Neue Story, da diese mit einem `.` beendet wurde.)**\r\n'
                                                       '---------------------')
                            one_word_counter = 0
                            last_sender = None
                            channel = client.get_channel(868012624313483304)
                            await channel.send(' '.join(sentence))
                            sentence = []
                else:
                    await message.delete()
                    try:
                        await message.author.send(f'Bitte halte dich daran, das du nicht mehrere wörter hintereinander senden darfst.')
                    except:
                        await message.channel.send(f'{message.author.mention} bitte halte dich daran, dass du nicht mehrere wörter hintereinander senden darfst.', delete_after=10)
            else:
                await message.delete()
                try:
                    await message.author.send(f'Bitte halte dich daran, dass dies eine **One Word Story** ist.\r\nHier darf nur 1 Wort pro Nachricht gesendet werden.')
                except:
                    await message.channel.send(f'{message.author.mention} bitte halte dich daran, dass dies eine **One Word Story** ist.\r\nHier darf nur 1 Wort pro Nachricht gesendet werden.', delete_after=10)
    with open("./JOBCENTER/jc_blacklist.json") as f:
        blacklist = json.load(f)
    for bad_word in blacklist["words"]:
        if bad_word in message.content.lower():
            if not message.author.guild_permissions.manage_messages:
                await message.delete()
                await message.channel.send(f'**{message.author.mention} bitte achte auf deine Wortwahl!**', delete_after=10)
                embed = discord.Embed(title='Automod', description=f'Nachricht von {message.author.mention} aufgrund der Blacklist gelöscht.', color=discord.Colour.red())
                embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                embed.set_footer(text=client.user.name + ' - Logs', icon_url=client.user.avatar_url)
                embed.add_field(name='Content:', value=f'```{message.content}```')
                await logchannel.send(embed=embed)
    whitelist = []
    if 'discord.gg/' in message.content:
        if not message.author.id in whitelist:
            if not message.author.guild_permissions.manage_messages:
                await message.channel.send('Bitte verwende keine Discord Invites.', delete_after=10)
                await message.delete()
    if 'http' in message.content:
        if not message.author.id in whitelist:
            if not message.author.guild_permissions.manage_messages:
                if not message.content.startswith('https://tenor.com/') and not message.content.startswith('https://giphy.com/'):
                    await message.delete()
                    try:
                        await message.author.send(f':x: **Bitte versende keine Links in {message.channel.name}.**')
                    except:
                        await message.author.send(f':x: **{message.author.mention}, bitte versende keine Links in diesem Channel.**')
    watchoutrole = client.get_guild(776912251944435723).get_role(868012491672784907)
    securerole = client.get_guild(776912251944435723).get_role(868050031264010281)
    if watchoutrole in message.author.roles:
        
        def membercheck(m):
            return m.author == message.author and m.channel == message.channel
        
        try:
            spamwait1 = await client.wait_for('message', timeout=10, check=membercheck)
            lastmsg = await message.channel.fetch_message(message.channel.last_message_id)
            removed_roles = []
            if lastmsg.content == message.content:
                for allroles in message.author.roles:
                    try:
                        removed_roles.append(allroles.name)
                        await message.author.remove_roles(allroles)
                    except:
                        pass
                await message.author.add_roles(securerole, reason='Security System triggered')
                await message.channel.send(f'Security System triggered. Target: **{message.author}** - Reason: `Same message several times`. - Action Taken: *User quarantined*.')
                embed = discord.Embed(title='Security System triggered', description=f'Target: **{message.author}** - Reason: `Same message several times`. - Action Taken: *User quarantined*.')
                embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                embed.set_footer(text='Jobcenter - Mod Logs', icon_url=client.user.avatar_url)
                embed.add_field(name='Roles removed:', value='`-`' + "\n`-` ".join(removed_roles))
                await logchannel.send(embed=embed)
                return
            spamwait2 = await client.wait_for('message', timeout=0.5, check=membercheck)
            for allroles in message.author.roles:
                try:
                    removed_roles.append(allroles.name)
                    await message.author.remove_roles(allroles)
                except:
                    pass
            await message.author.add_roles(watchoutrole, reason='Security System triggered')
            await message.author.add_roles(securerole, reason='Security System triggered')
            await message.channel.send(f'Security System triggered. Target: **{message.author}** - Reason: `Spamming`. - Action Taken: *User quarantined*.')
            embed = discord.Embed(title='Security System triggered', description=f'Target: **{message.author}** - Reason: `Spamming`. - Action Taken: *User quarantined*.')
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text='Jobcenter - Mod Logs', icon_url=client.user.avatar_url)
            embed.add_field(name='Roles removed:', value='`-`' + "\n`-` ".join(removed_roles))
            await logchannel.send(embed=embed)
        except asyncio.TimeoutError:
            return
          
    if lvl_enabled != False:
        with open('./JOBCENTER/jc_lvl_users.json', 'r') as f:
            users = json.load(f)
    
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)
    
        with open('./JOBCENTER/jc_lvl_users.json', 'w') as f:
            json.dump(users, f)

    if message.author == client.user:
	    return
    if not message.guild:
	    return
    with open("./JOBCENTER/jc_afk.json") as f:
        afk_list = json.load(f)
    if f"{message.author.id}" in afk_list:
        afk_list.pop(f"{message.author.id}")
        if message.author.display_name.startswith('[AFK] '):
            nickname = message.author.display_name
            await message.author.edit(nick=nickname[6:])
            pass
        else:
            pass
        await message.channel.send('Willkommen zurück {}, Ich habe deinen AFK Status entfernt.'.format(message.author.mention), delete_after=10)
        with open('./JOBCENTER/jc_afk.json', 'w') as f:
            json.dump(afk_list, f, indent=4)
    mentioned = message.mentions
    for user in mentioned:
        if f"{user.id}" in afk_list:
            await message.channel.send(f'**{user}** ist derzeit AFK: {afk_list[f"{user.id}"]}')
    muterole = client.get_guild(776912251944435723).get_role(868012378955075614)
    if muterole in message.author.roles:
        return
    await client.process_commands(message)
    

async def update_data(users, user):
    if lvl_enabled == False:
        return
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        
async def add_experience(users, user, exp):
    if lvl_enabled == False:
        return
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    if lvl_enabled == False:
        return
    with open('./JOBCENTER/jc_level.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} ist jetzt **Lvl `{lvl_end}`**')
        users[f'{user.id}']['level'] = lvl_end

@client.command(aliases=['lvl', 'rank'])
async def level(ctx, member: discord.Member = None):
    if lvl_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Das Levelsystem wurde vom Team vorübergehend deaktiviert!**')
        return
    if not member:
        id = ctx.message.author.id
        with open('./JOBCENTER/jc_lvl_users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        exp = users[str(id)]['experience']
        await ctx.send(f'Du bist derzeit Level **{lvl}** `{exp}xp`!')
    else:
        id = member.id
        with open('./JOBCENTER/jc_lvl_users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        exp = users[str(id)]['experience']
        await ctx.send(f'**{member}** ist derzeit Level **{lvl}** `{exp}xp`!')
    

@client.command()
async def startevent(ctx, event, arg=None):
    eventrole = client.get_guild(776912251944435723).get_role(868012374781751437)
    global guessthenumber
    if ctx.author.guild_permissions.manage_messages or eventrole in ctx.author.roles:
        if event.lower() == 'gtn' or event.lower() == 'guessthenumber' or event.lower() == 'guesser':
            channel = client.get_channel(889926544510832640)
            role = client.get_guild(776912251944435723).get_role(868012490871697448)
            guessthenumber = int(arg)
            await channel.send(f'> **Guess the Number**\r\n\r\nDas Event hat begonnen, errate die Zahl!')
            await channel.set_permissions(role, send_messages=True, view_channel=True)
            await ctx.message.add_reaction('✅')


botlist = []

@client.command()
async def whitelist(ctx, user: discord.User):
    global botlist
    if ctx.author.id == 753009216767393842:
        if not user.id in botlist:
            botlist.append(user.id)
            await ctx.send(f'**{user}** wurde zur Whitelist hinzugefügt.')
        else:
            botlist.remove(user.id)
            await ctx.send(f'**{user}** wurde von der Whitelist entfernt.')
    

@client.command()
async def blacklist(ctx, *, word: str=None):
    if ctx.author.guild_permissions.manage_guild:
        with open("./JOBCENTER/jc_blacklist.json") as f:
            liste = json.load(f)
        if word == None:
            embed = discord.Embed(title='Blacklist', description="- `" + "`\n- `".join(liste["words"]) + "`", color=0xE31316)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        elif word not in liste["words"]:
            liste["words"].append(str(word.lower()))
            with open('./JOBCENTER/jc_blacklist.json', 'w') as f:
                json.dump(liste, f, indent=4)
            await ctx.send(f'`{word}` wurde zur Blacklist hinzugefügt!')
        else:
            liste["words"].remove(str(word.lower()))
            with open('./JOBCENTER/jc_blacklist.json', 'w') as f:
                json.dump(liste, f, indent=4)
            await ctx.send(f'`{word}` wurde von der Blacklist entfernt!')



@client.command(name='afk')
async def afk(ctx, *, reason=None):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if reason == None:
        reason = 'AFK'
    if '@everyone' in reason:
        await ctx.send('Denk erst garnicht daran `@ everyone` zu pingen.')
    elif '@here' in reason:
        await ctx.send('Denk erst garnicht daran `@ here` zu pingen.')
    elif '@' in reason:
        await ctx.send('Bitte vermeide das erwähnen von Rollen oder Membern.')
    elif 'http' in reason:
        await ctx.send('Bitte verwende keine Links.')
    elif 'discord.gg/' in reason:
        await ctx.send('Bitte verwende keine Discord Invites.')
    else:
        try:
            oldnick = ctx.author.display_name
            if not ctx.author.display_name.startswith('[AFK]'):
                await ctx.author.edit(nick=f'[AFK] {oldnick}')
                pass
        except:
            pass
        await ctx.send(f'{ctx.author.mention} ich habe dich AFK gesetzt: {reason}')
        newafk = {ctx.author.id: reason}
        with open('./JOBCENTER/jc_afk.json', 'w') as f:
            json.dump(newafk, f, indent=4)

@client.command(name='setafk')
async def setafk(ctx, user: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.manage_messages:   
        if fun_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
            return
        if reason == None:
            reason = 'AFK'
        if user.guild_permissions.manage_messages:
            await ctx.send('Du kannst den AFK Status eines Teammitgliedes nicht verwalten.')
        elif '@everyone' in reason:
            await ctx.send('Denk erst garnicht daran `@ everyone` zu pingen.')
        elif '@here' in reason:
            await ctx.send('Denk erst garnicht daran `@ here` zu pingen.')
        elif '@' in reason:
            await ctx.send('Bitte vermeide das erwähnen von Rollen oder Membern.')
        elif 'http' in reason:
            await ctx.send('Bitte verwende keine Links.')
        elif 'discord.gg/' in reason:
            await ctx.send('Bitte verwende keine Discord Invites.')
        elif user.voice:
            await ctx.send('Du kannst niemanden AFK stellen während er sich in einem Voice befindet.')
        else:
            #afk_list.append(ctx.message.author.id)
            await ctx.send(f'{ctx.author.mention} ich habe **{user}** AFK gesetzt: {reason}')
            newafk = {user.id: reason}
            with open('./JOBCENTER/jc_afk.json', 'w') as f:
                json.dump(newafk, f, indent=4)

@client.command(name='clearafk')
async def clearafk(ctx, user: discord.Member):
    if ctx.author.guild_permissions.manage_messages:
        if f"{user.id}" in afk_list:
            afk_list.pop(f"{user.id}")
            await ctx.send('Willkommen zurück, Ich habe deinen AFK Status von **{}** entfernt.'.format(user))
            with open('./JOBCENTER/jc_afk.json', 'w') as f:
                json.dump(afk_list, f, indent=4)
        else:
            await ctx.send(f'{ctx.author.mention}, **{user}** ist derzeit nicht AFK.')


@client.command()
@commands.check(check_team)
async def re(ctx, member: discord.User, *, text):
    #de = pytz.timezone('Europe/Berlin')

    embed = discord.Embed(
        colour=discord.Colour.greyple(),
        title='Message received',
        description=f'{text}'
    )

    embed.set_footer(text=f'Message from {ctx.author.name}.', icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await member.send(embed=embed)
    await ctx.message.add_reaction('✅')


@client.command()
async def buttontest(ctx):
    await ctx.send("Test des Buttons", components = [Button(label = "Ein Knopf!")])

    interaction = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("Ein"))
    await interaction.respond(content = "Knopf gedrückt")


@client.command()
async def bannertest(ctx):
    server = client.get_guild(776912251944435723)
    background = Image.open("./JOBCENTER/Serverbanner.png")
    font = ImageFont.truetype("./JOBCENTER/HotBleb.ttf", 14)
    W, H = (256, 143)

    draw = ImageDraw.Draw(background)
    text = str(server.member_count)
    text2 = str(server.premium_subscription_count)

    w, h = draw.textsize(text)
    draw.text(((W-w)/2 - 80,(H-h)/2 + 55), text, (255, 255, 255), font=font)
    w, h = draw.textsize(text2)
    draw.text(((W-w)/2 + 85,(H-h)/2 + 55), text2, (255, 255, 255), font=font)
    background.save("./JOBCENTER/newServerBanner.png")

    await ctx.send(file=discord.File("./JOBCENTER/newServerBanner.png"))


@client.command()
async def welcometest(ctx, user: discord.User=None):
    if user == None:
        user = ctx.author
    background = Image.open("./JOBCENTER/BG.png")
    mask = Image.open('./JOBCENTER/mask.png')
    font = ImageFont.truetype("./JOBCENTER/arial.ttf", 20)
    W, H = (500, 280)

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((100,100))
    draw = ImageDraw.Draw(background)
    text = user.name

    circle_image = Image.new('L', (100, 100))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, 100, 100), fill=255)
    background.paste(pfp, (200,50), circle_image)

    w, h = draw.textsize(text)
    draw.text(((W-w)/2 - 15,(H-h)/2 + 25), text, (215, 0, 0), font=font)
    background.save("./JOBCENTER/welcome.png")

    await ctx.send(file=discord.File("./JOBCENTER/welcome.png"))


#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandNotFound):
#        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description=f'**Dieser Befehl (`{ctx.message.content}`) wurde nicht gefunden. Bitte überprüfe deine Rechtschreibung und versuche es erneut.**', color=0xff0000)
#        embed.set_footer(text='Für eine Liste aller Befehle, führe bitte den Befehl +help aus.')
#        await ctx.send(embed=embed)


@client.command(name='help')
async def help(ctx):
    dev = client.get_user(515602740500627477)
    prefix = ...
    embed = discord.Embed(title='Helpdesk', description='Mein Prefix  ist `,`.\r\n\r\n`Triff eine Auswahl um zu beginnen.`', color=0xE31316)
    embed.set_footer(text='Bot by: ' + dev.name + '#' + dev.discriminator, icon_url=dev.avatar_url)
    msg = await ctx.send(embed=embed, components=[Select(placeholder="Wähle einen Bereich", options=[SelectOption(label="🔰 Moderation", value="mod"), SelectOption(label="🔨 Utility", value="utility"), SelectOption(label="👮‍♂️ Management", value="manage"), SelectOption(label="🚨 Team Befehle", description='Diesen Bereich können nur Teammitglieder einsehen.', value="staff")])])
    
    def check(interaction):
        return interaction.channel == ctx.channel and interaction.message == msg

    try:
        while True:
            interaction = await client.wait_for("select_option", check=check, timeout=30)
            #if ctx.author == interaction.user:
            #    ...
            #else:
            #    await interaction.respond(content='Du bist nicht derjenige der den Befehl ausgeführt hat. 😡', hidden=True)
            #    return
            if interaction.component[0].value == "mod":
                embed = discord.Embed(title='Moderation Commands', description="`,ban` - **Bannt einen Nutzer.**\r\n"
                                                                               "`,unban` - **Entbannt einen Nutzer.**\r\n"
                                                                               "`,quarantine` - **Steckt einen Nutzer in Quarantäne.**\r\n"
                                                                               "`,release` - **Holt einen Nutzer aus Quarantäne.**\r\n"
                                                                               "`,mute` - **Muted einen Nutzer.**\r\n"
                                                                               "`,unmute` - **Entmuted einen Nutzer.**", color=0xE31316)
                await interaction.respond(embed=embed)
            if interaction.component[0].value == "utility":
                embed = discord.Embed(title='Fun und Utility Commands', description='', color=0xE31316)
                await interaction.respond(embed=embed)
            if interaction.component[0].value == "manage":
                embed = discord.Embed(title='Management Commands', description='', color=0xE31316)
                await interaction.respond(embed=embed)
            if interaction.component[0].value == "custom":
                embed = discord.Embed(title='Custom und RP Commands', description='', color=0xE31316)
                await interaction.respond(embed=embed)
            if interaction.component[0].value == "staff":
                teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
                intmember = interaction.user
                member = client.get_user(intmember.id)
                if teamrole in client.get_guild(ctx.guild.id).get_member(intmember.id).roles:
                    embed = discord.Embed(title='Team Commands', description='**Allgemeines:** \r\n'
                                                                             '\r\n'
                                                                             'Eine Rolle erstellen```,addrole <name>```\r\n'
                                                                             'Jemandem eine Rolle geben```,role <user> <role id>```\r\n'
                                                                             'Rollen Farbe einer Rolle ändern. (bei Hex Code ohne "#")```,rolecolor <role id> <hex>```\r\n'
                                                                             'Rollen Name einer Rolle ändern```,rolename <role id> <name>```\r\n'
                                                                             '***Diese Commands könnt ihr auch mit den Slash Befehlen machen (ist einfacher)***\r\n'
                                                                             '\r\n'
                                                                             '\r\n'
                                                                             '**Moderation:**\r\n'
                                                                             '\r\n'
                                                                             'eine Person stummen und entstummen```,mute <user> <zeit> <grund>\r\n'
                                                                             ',unmute <user> <grund>```\r\n'
                                                                             'eine Person vom Server bannen und entbannen```,ban <user> <grund> \r\n'
                                                                             ',unban <user> <grund>```\r\n'
                                                                             'einer Person die in der Sicherheitskontrolle ist Zugriff auf den Server geben```,release <user>```\r\n'
                                                                             '\r\n'
                                                                             '\r\n'
                                                                             '**Tickets:** (funktionieren nur in Ticket-Kanälen)\r\n'
                                                                             '\r\n'
                                                                             'Ticket schließen ```,close```\r\n'
                                                                             'eine Person zum Ticket hinzufügen```,adduser <user>```\r\n'
                                                                             'eine Person zum Ticket entfernen```,remove <user>```', color=0xE31316)
                    embed.set_footer(text='Restricted')
                    await interaction.respond(embed=embed)
                else:
                    await interaction.respond(content='*Du bist nicht berechtigt diesen Bereich einzusehen.*')
    except asyncio.TimeoutError:
        await msg.edit(components=[Select(placeholder="Timed out", options=[SelectOption(label="Timed out", value="timeout")], disabled=True)])

@client.command(name='reminder')
async def reminder(ctx, time: int, *, reminder: str):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.send(f'**Ich werde dich in `{time}` Sekunden erinnern:** {reminder}')
        await asyncio.sleep(time)
        embed = discord.Embed(title='Erinnerung', description=f'{reminder}', timestamp=ctx.message.created_at, color=0xE31316)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text='Erinnerung erstellt')
        await ctx.send(f"{ctx.author.mention}", embed=embed)


@client.command(name='suggest')
@commands.cooldown(1, 300, type=BucketType.user)
async def suggest(ctx, *, suggestion: str):
    channel = client.get_channel(868012626951680010)
    embed = discord.Embed(description=str(suggestion), timestamp=datetime.now(), color=0xE31316)
    embed.set_author(name=f'Vorschlag von {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text='Eingereicht am')
    #embed.add_field(name='Votes', value='Meinung: 0\r\nUpvotes: 0\r\nDownvotes: 0')
    msg = await channel.send(embed=embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('🤷')
    await msg.add_reaction('👎')
    await ctx.message.add_reaction('✅')


@client.command(name='echo')
@commands.cooldown(1, 5, type=BucketType.user)
async def echo(ctx, channel: discord.TextChannel, *, message):
    if ctx.author.guild_permissions.manage_roles:
        await channel.send(message)
        await ctx.message.add_reaction('✅')


@client.command(name='startpoll', aliases=['sendpoll'])
@commands.cooldown(1, 30, type=BucketType.user)
async def startpoll(ctx):#, *, message
    if ctx.author.guild_permissions.manage_messages:
        channel = client.get_channel(870654826848075826)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            await ctx.send('Wie lautet die Frage?\r\n(`cancel` zum abbrechen)')
            question = await client.wait_for('message', timeout=120.0, check=check)
            if question.content.lower() == 'cancel':
                await ctx.send('<:JC_xmark:826282095566913537> **Aktion abgebrochen!**')
                return
            await ctx.send('Wie lautet die erste Antwortmöglichkeit?')
            answer1 = await client.wait_for('message', timeout=120.0, check=check)
            if answer1.content.lower() == 'cancel':
                await ctx.send('<:JC_xmark:826282095566913537> **Aktion abgebrochen!**')
                return
            await ctx.send('Wie lautet die zweite Antwortmöglichkeit?')
            answer2 = await client.wait_for('message', timeout=120.0, check=check)
            if answer2.content.lower() == 'cancel':
                await ctx.send('<:JC_xmark:826282095566913537> **Aktion abgebrochen!**')
                return
            msg = await channel.send("[<@&870659091809304606>]\r\n**" + str(question.content) + "**\r\n:a: *" + str(answer1.content) + "*\r\noder\r\n :b: *" + str(answer2.content) + "*")
            await msg.add_reaction('🅰')
            await msg.add_reaction('🅱')
            await answer2.add_reaction('✅')
        except asyncio.TimeoutError:
            await ctx.message.reply('<:JC_xmark:826282095566913537> **Timed out!**')
            return


@client.command(name='say')
@commands.cooldown(1, 30, type=BucketType.user)
async def say(ctx, *, message):
    if ctx.author.guild_permissions.administrator:
        await ctx.send(message)
        await ctx.message.delete()
    elif '@everyone' in message:
        await ctx.send('Denk erst garnicht daran `@ everyone` zu pingen.')
    elif '@here' in message:
        await ctx.send('Denk erst garnicht daran `@ here` zu pingen.')
    elif '@' in message:
        await ctx.send('Bitte vermeide das erwähnen von Rollen oder Membern.')
    elif 'http' in message:
        await ctx.send('Bitte verwende keine Links.')
    elif 'discord.gg/' in message:
        await ctx.send('Bitte verwende keine Discord Invites.')
    else:
        await ctx.send(message)
        await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    prefix = '!'
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Es fehlt ein wichtiges Argument.**', color=0xff0000)
        embed.add_field(name='Usage', value=f'`{prefix}say <message>`')
        await ctx.send(embed=embed)


@client.command(name='addreaction', aliases=['react'])
async def addreaction(ctx, msgid: int, emoji: str):
    if ctx.author.guild_permissions.manage_messages:
        msg = await ctx.fetch_message(msgid)
        if msg:
            await msg.add_reaction(emoji)
            await ctx.message.add_reaction('✅')


@client.command(name='sendembed')
async def sendembed(ctx, *, message):
    if ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(description=message, color=0xE31316)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    elif 'http' in message:
        await ctx.send('Bitte verwende keine Links.')
    elif 'discord.gg/' in message:
        await ctx.send('Bitte verwende keine Discord Invites.')
    else:
        embed = discord.Embed(description=message, color=0xE31316)
        await ctx.send(embed=embed)
        await ctx.message.delete()


@client.command(name='vcembed', hidden=True)
async def vcembed(ctx, *, message):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(description=message, color=0xE31316)
        #embed.set_author(name='🎙 V O I C E - C R E A T E')
        embed.set_footer(text='Verbinde dich mit einem Custom-Channel um die Befehle verwenden zu können. ')
        msg = await ctx.send(embed=embed, components=[[Button(style=2, label='Lock', custom_id="lock"), Button(style=2, label='Unlock', custom_id="unlock"), Button(style=2, label='Hide', custom_id="hide"), Button(style=2, label='Unhide', custom_id="unhide"), Button(style=4, label='Delete', custom_id="delete")]])
        await ctx.message.delete()


@client.command(name='ticketembed', hidden=True)
async def ticketembed(ctx, *, message):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(description=message, color=0xE31316)
        embed.set_author(name='🎫 Ticket Support')
        embed.set_footer(text='Klicke auf die Reaktion um zu beginnen.')
        msg = await ctx.send(embed=embed, components=[Button(style=2, label='🎫 Ticket erstellen')])
        await ctx.message.delete()
        #await msg.add_reaction('🎫')


@client.command(name='selfnick')
async def selfnick(ctx, *, newnick):
    username = client.get_guild(ctx.guild.id).get_member(client.user.id)
    await username.edit(nick=newnick)
    embed = discord.Embed(title="Nichname", description=f"Ich habe mein Nichname auf **{newnick}** geändert.", color=discord.Color.dark_red())
    await ctx.send(embed=embed)
    await ctx.message.delete()


@client.command(name='logout')
async def logout(ctx):
    if(ctx.author.id == 515602740500627477):
        embed = discord.Embed(description='**Bot wird ausgeloggt...**', color=0xff0000)
        await ctx.send(embed=embed)
        await client.logout()


@client.command(name='ping')
async def ping(ctx):
    await ctx.send('**Pong!** :ping_pong: __**{0}s**__'.format(round(client.latency, 3)))


@client.command(name='devback')
async def devback(ctx):
    if ctx.author.id == 515602740500627477:
        role = client.get_guild(776912251944435723).get_role(884490052250533940)
        await ctx.author.add_roles(role)
        await ctx.reply(f'Willkommen zurück! Alle Systeme unverändert.')


@client.command(aliases=['getemoji', 'getemote'])
async def emoji(ctx, emoji: discord.PartialEmoji):
    if emoji.animated:
        await ctx.send('https://cdn.discordapp.com/emojis/' + str(emoji.id) + '.gif?v=1')
    else:
        await ctx.send('https://cdn.discordapp.com/emojis/' + str(emoji.id) + '.png?v=1')


@client.command(aliases=['stealemoji', 'stealemote'])
async def steal(ctx, emoji: discord.PartialEmoji, name: str=None):
    a = ""
    emojiformat = emoji.url_as(format='png')
    if emoji.animated:
        a = "a"
        emojiformat = emoji.url_as(format='gif')
    if name == None:
        name = emoji.name
    newemoji = await ctx.guild.create_custom_emoji(name=name, image=emojiformat)
    await ctx.send(f"<:JC_check:826282165423046666> Successfully added the emoji <{a}:{newemoji.name}:{newemoji.id}> with the name `{newemoji.name}`!")


@slash.slash(name="role",
             description="Vergebe oder entferne eine Rolle von einem Mitglied.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="member",
                    description="Erwähne ein Mitglied.",
                    option_type=6,
                    required=True
                ),
                create_option(
                    name="role",
                    description="Erwähne eine Rolle.",
                    option_type=8,
                    required=True
                ),
                create_option(
                    name="time",
                    description="Die Zeit der bestehung der Rolle in Sekunden.",
                    option_type=4,
                    required=False
                )
             ])
async def _role(ctx: SlashContext, member: discord.Member, role: discord.Role, time: int=None):
    if mod_enabled == False:
        await ctx.send('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**', hidden=True)
        return
    if ctx.author.guild_permissions.manage_messages:
        if role in ctx.guild.roles:
            if ctx.author.top_role.position-1 >= role.position:
                botrole = ctx.guild.me
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde von {member.mention} entfernt.', color=0xE31316)
                    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    if time != None:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde {member.mention} für **{time}s** hinzugefügt.', color=0xE31316)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(time)
                        await member.remove_roles(role)
                        logchannel = client.get_channel(884507838645428224)
                        logembed = discord.Embed(description=f'{role.mention} wurde {member.mention} für **{time}s** hinzugefügt.', color=discord.Colour.blurple())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)

                    else:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde {member.mention} hinzugefügt.', color=0xE31316)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        logchannel = client.get_channel(884507838645428224)
                        logembed = discord.Embed(description=f'{role.mention} wurde {member.mention} hinzugefügt.', color=discord.Colour.blurple())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
            else:
                embed = discord.Embed(description=f'<:JC_xmark:826282095566913537> Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
                embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(hidden=True, embed=embed)
        else:
            embed = discord.Embed(description=f'<:JC_xmark:826282095566913537> Diese Rolle "**{role}**" wurde nicht gefunden.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(hidden=True, embed=embed)


@client.command(name='role')
async def role(ctx, member: discord.Member, role: discord.Role, time: int=None):
    if ctx.author.guild_permissions.manage_messages:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        if role in ctx.guild.roles:
            if ctx.author.id == 515602740500627477:
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde von {member.mention} entfernt.', color=0xE31316)
                    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    await ctx.send(embed=embed)
                    logchannel = client.get_channel(884507838645428224)
                    logembed = discord.Embed(description=f'{role.mention} wurde von {member.mention} entfernt.', color=discord.Colour.blurple())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)
                else:
                    if time != None:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde {member.mention} für **{time}s** hinzugefügt.', color=0xE31316)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(time)
                        await member.remove_roles(role)
                        logchannel = client.get_channel(884507838645428224)
                        logembed = discord.Embed(description=f'{role.mention} wurde {member.mention} für **{time}s** hinzugefügt.', color=discord.Colour.blurple())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)

                    else:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde {member.mention} hinzugefügt.', color=0xE31316)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        logchannel = client.get_channel(884507838645428224)
                        logembed = discord.Embed(description=f'{role.mention} wurde {member.mention} hinzugefügt.', color=discord.Colour.blurple())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
            elif ctx.author.top_role.position-1 >= role.position:
                botrole = ctx.guild.me
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde von {member.mention} entfernt.', color=0xE31316)
                    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    await ctx.send(embed=embed)
                    logchannel = client.get_channel(884507838645428224)
                    logembed = discord.Embed(description=f'{role.mention} wurde von {member.mention} entfernt.', color=discord.Colour.blurple())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)
                else:
                    if time != None:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde {member.mention} für **{time}s** hinzugefügt.', color=0xE31316)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(time)
                        await member.remove_roles(role)
                        logchannel = client.get_channel(884507838645428224)
                        logembed = discord.Embed(description=f'{role.mention} wurde {member.mention} für **{time}s** hinzugefügt.', color=discord.Colour.blurple())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)

                    else:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'<:JC_check:826282165423046666> {role.mention} wurde {member.mention} hinzugefügt.', color=0xE31316)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        logchannel = client.get_channel(884507838645428224)
                        logembed = discord.Embed(description=f'{role.mention} wurde {member.mention} hinzugefügt.', color=discord.Colour.blurple())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
            else:
                embed = discord.Embed(description=f'Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
                embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'<:JC_xmark:826282095566913537> Diese Rolle "**{role}**" wurde nicht gefunden.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=embed)


@client.command()
async def massrole(ctx, aor, role1: discord.Role, role2: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        if aor.lower() == 'add':
            count = 0
            for members in role1.members:
                count += 1
            embed = discord.Embed(title='Massrole', description=f'Dadurch wird die Rolle {role2.mention} **{count} Mitgliedern** hinzugefügt.\r\n'
                                                                f'Der vorgang dauert etwa **{round(count * 1.1)} Sekunden**\r\n'
                                                                f'Möchtest du fortfahren? (ja/nein)', color=0xE31316)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and not m.author.bot

            try:
                confirmation = await client.wait_for('message', timeout=30.0, check=check)
                if confirmation.content.lower() == 'ja':
                    embed = discord.Embed(title='Massrole', description=f'Füge die Rolle {role2.mention} zu **{count} Mitgliedern** mit der Rolle {role1.mention} hinzu.\r\n'
                                                                        f'Dies dauert ungefähr **{round(count * 1.1)} Sekunden**', color=0xE31316)
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    success = 0
                    failed = 0
                    done = 0
                    for members in role1.members:
                        await members.add_roles(role2)
                        done += 1
                        success += 1
                        if done == 5:
                            await asyncio.sleep(5)
                            done = 0
                    embed = discord.Embed(title='Massrole abgeschlossen', color=discord.Colour.green())
                    embed.add_field(name="Erfolgreich", value=success)
                    embed.add_field(name="Fehlgeschlagen:", value=failed)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('<:JC_xmark:826282095566913537> **Vorgang abgebrochen**')
            except asyncio.TimeoutError:
                await ctx.send('<:JC_xmark:826282095566913537> **Vorgang abgebrochen**')
                return
        elif aor.lower() == 'remove':
            count = 0
            for members in role1.members:
                count += 1
            embed = discord.Embed(title='Massrole', description=f'Dadurch wird die Rolle von {role2.mention} **{count} Mitgliedern** entfernt.\r\n'
                                                                f'Der vorgang dauert etwa **{round(count * 1.1)} Sekunden**\r\n'
                                                                f'Möchtest du fortfahren? (ja/nein)', color=0xE31316)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and not m.author.bot

            try:
                confirmation = await client.wait_for('message', timeout=30.0, check=check)
                if confirmation.content.lower() == 'ja':
                    embed = discord.Embed(title='Massrole', description=f'Enferne die Rolle {role2.mention} von **{count} Mitgliedern** mit der Rolle {role1.mention}.\r\n'
                                                                        f'Dies dauert ungefähr **{round(count * 1.1)} Sekunden**', color=0xE31316)
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    success = 0
                    failed = 0
                    done = 0
                    for members in role1.members:
                        await members.add_roles(role2)
                        done += 1
                        success += 1
                        if done == 5:
                            await asyncio.sleep(5)
                            done = 0
                    embed = discord.Embed(title='Massrole abgeschlossen', color=discord.Colour.green())
                    embed.add_field(name="Erfolgreich", value=success)
                    embed.add_field(name="Fehlgeschlagen:", value=failed)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('<:JC_xmark:826282095566913537> **Vorgang abgebrochen**')
            except asyncio.TimeoutError:
                await ctx.send('<:JC_xmark:826282095566913537> **Vorgang abgebrochen**')
                return
        else:
            ... #error message

@massrole.error
async def massrole_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title='ERROR', description=f'<:JC_xmark:826282095566913537> Die angegebene Rolle wurde nicht gefunden.', color=0xff0000)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='ERROR', description=f'<:JC_xmark:826282095566913537> Es fählt ein wichtiges Argument.', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(aliases=['addrole', 'createrole'])
async def rolecreate(ctx, *, name):
    if ctx.author.guild_permissions.manage_roles:
        role = await ctx.guild.create_role(name=name)
        embed = discord.Embed(description=f'<:JC_check:826282165423046666> Die Rolle {role.mention} mit dem Namen `{role.name}` und der ID `{role.id}` wurde erstellt.', color=0xE31316)
        await ctx.send(embed=embed)
        logchannel = client.get_channel(884507838645428224)
        logembed = discord.Embed(description=f'Die Rolle {role.mention} mit dem Namen `{role.name}` und der ID `{role.id}` wurde erstellt.', color=discord.Colour.blurple())
        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
        await logchannel.send(embed=logembed)


@slash.slash(name="rolename",
             description="Ändere den Namen einer Rolle.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="role",
                    description="Erwähne eine Rolle.",
                    option_type=8,
                    required=True
                ),
                create_option(
                    name="name",
                    description="Der neue Name der Rolle.",
                    option_type=3,
                    required=True
                )
             ])
async def _rolename(ctx: SlashContext, role: discord.Role, name: str=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if ctx.author.guild_permissions.manage_roles:
        oldname = role.name
        await role.edit(name=name)
        embed = discord.Embed(description=f'<:JC_check:826282165423046666> Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=0xE31316)
        await ctx.send(embed=embed)
        logchannel = client.get_channel(884507838645428224)
        logembed = discord.Embed(description=f'Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=discord.Colour.blurple())
        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
        await logchannel.send(embed=logembed)
    elif teamrole in ctx.author.roles:
        if role.position <= ctx.author.top_role.position:
            oldname = role.name
            await role.edit(name=name)
            embed = discord.Embed(description=f'<:JC_check:826282165423046666> Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=0xE31316)
            await ctx.send(embed=embed)
            logchannel = client.get_channel(884507838645428224)
            logembed = discord.Embed(description=f'Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=discord.Colour.blurple())
            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)
        else:
            embed = discord.Embed(description=f'Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(hidden=True, embed=embed)
            return


@client.command()
async def rolename(ctx, role: discord.Role, *, name):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if ctx.author.guild_permissions.manage_roles:
        oldname = role.name
        await role.edit(name=name)
        embed = discord.Embed(description=f'<:JC_check:826282165423046666> Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=0xE31316)
        await ctx.send(embed=embed)
        logchannel = client.get_channel(884507838645428224)
        logembed = discord.Embed(description=f'Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=discord.Colour.blurple())
        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
        await logchannel.send(embed=logembed)
    elif teamrole in ctx.author.roles:
        if role.position <= ctx.author.top_role.position:
            oldname = role.name
            await role.edit(name=name)
            embed = discord.Embed(description=f'<:JC_check:826282165423046666> Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=0xE31316)
            await ctx.send(embed=embed)
            logchannel = client.get_channel(884507838645428224)
            logembed = discord.Embed(description=f'Der Name der Rolle {role.mention} wurde von `{oldname}` zu `{name}` geändert.', color=discord.Colour.blurple())
            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)
        else:
            embed = discord.Embed(description=f'Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=embed)
            return


@slash.slash(name="rolecolor",
             description="Ändere die Farbe einer Rolle.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="role",
                    description="Erwähne eine Rolle.",
                    option_type=8,
                    required=True
                ),
                create_option(
                    name="hex",
                    description="Die neue Farbe der Rolle als HEX-Code.",
                    option_type=3,
                    required=True
                )
             ])
async def _rolecolor(ctx: SlashContext, role: discord.Role, hex: str=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if ctx.author.guild_permissions.manage_messages:
        if not '#' in str(hex):
            beforecolor = role.color
            await role.edit(color=discord.Colour(int(f"0x{hex}", 16)))
            embed = discord.Embed(description=f'<:JC_check:826282165423046666> Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=0xE31316)
            await ctx.send(embed=embed)
            logchannel = client.get_channel(884507838645428224)
            logembed = discord.Embed(description=f'Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=discord.Colour.blurple())
            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)
        else:
            await ctx.send('<:JC_xmark:826282095566913537> Bitte verwende beim HEX code kein `#`.', hidden=True)
    elif teamrole in ctx.author.roles:
        if role.position <= ctx.author.top_role.position:
            if not '#' in str(hex):
                beforecolor = role.color
                await role.edit(color=discord.Colour(int(f"0x{hex}", 16)))
                embed = discord.Embed(description=f'<:JC_check:826282165423046666> Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=0xE31316)
                await ctx.send(embed=embed)
                logchannel = client.get_channel(884507838645428224)
                logembed = discord.Embed(description=f'Farbe der Rolle {role.mention} wurde zu **#{hex}** geändert.', color=discord.Colour.blurple())
                logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                await logchannel.send(embed=logembed)
            else:
                await ctx.send('<:JC_xmark:826282095566913537> Bitte verwende beim HEX code kein `#`.', hidden=True)
        else:
            embed = discord.Embed(description=f'Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(hidden=True, embed=embed)
            return

@client.command()
async def rolecolor(ctx, role: discord.Role, hex):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if ctx.author.guild_permissions.manage_messages:
        if not '#' in str(hex):
            beforecolor = role.color
            await role.edit(color=discord.Colour(int(f"0x{hex}", 16)))
            embed = discord.Embed(description=f'<:JC_check:826282165423046666> Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=0xE31316)
            await ctx.send(embed=embed)
            logchannel = client.get_channel(884507838645428224)
            logembed = discord.Embed(description=f'Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=discord.Colour.blurple())
            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)
        else:
            await ctx.reply('<:JC_xmark:826282095566913537> Bitte verwende beim HEX code kein `#`.')
    elif teamrole in ctx.author.roles:
        if role.position <= ctx.author.top_role.position:
            if not '#' in str(hex):
                beforecolor = role.color
                await role.edit(color=discord.Colour(int(f"0x{hex}", 16)))
                embed = discord.Embed(description=f'<:JC_check:826282165423046666> Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=0xE31316)
                await ctx.send(embed=embed)
                logchannel = client.get_channel(884507838645428224)
                logembed = discord.Embed(description=f'Farbe der Rolle {role.mention} wurde von **#{beforecolor}** zu **#{hex}** geändert.', color=discord.Colour.blurple())
                logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                await logchannel.send(embed=logembed)
            else:
                await ctx.reply('<:JC_xmark:826282095566913537> Bitte verwende beim HEX code kein `#`.')
        else:
            embed = discord.Embed(description=f'Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=embed)
            return


@client.command()
async def approve(ctx, user: discord.User, *, reason=None):
    if ctx.author.guild_permissions.manage_guild:
        if reason == None:
            reason = 'Kein Grund angegeben.'
        embed = discord.Embed(title='Bewerbung akzeptiert', description='Wir freuen uns dir mitteilen zu dürfen, dass deine schriftliche Bewerbung akzeptiert wurde. Wir laden dich hiermit zu einem mündlichen Bewerbungsgespräch ein.', timestamp=ctx.message.created_at, color=discord.Colour.green())
        embed.set_author(name='Jobcenter', icon_url=client.user.avatar_url)
        embed.set_footer(icon_url=ctx.guild.icon_url)
        embed.add_field(name='Anmerkung:', value=str(reason))
        await user.send(embed=embed)
        await ctx.message.add_reaction(':JC_check:826282165423046666')


@client.command()
async def accept(ctx, user: discord.User, *, reason=None):
    if ctx.author.guild_permissions.manage_guild:
        if reason == None:
            reason = 'Kein Grund angegeben.'
        embed = discord.Embed(title='Bewerbung akzeptiert', description='**Wir freuen uns dich bei uns im Team begrüßen zu dürfen.**', timestamp=ctx.message.created_at, color=discord.Colour.green())
        embed.set_author(name='Jobcenter', icon_url=client.user.avatar_url)
        embed.set_footer(icon_url=ctx.guild.icon_url)
        embed.add_field(name='Anmerkung:', value=str(reason))
        await user.send(embed=embed)
        await ctx.message.add_reaction(':JC_check:826282165423046666')


@client.command()
async def deny(ctx, user: discord.User, *, reason=None):
    if ctx.author.guild_permissions.manage_guild:
        if reason == None:
            reason = 'Kein Grund angegeben.'
        embed = discord.Embed(title='Bewerbung abgelehnt', description='Es tut uns wirklich leid dir mitteilen zu müssen, dass deine Bewerbung abgelehnt wurde.', timestamp=ctx.message.created_at, color=discord.Colour.red())
        embed.set_author(name='Jobcenter', icon_url=client.user.avatar_url)
        embed.set_footer(icon_url=ctx.guild.icon_url)
        embed.add_field(name='Grund:', value=str(reason))
        await user.send(embed=embed)
        await ctx.message.add_reaction(':JC_check:826282165423046666')
  

def paginate(lines, chars=2000):
    size = 0
    message = []
    for line in lines:
        if len(line) + size > chars:
            yield message
            message = []
            size = 0
        message.append(line)
        size += len(line)
    yield message
      

@client.command()
async def apply(ctx):
    if bw_offen == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Bewerbung ist derzeit Geschlossen!**\r\nBei Fragen wende dich bitte per Ticket an uns.')
        return

    role = client.get_guild(776912251944435723).get_role(868012378955075614) #BW verbot

    def check(m):
        return m.author == ctx.author and not m.guild
    
    if role not in ctx.author.roles:
        try:
            await ctx.message.add_reaction('<:JC_check:826282165423046666>')
            await ctx.send('<:JC_check:826282165423046666> **Bitte sieh in deine DMs.**')
            try:
                await ctx.author.send('Willkommen bei der Bewerbung für **JOBCENTER**.\r\n'
                                      'Bitte beantworte jewails eine frage in unter 5 Minuten sowie der Wahrheit entsprechend und ausführlich.')
            except:
                await ctx.message.add_reaction('<:JC_xmark:826282095566913537>')
                await ctx.reply('<:JC_xmark:826282095566913537> **Ich konnte dir keine DM senden.**')
            await ctx.author.send('Wie lautet dein Name?')
            name = await client.wait_for('message', timeout=60, check=check)
            await ctx.author.send('Wie alt bist du?')
            alter = await client.wait_for('message', timeout=300, check=check)
            await ctx.author.send('Erzähl uns etwas über dich')
            story = await client.wait_for('message', timeout=300, check=check)
            await ctx.author.send('Welche Erfahrungen hast du bereits als Supporter gesammelt?')
            erfahrung = await client.wait_for('message', timeout=300, check=check)
            await ctx.author.send('Welche Eigenschaft bringst du als Supporter mit?\r\n'
                                  'Und warum sollten wir genau dich nehmen?')
            mitbringen = await client.wait_for('message', timeout=300, check=check)
            await ctx.author.send('Wie sehen deine Online-Zeiten aus?')
            zeiten = await client.wait_for('message', timeout=300, check=check)
            await ctx.author.send('Was erwartest du von unserem Serverteam?')
            erwartungen = await client.wait_for('message', timeout=300, check=check)
            await ctx.author.send('**Bist du sicher dass du die Bewerbung abesnden möchtest?** (`Ja`/`Nein`)')
            bestätigung = await client.wait_for('message', timeout=300, check=check)
            if bestätigung.content == 'Ja':
                bwchannel = client.get_channel(869623266254409788)
                embed = discord.Embed(title='Neue Bewerbung', description=f'{ctx.author.mention} : {ctx.author.id}\r\n\r\n'
                f'**Name:**\r\n{name.content}\r\n\r\n'
                f'**Alter:**\r\n{alter.content}', timestamp=datetime.now(), color=0xE31316)
                embed2 = discord.Embed(title='Neue Bewerbung', description=f'**About:**\r\n{story.content}\r\n\r\n'
                f'**Erfahrungen:**\r\n{erfahrung.content}\r\n\r\n', color=0xE31316)
                embed3 = discord.Embed(title='Neue Bewerbung', description=f'**Eigenschaften:**\r\n{mitbringen.content}\r\n\r\n'
                f'**Online-Zeiten:**\r\n{zeiten.content}\r\n\r\n', color=0xE31316)
                embed4 = discord.Embed(title='Neue Bewerbung', description=f'**Erwartungen:**\r\n{erwartungen.content}', color=0xE31316)
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text='Sendung bestätigt')
                embed2.set_footer(text=f'Bewerber: {ctx.author}')
                embed3.set_footer(text=f'Bewerber: {ctx.author}')
                embed4.set_footer(text=f'Bewerber: {ctx.author}')
                await bwchannel.send(embed=embed)
                await bwchannel.send(embed=embed2)
                await bwchannel.send(embed=embed3)
                await bwchannel.send(embed=embed4)
                await bestätigung.add_reaction(':JC_check:826282165423046666')
            else:
                await ctx.author.send('<:JC_xmark:826282095566913537> **Vorgang abgebrochen!**')
        except asyncio.TimeoutError:
            await ctx.author.send('<:JC_xmark:826282095566913537> **Timout Error.**\r\nDu hast zu lange gebraucht!\r\n`,apply` um erneut zu beginnen.')


with open('./JOBCENTER/jc_reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []


@client.command(pass_context = True)
async def warn(ctx, user: discord.Member, *, reason: str):
    if ctx.author.guild_permissions.manage_messages:
        if not reason:
            await ctx.send("Bitte gebe einen Grund an.")
            return
        #reason = ' '.join(reason)
        for current_user in report['users']:
            if current_user['userid'] == user.id:
                current_user['reasons'].append(reason)
                await ctx.send(f'<:JC_check:826282165423046666> **{user.name}** wurde verwarnt: {reason}')
                break
        else:
            report['users'].append({
                'userid': user.id,
                'reasons': [reason,]
            })
            await ctx.send(f'<:JC_check:826282165423046666> **{user.name}** wurde verwarnt: {reason}')
        with open('./JOBCENTER/jc_reports.json','w+') as f:
            json.dump(report,f)

@client.command(pass_context = True, aliases=['warns'])
async def warnings(ctx,user:discord.User):
    for current_user in report['users']:
        if user.id == current_user['userid']:
            await ctx.send(f"**{user.name}** wurde `{len(current_user['reasons'])}` mal verwarnt : {', '.join(current_user['reasons'])}")
            break
    else:
        await ctx.send(f"**{user.name}** wurde noch nie verwarnt.")  

@client.command(pass_context = True, aliases=['resetwarn', 'removewarn'])
async def delwarn(ctx, user:discord.User, *, reason):
    for current_user in report['users']:
        if user.id == current_user['userid']:
            report['users'][user.id].remove(str(reason))
            await ctx.send(f'<:JC_check:826282165423046666> Die Verwarnung von **{user.name}** wurde entfernt.')
    else:
        await ctx.send(f"**{user.name}** wurde noch nie verwarnt.")  


@client.command(aliases=['massban'])
async def banall(ctx, *, content):
    if ctx.author.guild_permissions.administrator:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return

        def check(m):
            return m.author == ctx.author

        membercount = 0
        await ctx.message.add_reaction('a:JC_Timer:830745906327453696')
        for allmembers in ctx.guild.members:
            if content == '*':
                membercount += 1
            else:
                if str(content) in allmembers.name.lower() or str(content) in allmembers.display_name.lower():
                    membercount += 1
        await ctx.message.clear_reactions()
        if content == '*':
            confirmmsg = await ctx.send(f'Bist du dir sicher dass du einen Massban der leute starten willst? Dies würde **{membercount} Mitglieder** betreffen.')
        else:
            confirmmsg = await ctx.send(f'Bist du dir sicher dass du einen Massban der leute starten willst, dessen Name `{str(content)}` beinhaltet? Dies würde **{membercount} Mitglieder** betreffen.')
        try:
            bestätigung = await client.wait_for('message', timeout=10, check=check)
            if bestätigung.content == 'Ja' or bestätigung.content == 'ja':
                await ctx.send('<a:JC_Timer:830745906327453696> **Massban gestartet!**')
                if content == '*':
                    await ctx.reply('<:JC_xmark:826282095566913537> **Vorgang abgebrochen** (Error 403: Missing Permissions.)', delete_after=10)
                else:
                    success = 0
                    failed = 0
                    for allmembers in ctx.guild.members:
                        if str(content) == allmembers.name:
                            try:
                                #await allmembers.ban()
                                #await ctx.send(f'Banned {allmembers.name}#{allmembers.discriminator}')
                                #success += 1
                                failed += 1 # solange deaktiviert...
                            except:
                                failed += 1
                    await ctx.send(f'<:JC_check:826282165423046666> **Massban abgeschlossen!**\r\nErfolgreich: `{str(success)}`\r\nFehlgeschlagen: `{str(failed)}`')
        except asyncio.TimeoutError:
            await confirmmsg.delete()
            await ctx.message.delete()
            await ctx.reply('<:JC_xmark:826282095566913537> **Vorgang abgebrochen** (Error 5: Request timed out.)', delete_after=10)

@client.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if member == ctx.message.author:
            await ctx.send("Du kannst dich nicht selber kicken!")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("Diese Person ist zu mächtig um sie zu kicken.")
            return
        if reason == None:
            reason = "Kein Grund angegeben."
        await ctx.guild.kick(member, reason=reason)
        message = f"Du wurdest vom Server **{ctx.guild.name}** für **{reason}** gekickt."
        embed = discord.Embed(description=f"<:JC_check:826282165423046666> **{member}** wurde erfolgreich vom Server gekickt.\r\n**Grund:** {reason}", colour=0xE31316)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='<:JC_xmark:826282095566913537> Tut mir Leid, aber du bist nicht berechtigt diesen Befehl auszuführen!\r\n'
                                          '\r\n'
                                          '__Fehlende Berechtigung:__ **Mitglieder kicken**', color=0xff0000)
        await ctx.send(embed=embed)
        
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='<:JC_xmark:826282095566913537> **Bitte erwähne einen Nutzer.**', color=0xff0000)
        embed.add_field(name='Usage', value=f'`,kick <user> <reason>`')
        await ctx.send(embed=embed)


@client.command(aliases=['r21'])
async def ban(ctx, member: discord.User, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        if member == ctx.message.author:
            await ctx.send("Du kannst dich nicht selber bannen!")
            return
        if member in ctx.guild.members:
            user = ctx.guild.get_member(member.id)
            if user.top_role >= ctx.author.top_role:
                await ctx.send("Diese Person ist zu mächtig um sie zu bannen.")
                return
        if reason == None:
            reason = "Kein Grund angegeben."
        message = f"Du wurdest vom Server **{ctx.guild.name}** von **{ctx.author}** gebannt.\r\n**Grund:** {reason}"
        try:
            await member.send(message)
        except:
            pass
        embed = discord.Embed(description=f"**{member}** wurde vom Server gebannt.\r\n**Grund:** {reason}", colour=0xE31316)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
        await ctx.guild.ban(member, reason=reason)
        logchannel = client.get_channel(884507838645428224)
        logembed = discord.Embed(description=f'**{member.name}#{member.discriminator}** wurde von {ctx.author.mention} gebannt.', color=discord.Colour.red())
        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
        logembed.add_field(name='Grund:', value=reason)
        await logchannel.send(embed=logembed)
        await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command()
async def unban(ctx, id: int, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(description=f"**{user}** wurde entbannt.", colour=0xE31316)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
        if reason == None:
            reason = 'Kein Grund angegeben.'
        logchannel = client.get_channel(884507838645428224)
        embed = discord.Embed(description=f'**{user.name}#{user.discriminator}** wurde von {ctx.author.mention} entbannt.', color=discord.Colour.green())
        embed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
        await logchannel.send(embed=embed)

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='nuke')
@commands.cooldown(1, 60, type=BucketType.guild)
async def nuke(ctx, channel: discord.TextChannel=None):
    await ctx.send('**Dieser Channel wird in `10 Sekunden` genuked**')#\r\nZum abbrechen sende eine beliebige Nachricht.')
    await asyncio.sleep(5)
    await ctx.send('`5`')
    await asyncio.sleep(2)
    await ctx.send('`3`')
    await asyncio.sleep(1)
    await ctx.send('`2`')
    await asyncio.sleep(1)
    await ctx.send('`1`')
    await asyncio.sleep(1)
    if ctx.author == ctx.guild.owner:
        newc = await ctx.channel.clone()
        await ctx.channel.delete()
        await newc.send('**Channel wurde genuked**\r\nhttps://tenor.com/view/explosion-boom-explode-gif-17383346')
    elif ctx.author.guild_permissions.administrator:
        await ctx.reply('<:JC_xmark:826282095566913537> **Vorgang abgebrochen**\r\nFehlercode: `5`\r\nSonderberechtigung aufgrund von geschütztem Channel erforderlich')
    else:
        await ctx.reply('<:JC_xmark:826282095566913537> **Vorgang abgebrochen**\r\nFehlercode: `3`\r\nUnzureichende Berechtigungen')


@client.command(name='lock')
async def lock(ctx, channel: discord.TextChannel=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if mod_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if teamrole in ctx.author.roles:
        if channel == None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> **{ctx.channel.name}** unter lockdown versetzt.', color=0xE31316)
            await ctx.send(embed=embed)
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> **{channel.name}** unter lockdown versetzt.', color=0xE31316)
            await channel.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ <@&868012376946004059>", color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='unlock')
async def unlock(ctx, channel: discord.TextChannel=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if mod_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if teamrole in ctx.author.roles:
        if channel == None:
            await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=None)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> **{ctx.channel.name}** aus lockdown befreit.', color=0xE31316)
            await ctx.send(embed=embed)
        else:
            await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=None)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> **{channel.name}** aus lockdown befreit.', color=0xE31316)
            await channel.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ <@&868012376946004059>", color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='roleinfo')
async def roleinfo(ctx, role: discord.Role):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    embed = discord.Embed(description='**Information über** ' + role.mention, color=role.color)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name='Role-Name', value=role.name)
    embed.add_field(name='Role-ID', value=role.id)
    embed.add_field(name='Role-Mention', value=f"`{role.mention}`")
    embed.add_field(name='Role-Color', value=role.color)
    embed.add_field(name='Nutzer-Count', value=str(len(role.members)))
    embed.add_field(name='Erstellt', value=role.created_at.strftime(r"Am `%d.%m.%Y` um `%H:%M`"))
    embed.add_field(name='Position', value=f"{role.position}/{len(ctx.guild.roles)}")
    embed.add_field(name='Gruppiert', value=role.hoist)
    embed.add_field(name='Mentionable', value=role.mentionable)
    #embed.add_field(name='Key Permissions', value=", ".join([perm[0] for perm in role.permissions if perm[1]]))
    await ctx.send(embed=embed)


@slash.slash(name="inrole",
             description="Sehe wer eine bestimme Rolle besitzt.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="role",
                    description="Gib eine Rolle an.",
                    option_type=8,
                    required=True
                ),
                create_option(
                     name="verstecken",
                     description="Gib an ob die Nachricht versteckt werden soll. Standart: Ja",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="Verstecken",
                             value="yes"
                         ),
                         create_choice(
                             name="Anzeigen",
                             value="no"
                         )
                     ])
             ])
async def _inrole(ctx: SlashContext, role: discord.Role, verstecken="yes"):
    if ctx.author.guild_permissions.administrator:
        teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
        if fun_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
            return
        if teamrole in ctx.author.roles:
            embed = discord.Embed(description='**Information über** ' + role.mention, color=role.color)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Role-Name', value=role.name)
            embed.add_field(name='Role-ID', value=role.id)
            embed.add_field(name='Nutzer-Count', value=str(len(role.members)))
            usernames = [m.mention for m in role.members]
            if len(usernames) == 0:
                embed.add_field(name='Mitglieder der Rolle', value='Diese Rolle hat aktuell **keine** Mitglieder!', inline=False)
            elif len(usernames) <= 50:
                embed.add_field(name='Mitglieder der Rolle', value="- " + "\r\n- ".join(usernames), inline=False)
            else:
                embed.add_field(name='Mitglieder der Rolle', value='Die Liste ist zu lang da die Anzahl der Mitglieder der Rolle `50` überschreitet.', inline=False)
            if verstecken == "yes":
                await ctx.send(embed=embed, hidden=True)
            else:
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                              "\r\n"
                                              "__Fehlende Rolle:__ <@&868012376946004059>", color=0xff0000)
            await ctx.send(embed=embed, hidden=True)

@client.command(name='inrole')
async def inrole(ctx, role: discord.Role):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if teamrole in ctx.author.roles:
        embed = discord.Embed(description='**Information über** ' + role.mention, color=role.color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name='Role-Name', value=role.name)
        embed.add_field(name='Role-ID', value=role.id)
        embed.add_field(name='Nutzer-Count', value=str(len(role.members)))
        usernames = [m.mention for m in role.members]
        if len(usernames) == 0:
            embed.add_field(name='Mitglieder der Rolle', value='Diese Rolle hat aktuell **keine** Mitglieder!', inline=False)
        elif len(usernames) <= 50:
            embed.add_field(name='Mitglieder der Rolle', value="- " + "\r\n- ".join(usernames), inline=False)
        else:
            embed.add_field(name='Mitglieder der Rolle', value='Die Liste ist zu lang da die Anzahl der Mitglieder der Rolle `50` überschreitet.', inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ <@&868012376946004059>", color=0xff0000)
        await ctx.send(embed=embed)



@client.command(name='blockav', aliases=['avblock'])
async def blockav(ctx):
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if ctx.author.id in blockedav["ids"]:
        blockedav["ids"].remove(ctx.author.id)
        with open('./JOBCENTER/jc_avblock.json', 'w') as f:
            json.dump(blockedav, f, indent=4)
        await ctx.send('<:JC_check:826282165423046666> **Das einsehen deines Avatars wurde __freigegeben__!**')
    else:
        blockedav["ids"].append(ctx.author.id)
        with open('./JOBCENTER/jc_avblock.json', 'w') as f:
            json.dump(blockedav, f, indent=4)
        await ctx.send('<:JC_check:826282165423046666> **Das einsehen deines Avatars wurde __blockiert__!**')

@slash.slash(name="avatar",
             description="Sehe den Avatar eines Nutzers ein.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="user",
                    description="Erwähne ein Mitglied.",
                    option_type=6,
                    required=False
                )
             ])
async def _avatar(ctx: SlashContext, user: discord.User=None):
    context = client.get_context
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if fun_enabled == False:
        await ctx.send('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**', hidden=True)
        return
    if user != None:
        if not user.id in blockedav["ids"] or ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title='Avatar', color=0xE31316)
            embed.set_image(url=user.avatar_url)
            embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'<:JC_xmark:826282095566913537> **{user}** hat das einsehen des Avatars blockiert.', hidden=True)
    else:
        embed = discord.Embed(title='Avatar', color=0xE31316)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@client.command(aliases=['mostwanted', 'most-wanted'])
@commands.cooldown(1, 15, type=BucketType.channel)
async def wanted(ctx, user: discord.User=None):
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if user != None:
        if not user.id in blockedav["ids"] or ctx.author.guild_permissions.administrator:    
            background = Image.open("./JOBCENTER/wanted-template1.png")
            font = ImageFont.truetype("./JOBCENTER/wanted-font.ttf", 26)
            W, H = (400, 545)

            asset = user.avatar_url_as(size = 128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            pfp = pfp.resize((265,265))
            #sepia = Image.new('RGB', (65, 185), (56, 44, 30))
            #sepia = sepia.resize((265,265))
            #sepia = ImageColor.getrgb((56, 44, 30))
            #sepia.putalpha(127)
            
            draw = ImageDraw.Draw(background)
            ammount1 = randrange(1,10)
            ammount2 = randrange(100,999)
            text = str(ammount1) + "." + str(ammount2) + ".000 $"
            if ammount1 >= 10:
                text = "10.000.000 $"

            background.paste(pfp, (65,185))
            w, h = draw.textsize(text)
            draw.text(((W-w)/2 + 160,(H-h)/2 + 235), text, (0, 0, 0), anchor="rb", font=font)
        
            background.save("./JOBCENTER/wanted.png")

            await ctx.reply(file=discord.File("./JOBCENTER/wanted.png"))
        else:
            await ctx.reply(f'<:JC_xmark:826282095566913537> **{user}** hat das einsehen des Avatars blockiert.')
    else:
        background = Image.open("./JOBCENTER/wanted-template1.png")
        font = ImageFont.truetype("./JOBCENTER/wanted-font.ttf", 26)
        W, H = (400, 545)

        asset = ctx.author.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((265,265))

        draw = ImageDraw.Draw(background)
        ammount1 = randrange(1,10)
        ammount2 = randrange(100,999)
        text = str(ammount1) + "." + str(ammount2) + ".000 $"
        if ammount1 >= 10:
            text = "10.000.000 $"

        background.paste(pfp, (65,185))
        w, h = draw.textsize(text)
        draw.text(((W-w)/2 + 160,(H-h)/2 + 235), text, (0, 0, 0), anchor="rb", font=font)
        
        background.save("./JOBCENTER/wanted.png")

        await ctx.reply(file=discord.File("./JOBCENTER/wanted.png"))
    


@client.command(name='serveravatar', aliases=['avs', 'sav'])
@commands.cooldown(1, 15, type=BucketType.user)
async def serveravatar(ctx, user: discord.Member=None):
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    
    url = f"https://discord.com/api/v8/guilds/{ctx.guild.id}"
    headers = {"Authorization": f"Bot {TOKEN}"}
    r = requests.get(url, headers=headers)
    response = r.json()
    print(response)

    if user != None:
        if not user.id in blockedav["ids"] or ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title='Server Avatar', color=0xE31316)
            embed.set_image(url=avatar)
            embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f'<:JC_xmark:826282095566913537> **{user}** hat das einsehen des Avatars blockiert.')
    else:
        embed = discord.Embed(title='Avatar', color=0xE31316)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

     
        
@client.command(name='avatar', aliases=['av'])
@commands.cooldown(1, 15, type=BucketType.user)
async def avatar(ctx, user: discord.User=None):
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if user != None:
        if not user.id in blockedav["ids"] or ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title='Avatar', color=0xE31316)
            embed.set_image(url=user.avatar_url)
            embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f'<:JC_xmark:826282095566913537> **{user}** hat das einsehen des Avatars blockiert.')
    else:
        embed = discord.Embed(title='Avatar', color=0xE31316)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)


@slash.slash(name="banner",
             description="Sehe das Banner eines Nutzers ein.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="user",
                    description="Erwähne ein Mitglied.",
                    option_type=6,
                    required=False
                )
             ])
async def _banner(ctx: SlashContext, user: discord.User=None):
    context = client.get_context
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if fun_enabled == False:
        await ctx.send('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**', hidden=True)
        return
    if user == None:
        user = ctx.author
    url = f"https://discord.com/api/v8/users/{user.id}"
    headers = {"Authorization": f"Bot {TOKEN}"}
    r = requests.get(url, headers=headers)
    response = r.json()
    bannername = response['banner']
    bannerformat = 'png'
    if bannername[:2] == 'a_':
        bannerformat = 'gif'
    banner = f"https://cdn.discordapp.com/banners/{user.id}/{bannername}.{bannerformat}?size=4096"

    embed = discord.Embed(title='Banner', color=0xE31316)
    embed.set_image(url=banner)
    embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
    if user == ctx.author:
        await ctx.send(embed=embed)
    elif not user.id in blockedav["ids"] or ctx.author.guild_permissions.administrator:
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'<:JC_xmark:826282095566913537> **{user}** hat das einsehen des Avatars blockiert.', hidden=True)

@client.command(name='banner', aliases=['avb', 'avbanner'])
@commands.cooldown(1, 15, type=BucketType.user)
async def banner(ctx, user: discord.User=None):
    with open("./JOBCENTER/jc_avblock.json") as f:
        blockedav = json.load(f)
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if user == None:
        user = ctx.author
    url = f"https://discord.com/api/v8/users/{user.id}"
    headers = {"Authorization": f"Bot {TOKEN}"}
    r = requests.get(url, headers=headers)
    response = r.json()
    bannername = response['banner']
    bannerformat = 'png'
    if bannername[:2] == 'a_':
        bannerformat = 'gif'
    banner = f"https://cdn.discordapp.com/banners/{user.id}/{bannername}.{bannerformat}?size=4096"

    embed = discord.Embed(title='Banner', color=0xE31316)
    embed.set_image(url=banner)
    embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
    if user == ctx.author:
        await ctx.send(embed=embed)
    elif not user.id in blockedav["ids"] or ctx.author.guild_permissions.administrator:
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'<:JC_xmark:826282095566913537> **{user}** hat das einsehen des Avatars blockiert.', hidden=True)


@client.command(aliases=['randomav'])
async def randompfp(ctx):
    colors = [discord.Colour.dark_red(), discord.Colour.dark_orange(), discord.Colour.blue(), discord.Colour.dark_green(),
              discord.Colour.dark_blue(), discord.Colour.magenta(), discord.Colour.dark_magenta(), discord.Colour.purple(),
              discord.Colour.dark_purple()]
    randomuser = random.choice(ctx.guild.members)
    embed = discord.Embed(title='Ein zufälliges Profilbild', timestamp=datetime.now(), color=discord.Colour.random())
    embed.set_author(name=randomuser.name, icon_url=randomuser.avatar_url)
    embed.set_image(url=randomuser.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def spotify(ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            embed = discord.Embed(
                title = f"{user.name}'s Spotify",
                description = "Hört **{}**".format(activity.title),
                color = 0x1DB954)
            embed.set_thumbnail(url=activity.album_cover_url)
            embed.add_field(name="Artist", value=activity.artist)
            embed.add_field(name="Album", value=activity.album)
            embed.add_field(name="Duration", value=activity.duration)
            embed.set_footer(text="Song hat um {} begonnen.".format(activity.created_at.strftime("%H:%M")))
            await ctx.send(embed=embed)
        #else:
        #    await ctx.send(f'**{user}** hört derzeit kein Spotify.')


@slash.slash(name="userinfo",
             description="Erhalte Infos über einen Nutzer.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="user",
                    description="Erwähne einen Nutzer dessen Info du sehen willst.",
                    option_type=6,
                    required=False
                )
             ])
async def _userinfo(ctx: SlashContext, user: discord.User=None):
    if fun_enabled == False:
        await ctx.send('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**', hidden=True)
        return
    if user != None:
        highrole = user.top_role.mention
        highrolecolor = user.top_role.color
        if highrole == "@everyone":
            highrole = "None"
        em = discord.Embed(colour=highrolecolor)
        em.add_field(name='Nickname', value=user.nick, inline=True)
        em.add_field(name='Status', value=user.status, inline=True)
        em.add_field(name='Aktivität/Custom-Stauts', value=user.activity, inline=True)
        em.add_field(name='Höchste Rolle', value=highrole, inline=True)
        em.add_field(name='Account erstellt', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name='Server beigetreten', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=f'{user.avatar_url}')
        em.set_author(name=user, icon_url=f'{user.avatar_url}')
        em.set_footer(text=f'User ID: {user.id}')
        msg = await ctx.send(hidden=True, embed=em)
    else:
        highrole = ctx.author.top_role.mention
        highrolecolor = ctx.author.top_role.color
        if highrole == "@everyone":
            highrole = "None"
        em = discord.Embed(colour=highrolecolor)
        em.add_field(name='Nickname', value=ctx.author.nick, inline=True)
        em.add_field(name='Status', value=ctx.author.status, inline=True)
        em.add_field(name='Aktivität/Custom-Stauts', value=ctx.author.activity, inline=True)
        em.add_field(name='Höchste Rolle', value=highrole, inline=True)
        em.add_field(name='Account erstellt', value=ctx.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name='Server beigetreten', value=ctx.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=f'{ctx.author.avatar_url}')
        em.set_author(name=ctx.author, icon_url=f'{ctx.author.avatar_url}')
        em.set_footer(text=f'User ID: {ctx.author.id}')
        msg = await ctx.send(hidden=True, embed=em)

@client.command(name='userinfo', aliases=['whois'])
async def userinfo(ctx, user: discord.Member=None):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if user != None:
        highrole = user.top_role.mention
        highrolecolor = user.top_role.color
        if highrole == "@everyone":
            highrole = "None"
        em = discord.Embed(description='**Klicke auf "Löschen" um die Userinfo wieder zu löschen.**', colour=highrolecolor)
        em.add_field(name='Nickname', value=user.nick, inline=True)
        em.add_field(name='Status', value=user.status, inline=True)
        em.add_field(name='Aktivität/Custom-Stauts', value=user.activity, inline=True)
        em.add_field(name='Höchste Rolle', value=highrole, inline=True)
        em.add_field(name='Account erstellt', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name='Server beigetreten', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=f'{user.avatar_url}')
        em.set_author(name=user, icon_url=f'{user.avatar_url}')
        em.set_footer(text=f'User ID: {user.id}')
        msg = await ctx.send(embed=em,
        components=[Button(style=1, label="Löschen")])

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel
    
        try:
            res = await client.wait_for("button_click", check=check, timeout=60.0)
            await msg.delete()
            await ctx.message.delete()
        except asyncio.TimeoutError:
            await msg.edit(components=[Button(style=1, label="Löschen", disabled=True)])
    
    else:
        highrole = ctx.author.top_role.mention
        highrolecolor = ctx.author.top_role.color
        if highrole == "@everyone":
            highrole = "None"
        #em = discord.Embed(description='**Reagiere mit 🗑️ um die Userinfo wieder zu löschen.**', colour=highrolecolor)
        em = discord.Embed(description='**Klicke auf "Löschen" um die Userinfo wieder zu löschen.**', colour=highrolecolor)
        em.add_field(name='Nickname', value=ctx.author.nick, inline=True)
        em.add_field(name='Status', value=ctx.author.status, inline=True)
        em.add_field(name='Aktivität/Custom-Stauts', value=ctx.author.activity, inline=True)
        em.add_field(name='Höchste Rolle', value=highrole, inline=True)
        em.add_field(name='Account erstellt', value=ctx.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name='Server beigetreten', value=ctx.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=f'{ctx.author.avatar_url}')
        em.set_author(name=ctx.author, icon_url=f'{ctx.author.avatar_url}')
        em.set_footer(text=f'User ID: {ctx.author.id}')
        msg = await ctx.send(embed=em,
        components=[Button(style=1, label="Löschen")])

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel
    
        try:
            res = await client.wait_for("button_click", check=check, timeout=60.0)
            await msg.delete()
            await ctx.message.delete()
        except asyncio.TimeoutError:
            await msg.edit(components=[Button(style=1, label="Löschen", disabled=True)])
            
            
@client.command(name='nsfw')
async def nsfw(ctx):
    if ctx.author.guild_permissions.manage_messages:
        if ctx.channel.is_nsfw():
            await ctx.channel.edit(nsfw=False)
            embed = discord.Embed(description=f'Der Channel ist jetzt nicht mehr als `NSFW` markiert.', color=0xE31316)
            await ctx.send(embed=embed)
            await ctx.message.delete()
        else:
            await ctx.channel.edit(nsfw=True)
            embed = discord.Embed(description=f'Der Channel ist jetzt als `NSFW` markiert.', color=0xE31316)
            await ctx.send(embed=embed)
            await ctx.message.delete()
    else:
        embed = discord.Embed(description=':x: Tut mir Leid, aber du bist nicht berechtigt diesen Befehl auszuführen!\r\n'
                                          '\r\n'
                                          '__Fehlende Berechtigung:__ **Nachrichten verwalten**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='slowmode')
async def slowmode(ctx):
    if ctx.author.guild_permissions.manage_messages:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        args = ctx.message.content.split(' ')
        if len(args) == 2:
            if args[1].isdigit():
                zahl = int(args[1])
                await ctx.channel.edit(slowmode_delay=zahl)
                embed = discord.Embed(description=f':alarm_clock: Der Slowmode dieses Channels wurde auf **{args[1]} Sekunden** aktualisiert!', color=0xE31316)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
        else:
            embed = discord.Embed(description=':x: Bitte gebe eine Zeit an, auf die der Slowmode gesetzt werden soll!\r\n'
                                              '\r\n'
                                              '__Usage:__ `,slowmode <zahl>`', color=0xff0000)
            await ctx.send(embed=embed)
            await ctx.message.delete()
    else:
        embed = discord.Embed(description=':x: Tut mir Leid, aber du bist nicht berechtigt diesen Befehl auszuführen!\r\n'
                                          '\r\n'
                                          '__Fehlende Berechtigung:__ **Nachrichten verwalten**', color=0xff0000)
        await ctx.send(embed=embed)
        await ctx.message.delete()


@client.command(name='clear')
async def clear(ctx):
    if ctx.author.guild_permissions.manage_messages:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        args = ctx.message.content.split(' ')
        if len(args) == 2:
            if args[1].isdigit():
                count = int(args[1]) + 1
                deleted = await ctx.channel.purge(limit=count, check=is_not_pinned)
                embed = discord.Embed(description=':wastebasket: **{}** Nachricht/en gelöscht.'.format(len(deleted)-1), color=0xE31316)
                await ctx.send(embed=embed, delete_after=3)
        else:
            embed = discord.Embed(description=':x: Bitte gebe eine gültige Anzahl an Nachrichten an, die gelöscht werden sollen.\r\n'
                                              '\r\n'
                                              '__Usage:__ `,clear <Anzahl>`', color=0xff0000)
            await ctx.send(embed=embed, delete_after=10)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Command auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Berechtigung:__ **Nachrichten verwalten**", color=0xff0000)
        await ctx.send(embed=embed, delete_after=10)


@client.command(name='howgay')
@commands.cooldown(1, 10, type=BucketType.user)
async def howgay(ctx, user: discord.User=None):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    gayrange = randrange(100)
    gayflag = ""
    if int(gayrange) >= 50:
        gayflag = ":gay_pride_flag:"
    if user != None:
        embed = discord.Embed(title="Gaymeter", description=f"{user.name} ist {gayrange}% gay {gayflag}", color=0xE31316)
        await ctx.reply(embed=embed)
        return
    else:
        embed = discord.Embed(title="Gaymeter", description=f"Du bist {gayrange}% gay {gayflag}", color=0xE31316)
        await ctx.reply(embed=embed)


@client.command(name='f')
@commands.cooldown(1, 60, type=BucketType.guild)
async def f(ctx, *, message: str):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if not '@' in message:
        msg = await ctx.send(f"Press 🇫 to pay respect for **{message}**.")
        await msg.add_reaction("🇫")
        
        users = []

        try:
            def check(reaction, user):
                return str(reaction.emoji) == '🇫' and reaction.message.id == msg.id and user != client.user

            while True:
                reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                await msg.reply(f"🇫 {user.mention} is paying respect.")
                users.append(str(user.id))
        except asyncio.TimeoutError:
            await msg.reply(f"🇫 **{len(users)}** user(s) paid their respect to **{message}**.")
    else:
        await ctx.send('Bitte vermeide das erwähnen von Rollen oder Membern.')



@client.command(name='penis')
@commands.cooldown(1, 10, type=BucketType.user)
async def penis(ctx, user: discord.User=None):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    if user != None:
        embed = discord.Embed(title="Stop stop... Warte mal...", description=f"{user.mention} muss zulassen, dass du seine/ihre Penislänge einsehen darfst.", color=0xff0000)
        embed.set_footer(text='Mit "Zulassen" bestätigen.')
        msg = await ctx.send(f'{user.mention}', embed=embed,
        components=[Button(style=4, label="Zulassen")])

        def check(res):
            return res.user == user and res.channel == ctx.channel
    
        try:
            res = await client.wait_for("button_click", check=check, timeout=60.0)
            await res.respond(type=6)
            color = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
                      discord.Colour.blue(), discord.Colour.purple(), discord.Colour.magenta()]
            penis = ['', '=', '==', '===', '====', '=====', '======', '=======', '========', '=========', '==========', '===========', '============', '=============', '==============', '===============', '================']
            newembed = discord.Embed(title="Penislänge", description=f"{user.name}'s Penislänge\r\n"
                                                                      "8" + random.choice(penis) + "D", color=0xE31316)
            if user.id == 753009216767393842:
                newembed = discord.Embed(title="Penislänge", description=f"{user.name}'s Penislänge\r\n"
                                                                          "8=================D", color=0xE31316)
            if user.id == 490571058026512398:
                newembed = discord.Embed(title="Penislänge", description=f"{user.name}'s Penislänge\r\n"
                                                                          "8D", color=0xE31316)
            await msg.edit(embed=newembed, components=[Button(style=3, label="Zugelassen", disabled=True)])
        except asyncio.TimeoutError:
            await msg.edit(components=[Button(style=2, label="Timed out", disabled=True)])
    else:
        color = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
                  discord.Colour.blue(), discord.Colour.purple(), discord.Colour.magenta()]
        penis = ['', '=', '==', '===', '====', '=====', '======', '=======', '========', '=========', '==========', '===========', '============', '=============', '==============', '===============', '================']
        embed = discord.Embed(title="Penislänge", description=f"{ctx.author.name}'s Penislänge\r\n"
                                                               "8" + random.choice(penis) + "D", color=0xE31316)
        if ctx.author.id == 753009216767393842:
            embed = discord.Embed(title="Penislänge", description=f"{ctx.author.name}'s Penislänge\r\n"
                                                                   "8=================D", color=0xE31316)
        if ctx.author.id == 490571058026512398:
            embed = discord.Embed(title="Penislänge", description=f"{ctx.author.name}'s Penislänge\r\n"
                                                                   "8D", color=0xE31316)
        await ctx.send(embed=embed)

snipe_message_content = None
snipe_message_author = None
snipe_message_time = None
edit_snipe_message_content_before = None
edit_snipe_message_content_after = None
edit_snipe_message_author = None
edit_snipe_message_time = None

@client.event
async def on_message_edit(before, after):

    if before.author.bot:
        return
    
    if 'http' in after.content:
        return
    
    if '.gg/' in after.content:
        return

    global edit_snipe_message_content_before
    global edit_snipe_message_content_after
    global edit_snipe_message_author
    global edit_snipe_message_time

    edit_snipe_message_content_before = before.content
    edit_snipe_message_content_after = after.content
    edit_snipe_message_author = after.author
    edit_snipe_message_time = after.edited_at

@client.event
async def on_message_delete(message):

    if message.author.bot:
        return
    
    if 'http' in message.content:
        return
    
    if '.gg/' in message.content:
        return

    global snipe_message_content
    global snipe_message_author
    global snipe_message_time
    with open("./JOBCENTER/jc_blacklist.json") as f:
        blacklist = json.load(f)
    snipe_message_content = message.content
    snipe_message_author = message.author
    snipe_message_time = message.created_at
    for bad_word in blacklist["words"]:
        if bad_word in message.content.lower():
            snipe_message_content = None
            snipe_message_author = None
            snipe_message_time = None

    
@client.command(name='snipe')
@commands.cooldown(1, 30, type=BucketType.user)
async def snipe(ctx):
    if snipe_message_content != None:
        embed = discord.Embed(description=snipe_message_content, timestamp=snipe_message_time, color=0xE31316)
        embed.set_author(name=snipe_message_author, icon_url=snipe_message_author.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.reply('Es gibt nichts zu snipen.')

@client.command(name='editsnipe')
@commands.cooldown(1, 30, type=BucketType.user)
async def editsnipe(ctx):
    if edit_snipe_message_content_after != None:
        embed = discord.Embed(timestamp=edit_snipe_message_time, color=0xE31316)
        embed.add_field(name="Before:", value=edit_snipe_message_content_before, inline=False)
        embed.add_field(name="After", value=edit_snipe_message_content_after, inline=False)
        embed.set_author(name=edit_snipe_message_author, icon_url=edit_snipe_message_author.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Es gibt nichts zu snipen.')

#@client.command(name='pussy', aliases=['mumu', 'muschi'])
#async def pussy(ctx, user: discord.User=None):
#    if user != None:
#        embed = discord.Embed(title="Stop stop... Warte mal...", description="Du kannst nur deine eigene Pussytiefe einsehen. (Außer jemand erlaubt es dir in ihre Hose zu schauen :eyes:)", color=0xff0000)
#        await ctx.send(embed=embed)
#    else:
#        color = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
#                  discord.Colour.blue(), discord.Colour.purple(), discord.Colour.magenta()]
#        pussy = ['', '=', '==', '===', '====', '=====', '======', '=======', '========', '=========', '==========', '===========', '============', '=============', '==============', '===============', '================']
#        embed = discord.Embed(title="Pussytiefe", description=f"{ctx.author.name}'s Pussytiefe\r\n"
#                                                              "{(.)}" + random.choice(pussy) + "|", color=0xE31316)
#        await ctx.send(embed=embed)


@client.command(name='mute')
async def mute(ctx, user: discord.Member, time=None, *, reason=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if teamrole in ctx.author.roles:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        if not user == ctx.author:
            if time:
                if time == '0' or time == 'infinite':
                    role = discord.utils.get(ctx.guild.roles, id=868012378955075614)
                    await user.add_roles(role, reason=reason)
                    with open('./JOBCENTER/jc_data.json', 'r') as f:
                        data = json.load(f)
                    if not user.id in data["muted"]:
                        data["muted"].append(user.id)
                        with open('./JOBCENTER/jc_data.json', 'w') as f:
                            json.dump(data, f)
                    embed = discord.Embed(description=f'{user.mention}: {user.id} wurde gemuted!', color=0xE31316)
                    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    dmembed = discord.Embed(description=f'{user.mention} du wurdest auf dem {ctx.guild.name} Server gemuted!', color=0xE31316)
                    dmembed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    if reason == None:
   		                reason = "Kein Grund angegeben."
                    embed.add_field(name='Grund:', value=reason)
                    dmembed.add_field(name='Grund:', value=reason)
                    await ctx.send(embed=embed)
                else:
                    seconds = time[:-1]
                    duration = time[-1]
                    if duration == "s":
                        seconds = int(seconds) * 1
                    elif duration == "m":
                        seconds = int(seconds) * 60
                    elif duration == "h":
                        seconds = int(seconds) * 60 * 60
                    #elif duration == "d":
                    #    seconds = seconds * 86400
                    else:
                        await ctx.send(":x: Falsche Zeitangabe")
                        return
                    role = discord.utils.get(ctx.guild.roles, id=868012378955075614)
                    await user.add_roles(role, reason=reason)
                    with open('./JOBCENTER/jc_data.json', 'r') as f:
                        data = json.load(f)
                    if not user.id in data["muted"]:
                        data["muted"].append(user.id)
                        with open('./JOBCENTER/jc_data.json', 'w') as f:
                            json.dump(data, f)
                    embed = discord.Embed(description=f'{user.mention}: {user.id} wurde für **{time}** gemuted!', color=0xE31316)
                    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    dmembed = discord.Embed(description=f'Du wurdest auf dem **{ctx.guild.name}** Server von **{ctx.author}** gemuted!', color=0xE31316)
                    dmembed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    if reason == None:
   		                reason = "Kein Grund angegeben."
                    embed.add_field(name='Grund:', value=reason)
                    dmembed.add_field(name='Grund:', value=reason)
                    await ctx.send(embed=embed)
                    #message = f"Du wurdest vom Server **{ctx.guild.name}** für **{time}** gemutet.\r\nGrund: {reason}"
                    try:
                        await user.send(embed=dmembed)
                    except:
                        pass
                    logchannel = client.get_channel(884507838645428224)
                    logembed = discord.Embed(description=f'**{user.name}#{user.discriminator}** wurde von {ctx.author.mention} für **{time}** gemuted.', color=discord.Colour.red())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                    logembed.add_field(name='Grund:', value=reason)
                    await logchannel.send(embed=logembed)
                    await asyncio.sleep(int(seconds))
                    await user.remove_roles(role, reason=f'Automated unmute after {time}')
                    with open('./JOBCENTER/jc_data.json', 'r') as f:
                        data = json.load(f)
                    if user.id in data["muted"]:
                        data["muted"].remove(user.id)
                        with open('./JOBCENTER/jc_data.json', 'w') as f:
                            json.dump(data, f)
                    logchannel = client.get_channel(884507838645428224)
                    logembed = discord.Embed(description=f'**{user.name}#{user.discriminator}** wurde automatisch nach **{time}** entmuted.', color=discord.Colour.green())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)
            else:
                embed = discord.Embed(description=":x: Bitte nenne eine Dauer des Mutes.\r\n"
                                                  "_(Zeiten länger als 24h können zu fehlern führen.)_", color=0xff0000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=":x: Tut mir Leid, aber bist du grade dabei dich selber zu muten?\r\n"
                                              "Ist das dein Ernst? Das ist leider nicht möglich.", color=0xff0000)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ **<@&868012376946004059>**", color=0xff0000)
        await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='unmute')
async def unmute(ctx, user: discord.Member, *, reason=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if teamrole in ctx.author.roles:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        role = discord.utils.get(ctx.guild.roles, id=868012378955075614)
        await user.remove_roles(role, reason=reason)
        with open('./JOBCENTER/jc_data.json', 'r') as f:
            data = json.load(f)
        if user.id in data["muted"]:
            data["muted"].remove(user.id)
            with open('./JOBCENTER/jc_data.json', 'w') as f:
                json.dump(data, f)
        embed = discord.Embed(description=f'{user.mention}: {user.id} wurde entmuted!', color=0xE31316)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        dmembed = discord.Embed(description=f'Der Mute auf dem **{ctx.guild.name}** Server wurde von **{ctx.author}** aufgehoben!', color=0xE31316)
        dmembed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
        try:
            await user.send(embed=dmembed)
        except:
            pass
        if reason == None:
            reason = 'Kein Grund angegeben.'
        logchannel = client.get_channel(884507838645428224)
        logembed = discord.Embed(description=f'**{user.name}#{user.discriminator}** wurde von {ctx.author.mention} entmuted.', color=discord.Colour.green())
        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        logembed.set_footer(text=client.user.name + ' - Mod Logs', icon_url=client.user.avatar_url)
        logembed.add_field(name='Grund:', value=reason)
        await logchannel.send(embed=logembed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ **<@&868012376946004059>**", color=0xff0000)
        await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**ERROR.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='jail')
async def jail(ctx, user: discord.Member, *, reason=None):
    if client.get_guild(776912251944435723).get_role(868012376946004059) in ctx.author.roles:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        role = discord.utils.get(ctx.guild.roles, id=841759570703155240)
        #role2 = discord.utils.get(ctx.guild.roles, id=696537659438268468)
        await user.add_roles(role, reason=reason)
        #await user.remove_roles(role2, reason=reason)
        embed = discord.Embed(description=f':lock: {user.mention}: {user.id} wurde in den Knast gesteckt!', color=discord.Colour.orange())
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ **<@&868012376946004059>**", color=0xff0000)
        await ctx.send(embed=embed)

@jail.error
async def jail_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='unjail')
async def unjail(ctx, user: discord.Member, *, reason=None):
    if client.get_guild(776912251944435723).get_role(868012376946004059) in ctx.author.roles:
        if mod_enabled == False:
            await ctx.reply('<:JC_xmark:826282095566913537> **Die Moderationsbefehle wurden vom Team vorübergehend deaktiviert!**')
            return
        role = discord.utils.get(ctx.guild.roles, id=814635095485972500)
        #role2 = discord.utils.get(ctx.guild.roles, id=696537659438268468)
        await user.remove_roles(role, reason=reason)
        #await user.add_roles(role2, reason=reason)
        embed = discord.Embed(description=f':unlock: {user.mention}: {user.id} wurde aus dem Knast entlassen!', color=discord.Colour.green())
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ **<@&868012376946004059>**", color=0xff0000)
        await ctx.send(embed=embed)

@unjail.error
async def unjail_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)

### DIESES SYSTEM IST AUFGRUND FEHLERHAFTER NUTZUNG UND VERWECHSLUNG DEAKTIVIERT!!!
#       
#@client.command(name='lockdown')
#async def lockdown(ctx):
#        if ctx.author.guild_permissions.manage_guild:
#            memberrole = discord.utils.get(ctx.guild.roles, id=811744961204453377)
#            channel = client.get_channel(841759773519380500)
#            await memberrole.edit(permissions=discord.Permissions(send_messages=False, connect=False,
#                                                                  view_channel=True, read_messages=True, create_instant_invite=True,
#                                                                  change_nickname=True, add_reactions=True, speak=True, stream=True,
#                                                                  embed_links=True, external_emojis=True, use_voice_activation=True,
#                                                                  read_message_history=True, attach_files=True))
#            embed1 = discord.Embed(title=":lock: Lockdown", description="__Deutsch:__\r\n"
#                                                                 "Du bist **NICHT** gemutet.\r\n"
#                                                                 "\r\n"
#                                                                 "Der Server wurde von einem Teammitglied gesperrt.\r\n"
#                                                                 "**Niemand kann Schreiben!**\r\n"
#                                                                 "\r\n"
#                                                                 "__English:__\r\n"
#                                                                 "You're **NOT** muted.\r\n"
#                                                                 "\r\n"
#                                                                 "The server was lockeddown by a team member.\r\n"
#                                                                 "**Nobody can talk!**\r\n"
#                                                                 "\r\n"
#                                                                 "[Outage Server](https://discord.gg/9vHMVqCd9n)", color=0x7780ff)
#            embed1.set_footer(text=f'Verantwortlicher Moderator: {ctx.author}', icon_url=ctx.author.avatar_url)
#            embed2 = discord.Embed(title=":lock: Lockdown", description="**Gehe zu <#738831348625571891> für weitere Informationen**", color=0x7780ff)
#            await ctx.message.delete()
#            await channel.send(embed=embed1)
#        else:
#            embed = discord.Embed(description=":x: Tut mir leid, aber du bist nicht berechtigt, diesen Command auszuführen!\r\n"
#                                              "\r\n"
#                                              "__Fehlende Berechtigung:__ **Nachrichten verwalten**", color=0xff0000)
#            await ctx.send(embed=embed)
#
#
#@client.command(name='unlockdown')
#async def unlockdown(ctx):            
#        if ctx.author.guild_permissions.manage_guild:
#            memberrole = discord.utils.get(ctx.guild.roles, id=811744961204453377)
#            channel = client.get_channel(841759773519380500)
#            await memberrole.edit(permissions=discord.Permissions(send_messages=True, connect=True,
#                                                                  view_channel=True, read_messages=True, create_instant_invite=True,
#                                                                  change_nickname=True, add_reactions=True, speak=True, stream=True,
#                                                                  embed_links=True, external_emojis=True, use_voice_activation=True,
#                                                                  read_message_history=True, attach_files=True))
#            embed1 = discord.Embed(title=":unlock: Lockdown", description="**Lockdown aufgehoben!**", color=0x7780ff)
#            embed1.set_footer(text=f'Verantwortlicher Moderator: {ctx.author}', icon_url=ctx.author.avatar_url)
#            await channel.send(embed=embed1)
#            await ctx.message.delete()
#        else:
#            embed = discord.Embed(description=":x: Tut mir leid, aber du bist nicht berechtigt, diesen Command auszuführen!\r\n"
#                                              "\r\n"
#                                              "__Fehlende Berechtigung:__ **Nachrichten verwalten**", color=0xff0000)
#            await ctx.send(embed=embed)


@client.command(name='gn')
async def gn(ctx):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    await ctx.send(f'{ctx.author.mention} **Wünscht eine gute Nacht!** <a:JC_sleepybaby:821043309878181948>')
    await ctx.message.delete()
    

@client.command(name='gm')
async def gm(ctx):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    await ctx.send(f'{ctx.author.mention} **Schreit guten Morgen in den Raum!** <a:JC_pikagreet:855564460969820186>')
    await ctx.message.delete()


@client.command(name='w')
async def w(ctx):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    await ctx.send(f'Herzlich willkommen auf **{ctx.guild.name}**! <a:JC_dancethad:817550422910697563>')


@client.command(name='kiss')
async def kiss(ctx, user: discord.User):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**', hidden=True)
        return
    await ctx.send(f'{ctx.author.mention} gibt {user.mention} einen Kuss. <a:JC_mochakiss:855565360643833866>')
    await ctx.message.delete()

@kiss.error
async def kiss_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)
        

@client.command(name='hug')
async def hug(ctx, user: discord.User):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    await ctx.send(f'{ctx.author.mention} drückt {user.mention} ganz fest. <a:JC_mochahug:855564902584680528>')

@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)

@slash.slash(name="fight",
             description="Kämpfe mit einem anderen Nutzer.",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="user",
                    description="Erwähne einen Nutzer mit dem du Kämpfst.",
                    option_type=6,
                    required=True
                )
             ])
async def _fight(ctx: SlashContext, user: discord.User):
    if rp_enabled == False:
        await ctx.send('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**', hidden=True)
        return
    await ctx.send(f'Anfrage an **{user}** versendet.', hidden=True)
    msg = await ctx.channel.send(f'{ctx.author.mention} fordert {user.mention} zum Kampf heraus.', components=[Button(style=3, label="Accept")])

    def check(res):
        return res.user == user and res.channel == ctx.channel
    
    try:
        fighters = [ctx.author, user]
        winner = random.choice(fighters)
        res = await client.wait_for("button_click", check=check, timeout=60.0)
        await res.respond(type=6)
        await msg.edit(components=[Button(style=3, label="Kämpft", disabled=True)])
        await asyncio.sleep(1)
        await msg.edit(components=[Button(style=2, label="Beendet", disabled=True)])
        await msg.reply(f'{winner.mention} hat den Kampf gewonnen! <a:JC_KMS:817776207197241395>')
        #await res.reply(f'{winner.mention} hat den Kampf gewonnen! <a:JC_KMS:817776207197241395>')
        #await res.respond(type=InteractionType.ChannelMessageWithSource, content=f'{winner.mention} hat den Kampf gewonnen! <a:JC_KMS:817776207197241395>')
    except asyncio.TimeoutError:
        await msg.edit(components=[Button(style=2, label="Timed out", disabled=True)])

@client.command(name='fight')
@commands.cooldown(1, 30, type=BucketType.user)
async def fight(ctx, user: discord.User):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    msg = await ctx.send(f'{ctx.author.mention} fordert {user.mention} zum Kampf heraus.', components=[Button(style=3, label="Accept")])

    def check(res):
        return res.user == user and res.channel == ctx.channel
    
    try:
        fighters = [ctx.author, user]
        winner = random.choice(fighters)
        res = await client.wait_for("button_click", check=check, timeout=60.0)
        await res.respond(type=6)
        await msg.edit(components=[Button(style=3, label="Kämpft", disabled=True)])
        await asyncio.sleep(1)
        await msg.edit(components=[Button(style=2, label="Beendet", disabled=True)])
        await msg.reply(f'{winner.mention} hat den Kampf gewonnen! <a:JC_KMS:817776207197241395>')
        #await res.reply(f'{winner.mention} hat den Kampf gewonnen! <a:JC_KMS:817776207197241395>')
        #await res.respond(type=InteractionType.ChannelMessageWithSource, content=f'{winner.mention} hat den Kampf gewonnen! <a:JC_KMS:817776207197241395>')
    except asyncio.TimeoutError:
        await msg.edit(components=[Button(style=2, label="Timed out", disabled=True)])

@fight.error
async def fight_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)
    


@client.command(name='russianroulette', aliases=['rr'])
@commands.cooldown(1, 30, type=BucketType.user)
async def russianroulette(ctx, user: discord.User=None):
    embed = discord.Embed(title='Russian Roulette', description=f'{ctx.author.mention} die Trommel wurde gedreht.', color=0xE31316)
    msg = await ctx.send(embed=embed, components=[Button(style=1, label="Feuer!")])

    def check(res):
        return res.user == ctx.author and res.channel == ctx.channel
    
    try:
        nums = [1, 2, 3, 4, 5]
        bullet = random.choice(nums)
        res = await client.wait_for("button_click", check=check, timeout=10.0)
        treffer = [2, 4]
        if bullet in treffer:
            muterole = client.get_guild(776912251944435723).get_role(868012378955075614)
            await msg.edit(components=[Button(style=4, label="Treffer", disabled=True)])
            await msg.reply(f'{ctx.author.mention} die Kugel hat leider getroffen. RIP')
            await res.respond(content='Du wurdest für `30 Sekunden` gemuted, da die letze Kugel getroffen hat.')
            await ctx.author.add_roles(muterole)
            await asyncio.sleep(30)
            await ctx.author.remove_roles(muterole)
        else:
            await msg.edit(components=[Button(style=3, label="Kein Treffer", disabled=True)])
            await msg.reply(f'{ctx.author.mention} die Kugel hat nicht getroffen. GG!')
            await res.respond(type=6)
    except asyncio.TimeoutError:
        await msg.edit(components=[Button(style=2, label="Timed out", disabled=True)])


@client.command(name='slap')
async def slap(ctx, user: discord.User):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    await ctx.send(f'{ctx.author.mention} gibt {user.mention} eine klatsche. <a:JC_slap:855565487606071316>')
    await ctx.message.delete()

@slap.error
async def slap_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='kill')
async def kill(ctx, user: discord.User):
    if rp_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die RP-Befehle sind vorübergehend deaktiviert!**')
        return
    await ctx.send(f'{ctx.author.mention} möchte {user.mention} töten. <a:JC_pikakill:855565423486959636>')
    await ctx.message.delete()

@kill.error
async def kill_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command()
async def movefrom(ctx, fromchannel: discord.VoiceChannel, tochannel: discord.VoiceChannel):
    if ctx.author.guild_permissions.move_members and ctx.author.guild_permissions.manage_messages:
        msg = await ctx.send(f'<a:JC_Timer:830745906327453696> **Verschiebung gestartet...**')
        count = 0
        for allmembers in fromchannel.members:
            if role in allmembers.roles:
                await allmembers.move_to(tochannel)
                count += 1
        if count == 0:
            count = 'Keine'
        await msg.edit(f'<:JC_check:826282165423046666> **Verschiebung abgeschlossen!**\r\nVerschobene Mitglieder: `{count}`')

@client.command()
async def moveall(ctx, channel: discord.VoiceChannel=None, role: discord.Role=None):
    voicec = ctx.author.voice
    if ctx.author.guild_permissions.administrator:
        if channel == None:
            if voicec:
                channel = voicec.channel
            else:
                await ctx.send(f'<:JC_xmark:826282095566913537> **Bitte gib einen Kanal an, wenn du selber mit keinem verbunden bist.**')
                return
        msg = await ctx.send(f'<a:JC_Timer:830745906327453696> **Verschiebung gestartet...**')
        count = 0
        if role != None:
            for allchannels in ctx.guild.voice_channels:
                members = allchannels.members
                for allmembers in members:
                    if role in allmembers.roles:
                        await allmembers.move_to(channel)
                        count += 1
            if count == 0:
                count = 'Keine'
            await msg.edit(f'<:JC_check:826282165423046666> **Verschiebung abgeschlossen!**\r\nVerschobene Mitglieder: `{count}`')
        else:
            for allchannels in ctx.guild.voice_channels:
                members = allchannels.members
                for allmembers in members:
                    if not allmembers.bot:
                        await allmembers.move_to(channel)
                        count += 1
            if count == 0:
                count = 'Keine'
            await msg.edit(f'<:JC_check:826282165423046666> **Verschiebung abgeschlossen!**\r\nVerschobene Mitglieder: `{count}`')




@client.command()
async def vc(ctx, cmd, *, value=None):
    if vc_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Das Custom-Voice System wurde vom Team vorübergehend deaktiviert.**')
        return
    voicec = ctx.author.voice
    if cmd == 'cleanup':
        if ctx.author.guild_permissions.manage_messages:
            count = 0
            embed = discord.Embed(title='**Custom Voice**', description='<a:JC_Timer:830745906327453696> **Die Kanäle werden gereinigt.**', color=0xE31316)
            msg = await ctx.send(embed=embed)
            for emptychannels in ctx.guild.voice_channels:
                if emptychannels.category.id == 850113571215900677:
                    if len(emptychannels.members) == 0:
                        if emptychannels.id != 850113572373266444:
                            await emptychannels.delete()
                            count += 1
            embed2 = discord.Embed(title='**Custom Voice**', description=f'<:JC_check:826282165423046666> **Bereinigung abgeschlossen.**\r\n\r\nGelöschte Kanäle: `{str(count)}`', color=0xE31316)
            await msg.edit(embed=embed2)
            logchannel = client.get_channel(868012640616714251)
            logembed = discord.Embed(description=f'{ctx.author.mention} hat `{count}` Kanäle mit einem Cleanup bereinigt.', timestamp=datetime.now(), color=discord.Colour.orange())
            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)
    elif voicec:
        channel = voicec.channel
        if channel.category_id == 868012524312862770:
            if channel.permissions_for(ctx.author).manage_channels:
                if cmd == 'lock':
                    await channel.set_permissions(ctx.guild.default_role, connect=False)
                    embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde geschlossen**', color=0xE31316)
                    await ctx.send(embed=embed)
                    logchannel = client.get_channel(868012640616714251)
                    logembed = discord.Embed(description=f'**{channel.name}** wurde geschlossen.', timestamp=datetime.now(), color=discord.Colour.gold())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)

                elif cmd == 'unlock':
                    await channel.set_permissions(ctx.guild.default_role, connect=None)
                    embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde geöffnet**', color=0xE31316)
                    await ctx.send(embed=embed)
                    logchannel = client.get_channel(868012640616714251)
                    logembed = discord.Embed(description=f'**{channel.name}** wurde geöffnet.', timestamp=datetime.now(), color=discord.Colour.gold())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)
                elif cmd == 'hide':
                    await channel.set_permissions(ctx.guild.default_role, view_channel=False)
                    embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde versteckt**', color=0xE31316)
                    await ctx.send(embed=embed)
                    logchannel = client.get_channel(868012640616714251)
                    logembed = discord.Embed(description=f'**{channel.name}** wurde versteckt.', timestamp=datetime.now(), color=discord.Colour.gold())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)
                elif cmd == 'unhide':
                    await channel.set_permissions(ctx.guild.default_role, view_channel=None)
                    embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde aufgedeckt**', color=0xE31316)
                    await ctx.send(embed=embed)
                    logchannel = client.get_channel(868012640616714251)
                    logembed = discord.Embed(description=f'**{channel.name}** wurde aufgedeckt.', timestamp=datetime.now(), color=discord.Colour.gold())
                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                    logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=logembed)
                elif cmd == 'rename':
                    if value != None:
                        oldname = channel.name
                        await channel.edit(name=str(value))
                        embed = discord.Embed(title='**Custom Voice**', description=f'<:JC_check:826282165423046666> **Der Name deines Kanals wurde auf _{value}_ aktualisiert**', color=0xE31316)
                        await ctx.send(embed=embed)
                        logchannel = client.get_channel(868012640616714251)
                        logembed = discord.Embed(description=f'**{channel.name}** wurde von `{oldname}` zu `{channel.name}` umbenannt.', timestamp=datetime.now(), color=discord.Colour.gold())
                        logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe den neuen Namen an.**', color=0xE31316)
                        await ctx.send(embed=embed)
                elif cmd == 'limit':
                    if value != None:
                        if value == '0':
                            await channel.edit(user_limit=None)
                            embed = discord.Embed(title='**Custom Voice**', description=f'<:JC_check:826282165423046666> **Das Userlimit deines Kanals wurde auf `{value}` aktualisiert.**', color=0xE31316)
                            await ctx.send(embed=embed)
                            logchannel = client.get_channel(868012640616714251)
                            logembed = discord.Embed(description=f'Das Userlimit von **{channel.name}** wurde auf `{value}` aktualisiert.', timestamp=datetime.now(), color=discord.Colour.gold())
                            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                            await logchannel.send(embed=logembed)
                        elif int(value):
                            await channel.edit(user_limit=int(value))
                            embed = discord.Embed(title='**Custom Voice**', description=f'<:JC_check:826282165423046666> **Das Userlimit deines Kanals wurde auf `{value}` aktualisiert.**', color=0xE31316)
                            await ctx.send(embed=embed)
                            logchannel = client.get_channel(868012640616714251)
                            logembed = discord.Embed(description=f'Das Userlimit von **{channel.name}** wurde auf `{value}` aktualisiert.', timestamp=datetime.now(), color=discord.Colour.gold())
                            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                            await logchannel.send(embed=logembed)
                        else:
                            embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe das neue Limit an.**', color=0xE31316)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe das neue Limit an.**', color=0xE31316)
                        await ctx.send(embed=embed)
                elif cmd == 'add':
                    if value != None:
                        if int(value):
                            user = client.get_user(int(value))
                            await channel.set_permissions(user, view_channel=True, connect=True, speak=True)
                            embed = discord.Embed(title='**Custom Voice**', description=f'<:JC_check:826282165423046666> {user.mention} **wurde zu deinem Kanal hinzugefügt.**', color=0xE31316)
                            await ctx.send(embed=embed)
                            logchannel = client.get_channel(868012640616714251)
                            logembed = discord.Embed(description=f'{user.mention} wurde **{channel.name}** hinzugefügt.', timestamp=datetime.now(), color=discord.Colour.gold())
                            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                            await logchannel.send(embed=logembed)
                        else:
                            embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe die ID eines Nutzers an.**', color=0xE31316)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe die ID eines Nutzers an.**', color=0xE31316)
                        await ctx.send(embed=embed)
                elif cmd == 'remove':
                    if value != None:
                        if int(value):
                            user = client.get_user(int(value))
                            await channel.set_permissions(user, overwrite=None)
                            embed = discord.Embed(title='**Custom Voice**', description=f'<:JC_check:826282165423046666> {user.mention} **wurde aus deinem Kanal entfernt.**', color=0xE31316)
                            await ctx.send(embed=embed)
                            logchannel = client.get_channel(868012640616714251)
                            logembed = discord.Embed(description=f'{user.mention} wurde von **{channel.name}** entfernt.', timestamp=datetime.now(), color=discord.Colour.gold())
                            logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                            await logchannel.send(embed=logembed)
                        else:
                            embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe die ID eines Nutzers an.**', color=0xE31316)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte gebe die ID eines Nutzers an.**', color=0xE31316)
                        await ctx.send(embed=embed)
                elif cmd == 'transfer':
                    if value != None:
                        if int(value):
                            user = client.get_user(int(value))
                            embed = discord.Embed(title='**Custom Voice**', description=f'Bist du sicher dass du den Kanal {channel.mention} an {user.mention} übertragen möchtest?', color=0xE31316)
                            embed.set_footer(text='"Ja" zum Bestätigen')
                            msg = await ctx.send(embed=embed, components=[[Button(style=3, label="Ja"), Button(style=4, label="Nein")]])

                            def check(res):
                                return ctx.author == res.user and res.channel == ctx.channel

                            try:
                                res = await client.wait_for("button_click", check=check, timeout=30)
                                await res.respond(type=6)
                                if res.component.label == 'Ja':
                                    successembed = discord.Embed(title='**Custom Voice**', description=f'Der Kanal {channel.mention} wurde an {user.mention} übertragen.', color=discord.Colour.green())
                                    successembed.set_footer(text='Bestätigt')
                                    await channel.set_permissions(user, view_channel=True, connect=True, move_members=True, manage_channels=True,
                                                                        deafen_members=True, mute_members=True, speak=True)
                                    await channel.set_permissions(ctx.author, view_channel=True, connect=True, speak=True)
                                    await msg.edit(embed=successembed, components=[[Button(style=3, label="Ja", disabled=True), Button(style=4, label="Nein", disabled=True)]])
                                    logchannel = client.get_channel(868012640616714251)
                                    logembed = discord.Embed(description=f'**{channel.name}** wurde an {user.mention} übertragen.', timestamp=datetime.now(), color=discord.Colour.orange())
                                    logembed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
                                    logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                                    await logchannel.send(embed=logembed)
                                else:
                                        await msg.edit(components=[[Button(style=3, label="Ja", disabled=True), Button(style=4, label="Nein", disabled=True)]])
                            
                            except asyncio.TimeoutError:
                                await msg.edit(components=[[Button(style=3, label="Ja", disabled=True), Button(style=4, label="Nein", disabled=True)]])
            else:
                embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Du hast keine Berechtigungen für änderungen an diesem Kanal!**', color=0xE31316)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Du hast keine Berechtigungen für änderungen an diesem Kanal!**', color=0xE31316)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='**Custom Voice**', description='<:JC_xmark:826282095566913537> **Bitte tritt einem Custom Voice bei, bevor du diesen Befehl verwenden kannst.**', color=0xE31316)
        await ctx.send(embed=embed)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        #with open("neverland_voices.json") as f:
        #    vcdata = json.load(f)
        def voicecheck(x, y, z):
            return len(newchannel.members) == 0
        if after.channel.id == 868012547062775818:
            if vc_enabled == False:
                await member.move_to(channel=None, reason='Custom-VC closed')
                return
            #for guild in client.guilds:
            maincategory = client.get_channel(868012524312862770)
            newchannel = await member.guild.create_voice_channel(name=f'⏳ {member.name}', category=maincategory)
            await newchannel.set_permissions(member, connect=True, manage_channels=True,
                                            deafen_members=True, mute_members=True, speak=True)
            await member.move_to(newchannel)

            logchannel = client.get_channel(868012640616714251)
            logembed = discord.Embed(description=f'**{newchannel.name}** wurde als Custom-Voice von {member.mention} erstellt.', timestamp=datetime.now(), color=discord.Colour.blurple())
            logembed.set_author(name=member.name + '#' + member.discriminator, icon_url=member.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)

            await client.wait_for('voice_state_update', check=voicecheck)

            logchannel = client.get_channel(868012640616714251)
            logembed = discord.Embed(description=f'**{newchannel.name}** wurde nach verwendung wieder gelöscht.', timestamp=datetime.now(), color=discord.Colour.red())
            logembed.set_author(name=member.name + '#' + member.discriminator, icon_url=member.avatar_url)
            logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
            await logchannel.send(embed=logembed)

            await newchannel.delete()


#@client.event
#async def on_guild_channel_create(channel):
#    ctx = client.get_context
    #if 'ticket-' in channel.name:
    #    if channel.category_id == 868012518658965574:
    #        await channel.send('Guten Tag und herzlich willkommen in deinem Ticket.\r\n'
    #                            'Bitte wähle eine der folgenden Kategorien, damit das Team dir gezielt weiterhelfen kann.\r\n'
    #                            '\r\n'
    #                            '`1` - **Allgemeine Frage oder Anliegen**\r\n'
    #                            '`2` - **Frage bezüglich des Servers** (d.h. chatroom, tipico, etc...)\r\n'
    #                            '`3` - **Report oder Meldung eines Nutzers**\r\n'
    #                            '`4` - **Frage zum Team**\r\n'
    #                            '`5` - **Frage zu unseren Bots**\r\n'
    #                            '\r\n'
    #                            '`Bitte sende die dazugehörige Zahl in den Chat um die Kategorie auszuwählen.`\r\n'
    #                            '__Sollte innerhalb **10 Minuten** keine Antwort kommen, wird das Ticket geschlossen.__')
    #        def check(m):
    #            return m.channel == channel and not m.author.bot
#
    #        try:
    #            msg = await client.wait_for('message', timeout=600, check=check)
#
    #        except asyncio.TimeoutError:
    #            ticketrole = client.get_guild(776912251944435723).get_role(868012371912847411)
    #            ticketbot = client.get_user(771464798176149536)
    #            clsoverwrites = None
    #            overwrites = {
    #                channel.guild.default_role: discord.PermissionOverwrite(read_messages=False,
    #                                                                        send_messages=True),
    #                ticketrole: discord.PermissionOverwrite(read_messages=True),
    #                ticketbot: discord.PermissionOverwrite(read_messages=True, send_messages=True,
    #                                                       manage_channels=True),
    #                channel.guild.me: discord.PermissionOverwrite(read_messages=True)
    #            }
    #            await channel.edit(overwrites=clsoverwrites)
    #            await channel.edit(overwrites=overwrites)
    #            await channel.send(":warning: **Das Ticket wurde geschlossen da der Nutzer keine Zahl angegeben hat.**")
    #        else:
    #            if msg.content.lower() == "1":
    #                await channel.send('Es geht um **eine Allgemeine Frage oder Anliegen**.\r\n'
    #                                   'Bitte nenne uns dein Anliegen so detailgenau wie möglich.')
    #            elif msg.content.lower() == "2":
    #                await channel.send('Es geht um **eine Frage bezüglich des Servers**.\r\n'
    #                                   'Bitte nenne uns dein Anliegen so detailgenau wie möglich.')
    #            elif msg.content.lower() == "3":
    #                await channel.send('Es geht um **einen Report oder Meldung eines Nutzers**.\r\n'
    #                                   'Bitte nenne uns dein Anliegen so detailgenau wie möglich.')
    #            elif msg.content.lower() == "4":
    #                await channel.send('Es geht um **eine Frage zum Team**.\r\n'
    #                                   'Bitte nenne uns dein Anliegen so detailgenau wie möglich.')
    #            elif msg.content.lower() == "5":
    #                await channel.send('Es geht um **eine Frage zu unseren Bots**.\r\n'
    #                                   'Bitte nenne uns dein Anliegen so detailgenau wie möglich.\r\n'
    #                                   'Der Developer <@!515602740500627477> wird sich daraufhin um dich kümmern.')
    #            else:
    #                await channel.send(':x: Deine Nachricht konnte keiner Kategorie zugeordnet werden.\r\n'
    #                                   'Daher geht es um **eine Allgemeine Frage oder Anliegen**.')

tickettimeout = []

@client.command(pass_context=True)
async def ticket(ctx, cmd, user: discord.Member=None, amount: int=None):
    global tickettimeout
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    #if ctx.channel.id in data["ticket-channel-ids"]:
    logchannel = client.get_channel(868012587936268369)
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if cmd.lower() == 'timeout':
        if teamrole in ctx.author.roles:
            data["ticket-blacklist"].append(user.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f)
            embed = discord.Embed(description=f'{user.mention} wurde in timeout versetzt', color=0xE31316)
            msg = await ctx.channel.send(embed=embed)
    if cmd.lower() == 'untimeout':
        if teamrole in ctx.author.roles:
            data["ticket-blacklist"].remove(user.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f)
            embed = discord.Embed(description=f'{user.mention} wurde aus dem timeout befreit', color=0xE31316)
            msg = await ctx.channel.send(embed=embed)
    if cmd.lower() == 'allclaimed':
        if ctx.author.guild_permissions.administrator:
            with open("./JOBCENTER/jc_ticket_claimed.json") as f:
                data2 = json.load(f)
            keys = []
            values = []
            for allusers in data2.keys():
                user = client.get_user(int(allusers))
                keys.append(user.name)
            for allusers in data2:
                values.append(str(data2[allusers]))
            embed = discord.Embed(title="Claimed Tickets", color=0xE31316)
            if keys:
                embed.add_field(name="Users:", value="\r\n".join(keys), inline=True)
                embed.add_field(name="Count:", value="\r\n".join(values), inline=True)
            else:
                embed.add_field(name="Users:", value="Keine Daten...")
            embed.set_footer(text=ctx.guild.name)
            await ctx.send(embed=embed)
                
    if cmd.lower() == 'claimed':
        if teamrole in ctx.author.roles:
            with open("./JOBCENTER/jc_ticket_claimed.json") as f:
                data2 = json.load(f)
            if user == None:
                user = ctx.author
            if str(user.id) in data2:
                count = data2[str(user.id)]
                if count != 0:
                    if user == ctx.author:
                        await ctx.send(f'Du hast bis jetzt `{count}` Tickets geclaimt.')
                    else:
                        await ctx.send(f'**{ctx.author}** hat bis jetzt `{count}` Tickets geclaimt.')
                else:
                    if user == ctx.author:
                        await ctx.send('Du hast bis jetzt **keine** Tickets geclaimt.')
                    else:
                        await ctx.send(f'**{ctx.author}** hat bis jetzt **keine** Tickets geclaimt.')
            else:
                if user == ctx.author:
                    await ctx.send('<:JC_xmark:826282095566913537> Ich habe dich nicht in der Datenbank gefunden.')
                else:
                    await ctx.send('<:JC_xmark:826282095566913537> Ich habe den Nutzer nicht in der Datenbank gefunden.')
    #if cmd.lower() == 'setclaimed':
    #    if ctx.author.guild_permissions.administrator:
    #        with open("./JOBCENTER/jc_ticket_claimed.json") as f:
    #            data2 = json.load(f)
    #        if user == None:
    #            user = ctx.author
    #        if str(user.id) in data2:
    #            if user == None:
    #                user == ctx.author
    #            data2[user.id] = amount
    #            await ctx.send(f'**{user}** hat jetzt `{amount}` Tickets geclaimt.')
    #            with open("./JOBCENTER/jc_ticket_claimed.json", 'w') as f:
    #                json.dump(data2, f)
    #        else:
    #            if user == ctx.author:
    #                await ctx.send('<:JC_xmark:826282095566913537> Ich habe dich nicht in der Datenbank gefunden.')
    #            else:
    #                await ctx.send('<:JC_xmark:826282095566913537> Ich habe den Nutzer nicht in der Datenbank gefunden.')
    if cmd.lower() == 'updatedata':
        if ctx.author.guild_permissions.administrator:
            with open("./JOBCENTER/jc_ticket_claimed.json") as f:
                data2 = json.load(f)
            if user != None:
                if not str(user.id) in data2:
                    newuser = {str(user.id): 0}
                    data2[str(user.id)] = 0
                    with open("./JOBCENTER/jc_ticket_claimed.json", 'w') as f:
                        json.dump(data2, f)
                    await ctx.send(f'<:JC_check:826282165423046666> **{user}**(`{user.id}`) zur Datenbank hinzugefügt')

@client.command(pass_context=True)
async def claim(ctx):
    global tickettimeout
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    if ctx.channel.id in data["ticket-channel-ids"]:
        logchannel = client.get_channel(868012587936268369)
        teamrole = client.get_guild(776912251944435723).get_role(868012371912847411)
        if teamrole in ctx.author.roles:
            embed = discord.Embed(description=f'{ctx.author.mention} wird sich ab jetzt um dich kümmern.', color=discord.Color.gold())
            ticket_number = int(data["ticket-counter"])
            await ctx.channel.edit(name=f'claimed-{ticket_number}')
            msg = await ctx.channel.send(embed=embed)
            await ctx.message.delete()
            logembed = discord.Embed(title='Log - Ticket übertragen', description=f'Das Ticket **#{ctx.channel.name}** ({ctx.channel.mention}) wurde an **{ctx.author}** übertragen.', color=discord.Colour.gold())
            await logchannel.send(embed=logembed)

@client.command(pass_context=True)
async def close(ctx, member: discord.Member=None, *, grund=None):
    global tickettimeout
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    if ctx.channel.id == 846474040197906492:
        #de = pytz.timezone('Europe/Berlin')

        embed = discord.Embed(
            colour=discord.Colour.red(),
            title='<a:achtung:818524559594487839> **__ModMail__** <a:achtung:818524559594487839>',
            description=f'**Ihr ModMail-Ticket wurde geschlossen.**\r\n'
                         'Um ein neues Ticket zu öffnen, sende einfach eine neue Nachricht.'
        )
        if not grund == None:
            embed.add_field(name='**Reason:**', value=f'{grund}')
        else:
            embed.add_field(name='**Reason:**', value=f'No Reason given.')
        embed.set_footer(text=f'Gesprächspartner: {ctx.author.name}. - Do not reply to this message!', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await member.send(embed=embed)
        await ctx.message.add_reaction('✅')
    elif ctx.channel.id in data["ticket-channel-ids"]:
        logchannel = client.get_channel(868012587936268369)
        teamrole = client.get_guild(776912251944435723).get_role(868012371912847411)
        embed = discord.Embed(description=':lock: **Dieses Ticket wurde geschlossen.**\r\n'
                                          '*Reagiere mit* ⛔ *um das Ticket endgültig zu löschen.*', color=discord.Color.orange())
        embed.set_footer(text='Reagiere innerhalb 60 Sekunden')
        timeoutembed = discord.Embed(description=':lock: **Dieses Ticket wurde geschlossen.**\r\n'
                                                 '`,delete` *um das Ticket endgültig zu löschen.*', color=discord.Color.orange())
        ticket_number = int(data["ticket-counter"])
        clsoverwrites = None
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                    send_messages=True),
            teamrole: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        await ctx.channel.edit(overwrites=clsoverwrites)
        await ctx.channel.edit(overwrites=overwrites)
        await ctx.channel.edit(name=f'closed-{ticket_number}')
        
        if str(ctx.channel.id) in data["tickets"][0]:
            data["tickets"][0].pop(str(ctx.channel.id))

            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f)

        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction('⛔')
        await ctx.message.delete()
        logembed = discord.Embed(title='Log - Ticket geschlossen', description=f'Das Ticket **#{ctx.channel.name}** ({ctx.channel.mention}) wurde von **{ctx.author.name}** geschlossen.', color=discord.Colour.orange())
        await logchannel.send(embed=logembed)

        #with open("./JOBCENTER/jc_ticketusers.json") as f:
        #    users = json.load(f)
        #for allusers in ctx.channel.members:
        #    if allusers.id in users["ids"]:
        #        users["ids"].remove(allusers.id)
        #with open("./JOBCENTER/jc_ticketusers.json", 'w') as f:
        #    json.dump(users, f)

        def check(reaction, user):
            return str(reaction.emoji) == '⛔' and teamrole in ctx.author.roles

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60, check=check)
            embed2 = discord.Embed(description='**Dieses Ticket wird in `5` Sekunden gelöscht...**', color=0xff0000)
            await ctx.send(embed=embed2)
            await asyncio.sleep(5)
            logembed = discord.Embed(title='Log - Ticket geschlossen', description=f'Das Ticket **#{ctx.channel.name}** wurde von **{ctx.author.name}** endgültig gelöscht.', color=discord.Colour.red())
            msg = await logchannel.send(embed=logembed)
            data["ticket-channel-ids"].remove(ctx.channel.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f)
            await ctx.channel.delete()
        except asyncio.TimeoutError:
            await msg.edit(embed=timeoutembed)
            await msg.clear_reactions()

@client.command(pass_context=True)
async def delete(ctx):
    global tickettimeout
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    if ctx.channel.id in data["ticket-channel-ids"]:
        logchannel = client.get_channel(868012587936268369)
        teamrole = client.get_guild(776912251944435723).get_role(868012371912847411)
        if teamrole in ctx.author.roles:
            embed2 = discord.Embed(description='**Dieses Ticket wird in `5` Sekunden gelöscht...**', color=0xff0000)
            await ctx.send(embed=embed2)
            await asyncio.sleep(5)
            logembed = discord.Embed(title='Log - Ticket geschlossen', description=f'Das Ticket **#{ctx.channel.name}** wurde von **{ctx.author.name}** endgültig gelöscht.', color=discord.Colour.red())
            msg = await logchannel.send(embed=logembed)
            data["ticket-channel-ids"].remove(ctx.channel.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f, indent=4)
            await ctx.channel.delete()

@client.command(pass_context=True, aliases=['add'])
async def adduser(ctx, user: discord.Member):
    global tickettimeout
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    if ctx.channel.id in data["ticket-channel-ids"]:
        logchannel = client.get_channel(868012587936268369)
        teamrole = client.get_guild(776912251944435723).get_role(868012371912847411)
        embed = discord.Embed(description=f'{user.mention} (**{user}**) wurde zum Ticket {ctx.channel.mention} hinzugefügt.', color=discord.Color.blue())
        await ctx.channel.set_permissions(user, read_messages=True, send_messages=True)
        msg = await ctx.channel.send(embed=embed)

@client.command(pass_context=True, aliases=['remove'])
async def removeuser(ctx, user: discord.Member):
    global tickettimeout
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    if ctx.channel.id in data["ticket-channel-ids"]:
        logchannel = client.get_channel(868012587936268369)
        teamrole = client.get_guild(776912251944435723).get_role(868012371912847411)
        if not user == ctx.author:
            embed = discord.Embed(description=f'{user.mention} (**{user}**) wurde zum Ticket {ctx.channel.mention} hinzugefügt.', color=discord.Color.blue())
            await ctx.channel.set_permissions(user, overwrites=None)
            msg = await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title='ERROR', description=f'Du kannst dich nicht selber aus dem Ticket entfernen.', color=0xff0000)
            msg = await ctx.channel.send(embed=embed)


@client.event
async def on_button_click(button):
    member = button.guild.get_member(button.user.id)
    if button.channel.id == 868012642030223380:
        member = client.get_guild(button.guild.id).get_member(button.author.id)
        voicec = member.voice
        if voicec:
            channel = voicec.channel
            if channel.category_id == 868012524312862770:
                if channel.permissions_for(member).manage_channels:
                    if button.component.custom_id == "lock":
                        await channel.set_permissions(button.guild.default_role, connect=False)
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde geschlossen**', color=0xE31316)
                        await button.respond(embed=embed)
                        logchannel = client.get_channel(868012640616714251)
                        logembed = discord.Embed(description=f'**{channel.name}** wurde geschlossen.', timestamp=datetime.now(), color=discord.Colour.gold())
                        logembed.set_author(name=button.author.name + '#' + button.author.discriminator, icon_url=button.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
                    elif button.component.custom_id == "unlock":
                        await channel.set_permissions(button.guild.default_role, connect=None)
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde geöffnet**', color=0xE31316)
                        await button.respond(embed=embed)
                        logchannel = client.get_channel(868012640616714251)
                        logembed = discord.Embed(description=f'**{channel.name}** wurde geöffnet.', timestamp=datetime.now(), color=discord.Colour.gold())
                        logembed.set_author(name=button.author.name + '#' + button.author.discriminator, icon_url=button.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
                    elif button.component.custom_id == "hide":
                        await channel.set_permissions(button.guild.default_role, view_channel=False)
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde versteckt**', color=0xE31316)
                        await button.respond(embed=embed)
                        logchannel = client.get_channel(868012640616714251)
                        logembed = discord.Embed(description=f'**{channel.name}** wurde versteckt.', timestamp=datetime.now(), color=discord.Colour.gold())
                        logembed.set_author(name=button.author.name + '#' + button.author.discriminator, icon_url=button.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
                    elif button.component.custom_id == "unhide":
                        await channel.set_permissions(button.guild.default_role, view_channel=None)
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde aufgedeckt**', color=0xE31316)
                        await button.respond(embed=embed)
                        logchannel = client.get_channel(868012640616714251)
                        logembed = discord.Embed(description=f'**{channel.name}** wurde aufgedeckt.', timestamp=datetime.now(), color=discord.Colour.gold())
                        logembed.set_author(name=button.author.name + '#' + button.author.discriminator, icon_url=button.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
                    elif button.component.custom_id == "delete":
                        await channel.delete()
                        embed = discord.Embed(title='**Custom Voice**', description='<:JC_check:826282165423046666> **Dein Kanal wurde gelöscht.**', color=0xE31316)
                        await button.respond(embed=embed)
                        logchannel = client.get_channel(868012640616714251)
                        logembed = discord.Embed(description=f'**{channel.name}** wurde manuell gelöscht.', timestamp=datetime.now(), color=discord.Colour.red())
                        logembed.set_author(name=button.author.name + '#' + button.author.discriminator, icon_url=button.author.avatar_url)
                        logembed.set_footer(text=client.user.name + ' - Custom-Voice Logs', icon_url=client.user.avatar_url)
                        await logchannel.send(embed=logembed)
    if button.channel.id == 868012589207158785:
        if button.message.id == 868052276059725826:
            server = button.guild
            user = button.user
            logchannel = client.get_channel(868012587936268369)
            msgid = button.message.id
            ticketchannel = client.get_channel(868012589207158785)
            ticketmessage = await ticketchannel.fetch_message(msgid)
            with open("./JOBCENTER/jc_tickets.json") as f:
                data = json.load(f)
            if user.id in data["ticket-blacklist"]:
                await button.respond(content=f'<:JC_xmark:826282095566913537> *Du stehst auf der Ticket-Blacklist, daher kannst du derzeit kein Ticket eröffnen.*')
                return
            allusers = []
            allchannels = []
            #for allusers in data["tickets"][0].keys():
            #    allchannels.append(allusers)
            for users in data["tickets"][0].values():
                allusers.append(users)
            if user.id in allusers:
                await button.respond(content=f'<:JC_xmark:826282095566913537> *Du hat bereits ein offenes Ticket. Bitte schließe dein aktuelles Ticket vorher ab, bevor du ein neues eröffnest.*\r\n'
                                              '(Falls du denkst dass dies ein Fehler ist sende bitte eine DM an <@!515602740500627477>)')
                return
            teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
            ticketrole = client.get_guild(776912251944435723).get_role(868012371912847411)
            overwrites = {
                server.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=True),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                teamrole: discord.PermissionOverwrite(read_messages=True),
                server.me: discord.PermissionOverwrite(read_messages=True)
            }
            ticketcat = client.get_channel(868012518658965574)
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1
            data["ticket-counter"] = int(ticket_number)
            channel = await server.create_text_channel(f"ticket-{ticket_number}", category=ticketcat, overwrites=overwrites)
            data["tickets"][0][str(channel.id)] = user.id
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f, indent=4)
            data["ticket-channel-ids"].append(channel.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f, indent=4)
            await button.respond(content=f'Dein Ticket **#{ticket_number}** wurde erstellt. - {channel.mention}')
            embed = discord.Embed(title='Support-Ticket', description='Willkommen in deinem Ticket.\r\n'
                                                                      'Bitte nenne uns dein Anliegen so detailgenau wie möglich.\r\n'
                                                                      f'Ein {ticketrole.mention} wird sich in kürze um dich kümmern.', color=0xE31316)#color=discord.Colour.green())
            embed.add_field(name='Nutze die folgenden Commands um Mitglieder zum Ticket hinzuzufügen oder den Button um das Ticket zu schießen:', value= '➩ `,adduser <user>`', inline=False)
            msg = await channel.send(f'Hallo {user.mention}.', embed=embed, components=[Button(style=2, label='🔐 Ticket schließen')])
            await msg.pin()
            logembed = discord.Embed(title='Log - Ticket geöffnet', description=f'**{user}** hat ein Ticket geöffnet. Der Ticket-Kanal lautet {channel.mention}.', color=discord.Colour.dark_green())
            msg = await logchannel.send(ticketrole.mention, embed=logembed)
    with open("./JOBCENTER/jc_tickets.json") as f:
        data = json.load(f)
    if button.channel.id in data["ticket-channel-ids"]:
        if button.component.label == "🔐 Ticket schließen":
            logchannel = client.get_channel(868012587936268369)
            teamrole = client.get_guild(776912251944435723).get_role(868012371912847411)
            embed = discord.Embed(description=':lock: **Dieses Ticket wurde geschlossen.**\r\n'
                                              '*Reagiere mit* ⛔ *um das Ticket endgültig zu löschen.*', color=discord.Color.orange())
            embed.set_footer(text='Reagiere innerhalb 60 Sekunden')
            timeoutembed = discord.Embed(description=':lock: **Dieses Ticket wurde geschlossen.**\r\n'
                                                     '`,delete` *um das Ticket endgültig zu löschen.*', color=discord.Color.orange())
            ticket_number = int(data["ticket-counter"])
            clsoverwrites = None
            overwrites = {
                button.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                        send_messages=True),
                teamrole: discord.PermissionOverwrite(read_messages=True),
                button.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            
            if str(button.channel.id) in data["tickets"][0]:
                data["tickets"][0].pop(str(button.channel.id))
    
                with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                    json.dump(data, f)

            await button.channel.edit(overwrites=clsoverwrites)
            await button.channel.edit(overwrites=overwrites)
            await button.channel.edit(name=f'closed-{ticket_number}')
            msg = await button.channel.send(embed=embed)
            await msg.add_reaction('⛔')
            logembed = discord.Embed(title='Log - Ticket geschlossen', description=f'Das Ticket **#{button.channel.name}** ({button.channel.mention}) wurde von **{button.user.name}** geschlossen.', color=discord.Colour.orange())
            await logchannel.send(embed=logembed)
            await button.respond(type=6)

            #with open("./JOBCENTER/jc_ticketusers.json") as f:
            #    users = json.load(f)
            #for allusers in button.channel.members:
            #    if allusers.id in users["ids"]:
            #        users["ids"].remove(allusers.id)
            #with open("./JOBCENTER/jc_ticketusers.json", 'w') as f:
            #    json.dump(users, f)
            def check(reaction, user):
                return str(reaction.emoji) == '⛔' and teamrole in user.roles

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60, check=check)
                embed2 = discord.Embed(description='**Dieses Ticket wird in `5` Sekunden gelöscht...**', color=0xff0000)
                await button.channel.send(embed=embed2)
                await asyncio.sleep(5)
                logembed = discord.Embed(title='Log - Ticket geschlossen', description=f'Das Ticket **#{button.channel.name}** wurde von **{button.user.name}** endgültig gelöscht.', color=discord.Colour.red())
                msg = await logchannel.send(embed=logembed)
                data["ticket-channel-ids"].remove(button.channel.id)
                with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                    json.dump(data, f)
                await button.channel.delete()
            except asyncio.TimeoutError:
                await msg.edit(embed=timeoutembed)
                await msg.clear_reactions()

@client.event
async def on_raw_reaction_add(reaction):
    global tickettimeout
    user = reaction.member
    server = client.get_guild(reaction.guild_id)
    if reaction.message_id == 868457626596442112:
        if reaction.emoji == discord.PartialEmoji(name="🎫"):
            logchannel = client.get_channel(868012587936268369)
            msgid = reaction.message_id
            ticketchannel = client.get_channel(868457010369298452)
            ticketmessage = await ticketchannel.fetch_message(msgid)
            await ticketmessage.remove_reaction(discord.PartialEmoji(name="🎫"), user)
            if user.id in tickettimeout:
                return
            with open("./JOBCENTER/jc_tickets.json") as f:
                data = json.load(f)
            allusers = []
            allchannels = []
            #for allusers in data["tickets"][0].keys():
            #    allchannels.append(allusers)
            for users in data["tickets"][0].values():
                allusers.append(users)
            if user.id in allusers:
                await button.respond(content=f'<:JC_xmark:826282095566913537> *Du hat bereits ein offenes Ticket. Bitte schließe dein aktuelles Ticket vorher ab, bevor du ein neues eröffnest.*')
                return
            teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
            ticketrole = client.get_guild(776912251944435723).get_role(868012371912847411)
            overwrites = {
                server.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
                teamrole: discord.PermissionOverwrite(read_messages=True),
                server.me: discord.PermissionOverwrite(read_messages=True)
            }
            ticketcat = client.get_channel(868012518658965574)
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1
            data["ticket-counter"] = int(ticket_number)
            channel = await server.create_text_channel(f"⚠-ticket-{ticket_number}", category=ticketcat, overwrites=overwrites)
            data["tickets"][0][str(channel.id)] = user.id
            data["ticket-channel-ids"].append(channel.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f)
            await ticketchannel.send(f'Dein Ticket **#{ticket_number}** wurde erstellt. - {channel.mention}', delete_after=5)
            embed = discord.Embed(title='Sicherheits-Ticket', description='Willkommen in deinem Sicherheits-Ticket.\r\n'
                                                                          'Du bist hier da dein Account als gefährlich eingestuft wurde.\r\n'
                                                                          'Bitte folge den Anweisungen des Teams um die Sicherheitskontrolle zu verlassen.\r\n'
                                                                          f'Ein {ticketrole.mention} wird sich in kürze um dich kümmern.', color=0xE31316)#color=discord.Colour.green())
            embed.add_field(name='Nutze die folgenden Commands um Mitglieder zum Ticket hinzuzufügen oder das Ticket zu schießen:', value= '➩ `,adduser <user>`\r\n➩ `,close`', inline=False)
            msg = await channel.send(f'Hallo {user.mention}.', embed=embed)
            await msg.pin()
            logembed = discord.Embed(title='Log - Sicherheits-Ticket geöffnet', description=f'**{user}** hat ein Sicherheits-Ticket geöffnet. Der Ticket-Kanal lautet {channel.mention}.', color=discord.Colour.dark_green())
            msg = await logchannel.send(ticketrole.mention, embed=logembed)
    elif reaction.message_id == 868052276059725826:
        if reaction.emoji == discord.PartialEmoji(name="🎫"):
            logchannel = client.get_channel(868012587936268369)
            msgid = reaction.message_id
            ticketchannel = client.get_channel(868012589207158785)
            ticketmessage = await ticketchannel.fetch_message(msgid)
            await ticketmessage.remove_reaction(discord.PartialEmoji(name="🎫"), user)
            if user.id in tickettimeout:
                return
            #with open("./JOBCENTER/jc_ticketusers.json") as f:
            #    users = json.load(f)
            #if user.id in users["ids"]:
            #    await user.send('Bitte schließe dein derzeitiges Ticket vorher ab, bevor du ein neues öffnen kannst.')
            #    return
            #users['ids'].append(user.id)
            #with open("./JOBCENTER/jc_ticketusers.json", 'w') as f:
            #    json.dump(users, f)
            with open("./JOBCENTER/jc_tickets.json") as f:
                data = json.load(f)
            teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
            ticketrole = client.get_guild(776912251944435723).get_role(868012371912847411)
            overwrites = {
                server.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                teamrole: discord.PermissionOverwrite(read_messages=True),
                server.me: discord.PermissionOverwrite(read_messages=True)
            }
            ticketcat = client.get_channel(868012518658965574)
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1
            data["ticket-counter"] = int(ticket_number)
            channel = await server.create_text_channel(f"ticket-{ticket_number}", category=ticketcat, overwrites=overwrites)
            data["ticket-channel-ids"].append(channel.id)
            with open("./JOBCENTER/jc_tickets.json", 'w') as f:
                json.dump(data, f, indent=4)
            await ticketchannel.send(f'Dein Ticket **#{ticket_number}** wurde erstellt. - {channel.mention}', delete_after=5)
            embed = discord.Embed(title='Support-Ticket', description='Willkommen in deinem Ticket.\r\n'
                                                                      'Bitte nenne uns dein Anliegen so detailgenau wie möglich.\r\n'
                                                                      f'Ein {ticketrole.mention} wird sich in kürze um dich kümmern.', color=0xE31316)#color=discord.Colour.green())
            embed.add_field(name='Nutze die folgenden Commands um Mitglieder zum Ticket hinzuzufügen oder das Ticket zu schießen:', value= '➩ `,adduser <user>`\r\n➩ `,close`', inline=False)
            msg = await channel.send(f'Hallo {user.mention}.', embed=embed)
            await msg.pin()
            logembed = discord.Embed(title='Log - Ticket geöffnet', description=f'**{user}** hat ein Ticket geöffnet. Der Ticket-Kanal lautet {channel.mention}.', color=discord.Colour.dark_green())
            msg = await logchannel.send(ticketrole.mention, embed=logembed)
        else:
            msgid = reaction.message_id
            ticketchannel = client.get_channel(868012589207158785)
            ticketmessage = await ticketchannel.fetch_message(msgid)
            await ticketmessage.remove_reaction(reaction.emoji, user)
### Tickt-System Ende
    #if reaction.channel_id == 868012626951680010:
    #    channel = client.get_channel(reaction.channel_id)
    #    msg = await channel.fetch_message(reaction.message_id)
    #    if msg.author == client.user:
    #        if reaction.emoji == discord.PartialEmoji(name="👎") or reaction.emoji == discord.PartialEmoji(name="👍"):
    #            print(msg.reactions)
### Reaction Roles Anfang
    if reaction.channel_id == 868012609616621568:
        if reaction.message_id == 870664032376463430:
            if reaction.emoji == discord.PartialEmoji(name="🇩🇪"):
                role = client.get_guild(776912251944435723).get_role(869140610035118110)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🇦🇹"):
                role = client.get_guild(776912251944435723).get_role(869140672505061396)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🇨🇭"):
                role = client.get_guild(776912251944435723).get_role(869141160118067270)
                await user.add_roles(role)
        elif reaction.message_id == 870664063724711976:
            if reaction.emoji == discord.PartialEmoji(name="👶"):
                role = client.get_guild(776912251944435723).get_role(868012504914206720)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="👦"):
                role = client.get_guild(776912251944435723).get_role(868012504050196481)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🧑"):
                role = client.get_guild(776912251944435723).get_role(868012503332974602)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="👨"):
                role = client.get_guild(776912251944435723).get_role(869140063076905010)
                await user.add_roles(role)
        elif reaction.message_id == 870664149275934771:
            if reaction.emoji == discord.PartialEmoji(name="🚹"):
                role = client.get_guild(776912251944435723).get_role(868012505870524416)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🚺"):
                role = client.get_guild(776912251944435723).get_role(868012506675818526)
                await user.add_roles(role)
        elif reaction.message_id == 870664196696731678:
            if reaction.emoji == discord.PartialEmoji(name="💛"):
                role = client.get_guild(776912251944435723).get_role(869141232281079808)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💜"):
                role = client.get_guild(776912251944435723).get_role(869141295468249148)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💙"):
                role = client.get_guild(776912251944435723).get_role(869141424279547914)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="❤️"):
                role = client.get_guild(776912251944435723).get_role(869141342641598484)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🧡"):
                role = client.get_guild(776912251944435723).get_role(869141668488687647)
                await user.add_roles(role)
        elif reaction.message_id == 870664268066983936:
            if reaction.emoji == discord.PartialEmoji(name="🍑"):
                role = client.get_guild(776912251944435723).get_role(869141928762028053)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🍋"):
                role = client.get_guild(776912251944435723).get_role(869141974798725160)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🥙"):
                role = client.get_guild(776912251944435723).get_role(869141809362796554)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🍟"):
                role = client.get_guild(776912251944435723).get_role(869141765498740737)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🖥"):
                role = client.get_guild(776912251944435723).get_role(869142038766026752)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="📱"):
                role = client.get_guild(776912251944435723).get_role(869142088866988062)
                await user.add_roles(role)
        elif reaction.message_id == 870664298467315712:
            if reaction.emoji == discord.PartialEmoji(name="❤️"):
                role = client.get_guild(776912251944435723).get_role(870657460803866646)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💜"):
                role = client.get_guild(776912251944435723).get_role(870659688021262346)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💛"):
                role = client.get_guild(776912251944435723).get_role(869707827734790154)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💚"):
                role = client.get_guild(776912251944435723).get_role(870649082333507644)
                await user.add_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💙"):
                role = client.get_guild(776912251944435723).get_role(870659091809304606)
                await user.add_roles(role)
### Reaction Roles Ende

@client.event
async def on_raw_reaction_remove(reaction):
    user = client.get_guild(776912251944435723).get_member(reaction.user_id)
    server = client.get_guild(reaction.guild_id)
### Reaction Roles Anfang
    if reaction.channel_id == 868012609616621568:
        if reaction.message_id == 870664032376463430:
            if reaction.emoji == discord.PartialEmoji(name="🇩🇪"):
                role = client.get_guild(776912251944435723).get_role(869140610035118110)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🇦🇹"):
                role = client.get_guild(776912251944435723).get_role(869140672505061396)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🇨🇭"):
                role = client.get_guild(776912251944435723).get_role(869141160118067270)
                await user.remove_roles(role)
        if reaction.message_id == 870664063724711976:
            if reaction.emoji == discord.PartialEmoji(name="👶"):
                role = client.get_guild(776912251944435723).get_role(868012504914206720)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="👦"):
                role = client.get_guild(776912251944435723).get_role(868012504050196481)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🧑"):
                role = client.get_guild(776912251944435723).get_role(868012503332974602)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="👨"):
                role = client.get_guild(776912251944435723).get_role(869140063076905010)
                await user.remove_roles(role)
        if reaction.message_id == 870664149275934771:
            if reaction.emoji == discord.PartialEmoji(name="🚹"):
                role = client.get_guild(776912251944435723).get_role(868012505870524416)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🚺"):
                role = client.get_guild(776912251944435723).get_role(868012506675818526)
                await user.remove_roles(role)
        if reaction.message_id == 870664196696731678:
            if reaction.emoji == discord.PartialEmoji(name="💛"):
                role = client.get_guild(776912251944435723).get_role(869141232281079808)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💜"):
                role = client.get_guild(776912251944435723).get_role(869141295468249148)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💙"):
                role = client.get_guild(776912251944435723).get_role(869141424279547914)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="❤️"):
                role = client.get_guild(776912251944435723).get_role(869141342641598484)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🧡"):
                role = client.get_guild(776912251944435723).get_role(869141668488687647)
                await user.remove_roles(role)
        if reaction.message_id == 870664268066983936:
            if reaction.emoji == discord.PartialEmoji(name="🍑"):
                role = client.get_guild(776912251944435723).get_role(869141928762028053)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🍋"):
                role = client.get_guild(776912251944435723).get_role(869141974798725160)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🥙"):
                role = client.get_guild(776912251944435723).get_role(869141809362796554)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🍟"):
                role = client.get_guild(776912251944435723).get_role(869141765498740737)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="🖥"):
                role = client.get_guild(776912251944435723).get_role(869142038766026752)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="📱"):
                role = client.get_guild(776912251944435723).get_role(869142088866988062)
                await user.remove_roles(role)
        if reaction.message_id == 870664298467315712:
            if reaction.emoji == discord.PartialEmoji(name="❤️"):
                role = client.get_guild(776912251944435723).get_role(870657460803866646)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💜"):
                role = client.get_guild(776912251944435723).get_role(870659688021262346)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💛"):
                role = client.get_guild(776912251944435723).get_role(869707827734790154)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💚"):
                role = client.get_guild(776912251944435723).get_role(870649082333507644)
                await user.remove_roles(role)
            if reaction.emoji == discord.PartialEmoji(name="💙"):
                role = client.get_guild(776912251944435723).get_role(870659091809304606)
                await user.remove_roles(role)
### Reaction Roles Ende


@client.event
async def on_member_update(before, after):
    amin = client.get_guild(776912251944435723).get_member(753009216767393842)
    #granit = client.get_guild(776912251944435723).get_member(687060609396899860)
    #yasmin = client.get_guild(776912251944435723).get_member(875123461062815795)
    luca = client.get_guild(776912251944435723).get_member(515602740500627477)
    #kj = client.get_guild(776912251944435723).get_member(796503415021633586)

    names = [amin.display_name, luca.display_name, amin.name, luca.name]
    if len(before.roles) < len(after.roles):
        sicherheitsrole = client.get_guild(776912251944435723).get_role(868050031264010281)
        role = client.get_guild(776912251944435723).get_role(868012490871697448)
        if sicherheitsrole in after.roles:
            await after.remove_roles(role)
    if 'gg/' in str(after.nick) or str(after.nick) in names:
        user = client.get_guild(776912251944435723).get_member(after.id)
        if not user.guild_permissions.administrator:
            channel = client.get_channel(868012618214944788)
            await after.edit(nick='moderated nickname')
            await channel.send(f'{after.mention} Bitte ändere dein Nickname!')
    if 'gg/jobcenter' in str(after.activity):
        if before.status == after.status:
            if before.activity != after.activity:
                if not 'gg/jobcenter' in str(before.activity):
                    logchannel = client.get_channel(884507838645428224)
                    channel = client.get_channel(843888350409654312)
                    promorole = client.get_guild(776912251944435723).get_role(868012507514691594)
                    #await channel.send(f'**{after.mention} vielen Dank dass du unseren Server in deinem Status promotest!**', delete_after=30)
                    embed = discord.Embed(description=f'**{after.name}#{after.discriminator}** hat den Serverlink zum Status hinzugefügt.', color=discord.Colour.green())
                    embed.set_author(name=after.name + '#' + after.discriminator, icon_url=after.avatar_url)
                    embed.set_footer(text=client.user.name + ' - Logs', icon_url=client.user.avatar_url)
                    #await logchannel.send(embed=embed)
                    if client.get_guild(776912251944435723).get_role(868012376946004059) not in after.roles:
                        await after.add_roles(promorole, reason='Jobcenter Invite zum Status hinzugefügt!')
        if not 'gg/jobcenter' in str(after.activity):
            if before.activity != after.activity:
                if 'gg/jobcenter' in str(before.activity):
                    logchannel = client.get_channel(884507838645428224)
                    promorole = client.get_guild(776912251944435723).get_role(868012507514691594)
                    embed = discord.Embed(description=f'**{after.name}#{after.discriminator}** hat den Serverlink aus dem Status entfernt.', color=discord.Colour.red())
                    embed.set_author(name=after.name + '#' + after.discriminator, icon_url=after.avatar_url)
                    embed.set_footer(text=client.user.name + ' - Logs', icon_url=client.user.avatar_url)
                    await logchannel.send(embed=embed)
                    await after.remove_roles(promorole, reason='Jobcenter Invite aus dem Status entfernt!')



@client.command(name='release')
async def release(ctx, user: discord.Member, *, reason=None):
    highteamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if highteamrole in ctx.author.roles:
        role = discord.utils.get(ctx.guild.roles, id=868050031264010281)
        role2 = discord.utils.get(ctx.guild.roles, id=868012490871697448)
        await user.remove_roles(role, reason=reason)
        await user.add_roles(role2)
        with open('./JOBCENTER/jc_data.json', 'r') as f:
            data = json.load(f)
        if user.id in data["quarantine"]:
            data["quarantine"].remove(user.id)
            with open('./JOBCENTER/jc_data.json', 'w') as f:
                json.dump(data, f)
        embed = discord.Embed(description=f':unlock: {user.mention} **wurde aus der Quarantäne entlassen!**', color=discord.Colour.green())
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ <@&892100507533979678>", color=0xff0000)
        await ctx.send(embed=embed)

@release.error
async def release_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)
        
@client.command(name='quarantine', aliases=['secure', 'softban'])
async def quarantine(ctx, user: discord.Member, *, reason=None):
    teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
    if teamrole in ctx.author.roles:
        if ctx.author.top_role.position-1 >= user.top_role.position:
            role = discord.utils.get(ctx.guild.roles, id=868050031264010281)
            for allroles in user.roles:
                try:
                    await user.remove_roles(allroles)
                except:
                    pass
            await user.add_roles(role, reason=reason)
            with open('./JOBCENTER/jc_data.json', 'r') as f:
                data = json.load(f)
            if not user.id in data["quarantine"]:
                data["quarantine"].append(user.id)
                with open('./JOBCENTER/jc_data.json', 'w') as f:
                    json.dump(data, f)
            embed = discord.Embed(description=f':lock: {user.mention} **wurde in Quarantäne versetzt!**', color=discord.Colour.green())
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'Diese Rolle ist zu mächtig um sie zu verwalten.\r\nBitte frage ein höheres Teammitglied oder den Owner um Hilfe.', color=0xff0000)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=":x: Tut mir Leid, aber du bist nicht berechtigt, diesen Befehl auszuführen!\r\n"
                                          "\r\n"
                                          "__Fehlende Rolle:__ <@&868012376946004059>", color=0xff0000)
        await ctx.send(embed=embed)

@quarantine.error
async def quarantine_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**Es ist ein Fehler aufgetreten.**', description='**Bitte erwähne einen Nutzer.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.event
async def on_member_remove(member):
    whitelist = [753009216767393842, 687060609396899860, 515602740500627477, 676789996891537422]
    check1 = await client.wait_for('member_remove', timeout=300)
    entry1 = await member.guild.audit_logs(action=discord.AuditLogAction.ban, limit=1).get()
    if entry1.user.id in whitelist:
        return
    if entry1.user == client.user:
        return
    check2 = await client.wait_for('member_remove', timeout=300)
    entry2 = await member.guild.audit_logs(action=discord.AuditLogAction.ban, limit=1).get()
    if entry1.user != entry2.user:
        return
    check3 = await client.wait_for('member_remove', timeout=300)
    entry = await member.guild.audit_logs(action=discord.AuditLogAction.ban, limit=1).get()
    if entry2.user != entry.user:
        return
    removed_roles = []
    for allroles in entry.user.roles:
        try:
            removed_roles.append(allroles.name)
            await entry.user.remove_roles(allroles)
        except:
            pass
    logchannel = client.get_channel(884507838645428224)
    user1 = client.get_user(753009216767393842)
    user2 = client.get_user(515602740500627477)
    securerole = client.get_guild(776912251944435723).get_role(868050031264010281)
    await entry.user.add_roles(securerole, reason='Security System triggered')
    await user1.send(f'Security System triggered. Target: **{entry.user}** - Reason: `3 Bans in a row`. - Action Taken: *User quarantined*.\r\n' + '`-`' + "\n`-` ".join(removed_roles))
    await user2.send(f'Security System triggered. Target: **{entry.user}** - Reason: `3 Bans in a row`. - Action Taken: *User quarantined*.\r\n' + '`-`' + "\n`-` ".join(removed_roles))
    return

@client.event
async def on_guild_channel_delete(channel):
    whitelist = [753009216767393842, 687060609396899860, 515602740500627477, 676789996891537422]
    check1 = await client.wait_for('guild_channel_delete', timeout=300)
    entry1 = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
    if entry1.user.id in whitelist:
        return
    if entry1.user == client.user:
        return
    check2 = await client.wait_for('guild_channel_delete', timeout=300)
    entry2 = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
    if entry1.user != entry2.user:
        return
    check3 = await client.wait_for('guild_channel_delete', timeout=300)
    entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
    if entry2.user != entry.user:
        return
    removed_roles = []
    for allroles in entry.user.roles:
        try:
            removed_roles.append(allroles.name)
            await entry.user.remove_roles(allroles)
        except:
            pass
    logchannel = client.get_channel(884507838645428224)
    chat = client.get_channel(841759712428032040)
    securerole = client.get_guild(776912251944435723).get_role(868050031264010281)
    user1 = client.get_user(753009216767393842)
    user2 = client.get_user(515602740500627477)
    await entry.user.add_roles(securerole, reason='Security System triggered')
    await user1.send(f'Security System triggered. Target: **{entry.user}** - Reason: `3 deleted Channels in a row`. - Action Taken: *User quarantined*.\r\n' + '`-`' + "\n`-` ".join(removed_roles))
    await user2.send(f'Security System triggered. Target: **{entry.user}** - Reason: `3 deleted Channels in a row`. - Action Taken: *User quarantined*.\r\n' + '`-`' + "\n`-` ".join(removed_roles))
    return


@client.event
async def on_member_join(member):
    welcomechannel = client.get_channel(868012597230854194)
    with open('./JOBCENTER/jc_lvl_users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('./JOBCENTER/jc_lvl_users.json', 'w') as f:
        json.dump(users, f)
    with open('./JOBCENTER/jc_data.json', 'r') as f:
        maindata = json.load(f)
    if welcome_enabled == False:
        return
    global botlist
    if member.bot:
        if not member.id in botlist:
            await welcomechannel.send(f'> **Der Bot {member.mention}, ist gerade beigetreten, wurde aber aufgrund der Sicherheitseinstellungen wieder gekickt!**')
            user1 = client.get_user(753009216767393842)
            user2 = client.get_user(515602740500627477)
            securerole = client.get_guild(776912251944435723).get_role(868050031264010281)
            entry = await member.guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1).get()
            await entry.user.add_roles(securerole, reason='Security System triggered')
            await user1.send(f'Security System triggered. Target: **{entry.user}** Reason: `Versuch einen Bot hinzuzufügen` - Action Taken: *Bot kicked*.')
            await user2.send(f'Security System triggered. Target: **{entry.user}** Reason: `Versuch einen Bot hinzuzufügen` - Action Taken: *Bot kicked*.')
            await member.kick()
        else:
            await welcomechannel.send(f'> **Der Bot {member.mention}, ist gerade beigetreten!**')
    else:
        channel = client.get_channel(868012578398437396)
        background = Image.open("./JOBCENTER/BG.png")
        mask = Image.open('./JOBCENTER/mask.png')
        font = ImageFont.truetype("./JOBCENTER/arial.ttf", 20)
        W, H = (500, 280)

        asset = member.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((100,100))
        draw = ImageDraw.Draw(background)
        text = member.name

        circle_image = Image.new('L', (100, 100))
        circle_draw = ImageDraw.Draw(circle_image)
        circle_draw.ellipse((0, 0, 100, 100), fill=255)
        background.paste(pfp, (200,50), circle_image)

        w, h = draw.textsize(text)
        draw.text(((W-w)/2 - 15,(H-h)/2 + 25), text, (215, 0, 0), font=font)
        background.save("./JOBCENTER/welcome.png")

        teamrole = client.get_guild(776912251944435723).get_role(868012376946004059)
        torrole = client.get_guild(776912251944435723).get_role(834530876431269978)
        sicherheitsrole = client.get_guild(776912251944435723).get_role(868050031264010281)
        allowedtime = datetime.now() - timedelta(days=14)
        #buchstaben =  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 'd', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
        with open("./JOBCENTER/jc_blacklist.json") as f:
            blacklist = json.load(f)
        for bad_word in blacklist["words"]:
            if bad_word in member.name.lower() or "gg/" in member.name.lower():
                await member.add_roles(sicherheitsrole)
                embed = discord.Embed(title=":warning: **Verdächtiges Konto erkannt!** :warning:", description=f"Der Nutzer **{member}** mit der ID **{member.id}** wurde in Quarantäne versetzt.", color=0xff0000)
                embed.add_field(name="User", value=member.mention + " : " + str(member.id))
                embed.add_field(name="Betreten am:", value=member.joined_at, inline=False)
                embed.add_field(name="Erstellt am:", value=member.created_at, inline=False)
                embed.add_field(name="Der Account hat einen __anstößigen Namen__.", value=member.name)
                if member.created_at > allowedtime:
                    embed.add_field(name="Der Account ist __zu jung__.", value="Mind. 14 Tage erforderlich.", inline=False)
                #if member.avatar == discord.DefaultAvatar:
                #    embed.add_field(name="<:JC_discord:846696944344629248> Der Account besitzt __keinen Avatar__.", value="\u200b", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text="Zum freigeben: ,release <User> <reason>")
                await channel.send(teamrole.mention, embed=embed)
                return
        if member.created_at > allowedtime:
            await member.add_roles(sicherheitsrole)
            embed = discord.Embed(title=":warning: **Verdächtiges Konto erkannt!** :warning:", description=f"Der Nutzer **{member}** mit der ID **{member.id}** wurde in Quarantäne versetzt.", color=0xff0000)
            embed.add_field(name="User", value=member.mention + " : " + str(member.id))
            embed.add_field(name="Betreten am:", value=member.joined_at, inline=False)
            embed.add_field(name="Erstellt am:", value=member.created_at, inline=False)
            embed.add_field(name="Der Account ist __zu jung__.", value="Mind. 14 Tage erforderlich.", inline=False)
            #if member.avatar == discord.DefaultAvatar:
            #    embed.add_field(name="Der Account besitzt __keinen Avatar__.", value="\u200b", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="Zum freigeben: ,release <User> <reason>")
            await channel.send(teamrole.mention, embed=embed)
        elif member.avatar == discord.DefaultAvatar:
            await member.add_roles(sicherheitsrole)
            embed = discord.Embed(title=":warning: **Verdächtiges Konto erkannt!** :warning:", description=f"Der Nutzer **{member}** mit der ID **{member.id}** wurde in Quarantäne versetzt.", color=0xff0000)
            embed.add_field(name="ID", value=str(member.id))
            embed.add_field(name="User", value=member.mention + " : " + str(member.id))
            embed.add_field(name="Betreten am:", value=member.joined_at, inline=False)
            embed.add_field(name="Erstellt am:", value=member.created_at, inline=False)
            embed.add_field(name="<:JC_discord:846696944344629248> Der Account besitzt __keinen Avatar__.", value="\u200b", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="Zum freigeben: ,release <User> <reason>")
            await channel.send(teamrole.mention, embed=embed)
        else:
            if member.id in maindata["quarantine"]:
                await member.add_roles(sicherheitsrole)
                embed = discord.Embed(title=":warning: **Verdächtiges Konto erkannt!** :warning:", description=f"Der Nutzer **{member}** mit der ID **{member.id}** wurde in Quarantäne versetzt.", color=0xff0000)
                embed.add_field(name="User", value=member.mention + " : " + str(member.id))
                embed.add_field(name="Betreten am:", value=member.joined_at, inline=False)
                embed.add_field(name="Erstellt am:", value=member.created_at, inline=False)
                embed.add_field(name="Rejoin versuch erkannt", value="Der Nutzer war vor dem Leave in der Sicherheitskontrolle.", inline=False)
                if member.created_at > allowedtime:
                    embed.add_field(name="Der Account ist __zu jung__.", value="Mind. 14 Tage erforderlich.", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text="Zum freigeben: ,release <User> <reason>")
                await channel.send(teamrole.mention, embed=embed)
            else:
                if member.id in maindata["muted"]:
                    muterole = client.get_guild(776912251944435723).get_role(868012378955075614)
                    await member.add_role(muterole)
                chat = client.get_channel(868012618214944788)
                await chat.send(f"Eywaaaa {member.mention} du suchst Arbeit? Willkommen auf JOBCENTER! <a:JC_Sharingan:830837654782214164>")
                await welcomechannel.send(file=discord.File("./JOBCENTER/welcome.png"))
                await welcomechannel.send(f'> **Hey {member.mention}, willkommen auf JOBCENTER.**\r\n'
                                           '> \r\n'
                                           '> **Wir hoffen du findest den richtigen Job :white_check_mark:**\r\n'
                                           '> \r\n'
                                           '> **Bitte lest euch das <#811645544790229082> durch und bei weiteren Fragen zieh ein Ticket in <#868012589207158785> :wink:**\r\n')

#### ECONOMY SYSTEM - BEGINN!!

cmoney = 0
bmoney = 0
tmoney = bmoney + cmoney
#
@client.command(name='bal', aliases=['balance', 'money'])
async def balance(ctx, user: discord.User=None):
    if user == None:
        user = ctx.author
    embed = discord.Embed(timestamp=datetime.now(timezone.utc), color=0xE31316)
    embed.set_author(name=user, icon_url=user.avatar_url)
    global cmoney
    global bmoney
    global tmoney
    embed.add_field(name='Cash:', value=f'<:JC_Coin:852980654027702292> {str(cmoney)}€')
    embed.add_field(name='Bank:', value=f'<:JC_Coin:852980654027702292> {str(bmoney)}€')
    embed.add_field(name='Total:', value=f'<:JC_Coin:852980654027702292> {str(tmoney)}€')
    await ctx.send(embed=embed)
#
#
#@client.command(name='pay', aliases=['givemoney'])
#async def pay(ctx, user: discord.User=None, ammount=None):
#    if user == None:
#        user = ctx.author
#    if ammount == None:
#        await ctx.send('Bitte gebe eine Mänge an.')
#        return
#    if ammount == 'all':
#        ammount = cmoney
#    embed = discord.Embed(description=f'Du hast {user.mention} **{ammount}€** gezahlt.', timestamp=datetime.now(timezone.utc), color=0xE31316)
#    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
#    await ctx.send(embed=embed)
#
#
#@client.command(name='setmoney')
#async def setmoney(ctx, where=None, user: discord.User=None, ammount: int=None):
#    global cmoney
#    global bmoney
#    global tmoney
#    if user == None:
#        user = ctx.author
#    if where == None:
#        await ctx.send('Bitte gebe einen Endpunkt an. `bank/cash`')
#        return
#    elif where == 'bank':
#        where = 'Bank'
#        bmoney = int(ammount)
#    elif where == 'cash':
#        where = 'Bargeld'
#        cmoney = int(ammount)
#    if ammount == None:
#        await ctx.send('Bitte gebe eine Mänge an.')
#        return
#    embed = discord.Embed(description=f'Du hast {user.mention} {where} Geld auf **{ammount}€** gesetzt.', timestamp=datetime.now(timezone.utc), color=0xE31316)
#    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
#    await ctx.send(embed=embed)


@client.command(name='tictactoe', aliases=['ttt'])
@commands.cooldown(1, 30, type=BucketType.user)
async def tictactoe(ctx, user: discord.Member):
    if fun_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Die Fun und Utility Befehle wurden vom Team vorübergehend deaktiviert!**')
        return
    msg = await ctx.send(f'{ctx.author.mention} lädt {user.mention} zu einem **Tic Tac Toe** Spiel ein.', components=[Button(style=3, label="Accept")])

    players = [ctx.author, user]
    def check(res):
        return res.channel == ctx.channel and res.user in players
    

    try:
        res = await client.wait_for("button_click", check=check, timeout=60.0)
        await res.respond(type=6)
        current = user
        # a = Keiner, b = Author, c = User
        a = ":white_square_button:"
        b = ":x:"
        c = ":o:"
        A1 = a
        A2 = a
        A3 = a
        B1 = a
        B2 = a
        B3 = a
        C1 = a
        C2 = a
        C3 = a
        gameembed = discord.Embed(title='Tic Tac Toe', description=f':x: = {ctx.author.mention}\r\n'
                                                                   f':o: = {user.mention}\r\n\r\n'
                                                                   f'**Bereite dich vor**\r\n'
                                                                   f'*Spiel startet bald...*', color=0xE31316)
        game = await ctx.send(embed=gameembed)
        await asyncio.sleep(3)
        while True:
            if current == ctx.author:
                current = user
            else:
                current = ctx.author
            embed = discord.Embed(title='Tic Tac Toe', description=f':x: = {ctx.author.mention}\r\n'
                                                                   f':o: = {user.mention}\r\n\r\n'
                                                                   f'{str(A1)} ǀ {str(A2)} ǀ {str(A3)}\r\n'
                                                                   f' 𑁋𑁋𑁋𑁋𑁋\r\n'
                                                                   f'{str(B1)} ǀ {str(B2)} ǀ {str(B3)}\r\n'
                                                                   f' 𑁋𑁋𑁋𑁋𑁋\r\n'
                                                                   f'{str(C1)} ǀ {str(C2)} ǀ {str(C3)}', color=0xE31316)
            embed.set_footer(text=str(current.name) + " ist am Zug.")
            await game.edit(embed=embed, components=[[Button(style=2, label="A1"), Button(style=2, label="A2"), Button(style=2, label="A3")],
                                                     [Button(style=2, label="B1"), Button(style=2, label="B2"), Button(style=2, label="B3")],
                                                     [Button(style=2, label="C1"), Button(style=2, label="C2"), Button(style=2, label="C3")]])
            try:
                res = await client.wait_for("button_click", check=check, timeout=30.0)
                if res.user == current:
                    if current == ctx.author:
                        if res.component.label == "A1":
                            A1 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "A2":
                            A2 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "A3":
                            A3 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "B1":
                            B1 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "B2":
                            B2 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "B3":
                            B3 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "C1":
                            C1 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "C2":
                            C2 = b
                            current = user
                            await res.respond(type=6)
                        elif res.component.label == "C3":
                            C3 = b
                            current = user
                            await res.respond(type=6)
                    elif current == user:
                        if res.component.label == "A1":
                            A1 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "A2":
                            A2 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "A3":
                            A3 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "B1":
                            B1 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "B2":
                            B2 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "B3":
                            B3 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "C1":
                            C1 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "C2":
                            C2 = c
                            current = ctx.author
                            await res.respond(type=6)
                        elif res.component.label == "C3":
                            C3 = c
                            current = ctx.author
                            await res.respond(type=6)
            except asyncio.TimeoutError:
                await game.reply('<:JC_xmark:826282095566913537> **Timed out!**')
                await game.edit(components=[[Button(style=2, label="A1", disabled=True), Button(style=2, label="A2", disabled=True), Button(style=2, label="A3", disabled=True)],
                                            [Button(style=2, label="B1", disabled=True), Button(style=2, label="B2", disabled=True), Button(style=2, label="B3", disabled=True)],
                                            [Button(style=2, label="C1", disabled=True), Button(style=2, label="C2", disabled=True), Button(style=2, label="C3", disabled=True)]])
                return
        
    except asyncio.TimeoutError:
        await msg.reply('<:JC_xmark:826282095566913537> **Timed out!**')
        await msg.edit(components=[Button(style=4, label="Timed Out", disabled=True)])


@client.command(name='slot', aliases=['slots', 'slotmaschine'])
async def slot(ctx, bet: int=None):
    if casino_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Das Casinosystem wurde vom Team vorübergehend deaktiviert!**')
        return
    if bet == None:
        bet = 'Just for fun'
    else:
        bet = f'{bet}€'
    symbols = ['🍇', '🍉', '🍒', '💎', '🍐', '🍊']
    if ctx.author.id == 515602740500627477:
        symbols = ['🍇', '🍉', '🍒', '💎', '💎', '💎']
    slot1 = random.choice(symbols)
    slot2 = random.choice(symbols)
    slot3 = random.choice(symbols)
    winning = 1
    if str(slot1) == str(slot2):
        winning += 1
        if str(slot1) == str(slot3):
            winning += 1
            if str(slot1) == '💎':
                winning = 'JACKPOT'
    elif str(slot2) == str(slot3):
        winning += 1
    elif str(slot1) == str(slot3):
        winning += 1
    embed = discord.Embed(description=f'**Bet:** {bet}\r\n\r\n{slot1} | {slot2} | {slot3}\r\n\r\nIn a row: `{str(winning)}`', timestamp=datetime.now(timezone.utc), color=0xE31316)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    msg = await ctx.send(embed=embed, components=[Button(style=1, label="Reroll")])

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await client.wait_for("button_click", check=check, timeout=30)
        await res.respond(type=6)
        times = 1
        while True:
            slot1 = random.choice(symbols)
            slot2 = random.choice(symbols)
            slot3 = random.choice(symbols)
            winning = 1
            if str(slot1) == str(slot2):
                winning += 1
                if str(slot1) == str(slot3):
                    winning += 1
                    if str(slot1) == '💎':
                        winning = 'JACKPOT'
            elif str(slot2) == str(slot3):
                winning += 1
            elif str(slot1) == str(slot3):
                winning += 1
            embed = discord.Embed(description=f'**Bet:** {bet}\r\n\r\n{slot1} | {slot2} | {slot3}\r\n\r\nIn a row: `{str(winning)}`\r\nRerolls: `{str(times)}`', timestamp=datetime.now(timezone.utc), color=0xE31316)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await msg.edit(embed=embed, components=[Button(style=1, label="Reroll")])

            def check(res):
                return ctx.author == res.user and res.channel == ctx.channel

            try:
                res = await client.wait_for("button_click", check=check, timeout=30)
                times += 1
                await res.respond(type=6)
                continue

            except asyncio.TimeoutError:
                await msg.edit(components=[Button(style=1, label="Reroll", disabled=True)])
                break
    except asyncio.TimeoutError:
        await msg.edit(components=[Button(style=1, label="Reroll", disabled=True)])



@client.command(name='blackjack', aliases=['bj'])
async def blackjack(ctx, bet: int=None):
    if casino_enabled == False:
        await ctx.reply('<:JC_xmark:826282095566913537> **Das Casinosystem wurde vom Team vorübergehend deaktiviert!**')
        return
    if bet == None:
        await ctx.reply('<:JC_xmark:826282095566913537> **Bitte gib eine einen Betrag für die Wette an.**')
        return
    else:
        bet = f'{bet}€'
    cardback = "<:KartenRckseite:857630051508158474>"
    CardA = ["<:pikAss:857370425947717633>","<:kreuzAss:857625793672642620>","<:karoAss:857625009269768213>","<:herzAss:857370290342723674>"] #11 Punkte
    CardK = ["<:pikKing:857626643265880074>", "<:herzKing:857370290350718986>", "<:karoKing:857628943753805875>", "<:kreuzKing:857626077224894464>"] #10 Punkte
    CardQ = ["<:pikDame:857626670818918400>","<:karoDame:857628964826251264>","<:herzDame:857370290517835837>", "<:kreuzDame:857626038440034364>"] #10 Punkte
    CardJ = ["<:pikBube:857626670261731341>","<:karoBube:857628639259656242>","<:herzBube:857370290383487006>", "<:KreuzBube:857626038161899521>"] #10 Punkte
    Card9 = ["<:pik9:857370426060701736>", "<:kreuz9:857370777389367318>","<:karo9:857625009257578496>","<:herz9:857370290375753818>"]
    Card8 = ["<:pik8:857370426040909825>","<:kreuz8:857370777863192577>","<:karo8:857625009484464148>","<:herz8:857370290337218591>"]
    Card7 = ["<:pik7:857370425998442517>","<:kreuz7:857370777703415818>","<:karo7:857625009290870874>","<:herz7:857370290078220309>"]
    Card6 = ["<:pik6:857370425814417408>","<:kreuz6:857370777699745894>","<:karo6:857625009282482186>","<:herz6:857370289712267276>"]
    Card5 = ["<:pik5:857370425881001985> ","<:kreuz5:857370777493962782>","<:karo5:857625009190731826> ","<:herz5:857370289993547796>"]
    Card4 = ["<:pik4:857370425495519243>","<:kreuz4:857370777514803210> ","<:karo4:857625008553721896> ","<:herz4:857370289720918037>"]
    Card3 = ["<:pik3:857370425775095848>","<:kreuz3:857370777417940992>","<:karo3:857625008473767996>"]
    Card2 = ["<:herz2:857370288974987294>"]
    randomcard = [random.choice(CardA), random.choice(CardK), random.choice(CardQ), random.choice(CardJ), random.choice(Card9), random.choice(Card8), random.choice(Card7), random.choice(Card6), random.choice(Card5), random.choice(Card4), random.choice(Card3), random.choice(Card2),]
    selfvalue = 0
    dealervalue = 0
    embed = discord.Embed(description=f'**Bet:** {bet}\r\n\r\n'
                                       '`hit` - eine weitere Karte nehmen\r\n'
                                       '`stand` - Spiel beenden\r\n'
                                       '`double down` - verdoppeln, neue Karte, dann stand', color=0xE31316)
    embed.add_field(name='Deine Hand:', value=f'{random.choice(randomcard)} {random.choice(randomcard)}\r\nValue: `{selfvalue}`')
    embed.add_field(name='Dealer Hand:', value=f'{random.choice(randomcard)} {cardback}\r\nValue: `{dealervalue}`')
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    msg = await ctx.send(embed=embed, components=[[Button(style=1, label="Hit"), Button(style=3, label="Stand"), Button(style=2, label="Double Down"), Button(style=2, label="Split", disabled=True)]])
    
    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await client.wait_for("button_click", check=check, timeout=30)
        await res.respond(type=6)
    
    except asyncio.TimeoutError:
        await msg.edit(components=[[Button(style=1, label="Hit", disabled=True), Button(style=3, label="Stand", disabled=True), Button(style=2, label="Double Down", disabled=True), Button(style=2, label="Split", disabled=True)]])

#### ECONOMY SYSTEM ENDE!!        
        

#### MUSIK SYSTEM BEGINN!!
  
music = DiscordUtils.Music()

@client.command()
async def join(ctx):
    voicec = ctx.author.voice
    if voicec:
        channel = voicec.channel
        if channel:
            if not ctx.voice_client:
                await ctx.message.add_reaction('a:JC_Timer:830745906327453696')
                embed = discord.Embed(title='Joined', description=f'Ich bin dem Kanal {channel.mention} beigetreten!', colour=0xE31316)
                embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
                await channel.connect()  # Joins author's voice channel
                await ctx.message.clear_reactions()
                await ctx.reply(embed=embed)
    
@client.command()
async def leave(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    await ctx.voice_client.disconnect()
    await ctx.message.add_reaction('👋')

@client.command()
@commands.guild_only()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not ctx.voice_client:
        voicec = ctx.author.voice
        if voicec:
            channel = voicec.channel
            if channel:
                await channel.connect()
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        if not ctx.voice_client.channel == ctx.author.voice.channel:
            return
        await ctx.message.add_reaction('a:JC_Timer:830745906327453696')
        await player.queue(url, search=True)
        song = await player.play()
        embed = discord.Embed(title='Playing',
                              description=f'Es folgt **{song.name}**...',
                              colour=0xE31316)
        embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
        await ctx.message.clear_reactions()
        await ctx.reply(embed=embed)
    else:
        if not ctx.voice_client.channel == ctx.author.voice.channel:
            return
        song = await player.queue(url, search=True)
        embed = discord.Embed(title='Queued',
                              description=f"**{song.name}** zur Warteschlange hinzugefügt.", colour=0xE31316)
        await ctx.reply(embed=embed)

@client.command()
async def pause(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    embed = discord.Embed(title='Paused',
                          description=f'**{song.name}** wurde pausert.',
                          colour=0xE31316)
    embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)

@client.command()
async def resume(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    embed = discord.Embed(title='Resumed',
                          description=f'**{song.name}** wird fortgesetzt', color=0xE31316)
    embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)

@client.command()
async def stop(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    embed = discord.Embed(title='Stopped',
                          description='Die Musikwiedergabe wurde beendet.',
                          colour=0xE31316)
    embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)

@client.command()
async def loop(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        embed = discord.Embed(title='Loop aktiviert',
                              description=f'**{song.name}** wird ab jetzt wiederholt.',
                              color=0xE31316)
        embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Loop deaktiviert',
                              description=f'**{song.name}** wird nicht mehr wiederholt.',
                              colour=0xE31316)
        embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
        await ctx.reply(embed=embed)

@client.command()
async def queue(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    diequeue = player.current_queue()
    list = []
    for item in diequeue:
        list.append(item.name)
        dielist = '\n'.join(list)
        embed = discord.Embed(title='Warteschlange',
                              description=f'**{dielist}**',
                              colour=0xE31316)
        embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)
    #await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

@client.command()
async def np(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    embed = discord.Embed(title='Now Playing',
                          description=f'Aktuell Spielt: **{song.name}**',
                          colour=0xE31316)
    embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)

@client.command()
async def skip(ctx):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        embed = discord.Embed(title='Skipping',
                              description=f"**{data[0].name}** wurde übersprungen.",
                              colour=0xE31316)
        embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title='Skipped',
                              description=f'Überspringe **{data[0].name}**', colour=0xE31316)
        embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
        await ctx.reply(embed=embed)

@client.command(name='v')
async def volume(ctx, vol):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(int(vol) / 100)  # volume should be a float between 0 to 1
    embed = discord.Embed(title='Lautstärke', description=f"Lautstärke von **{song.name}** auf **{volume * 100}%** geändert.",
                          colour=0xE31316)
    embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)

@client.command()
async def removesong(ctx, index):
    if not ctx.voice_client.channel == ctx.author.voice.channel:
        return
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    embed = discord.Embed(title='Aus Warteschlange entfernt',
                          description=f"Removed **{song.name}** from queue",
                          colour=0xE31316)
    embed.set_footer(text=f'von {ctx.author} \u200b', icon_url=f'{ctx.author.avatar_url}')
    await ctx.reply(embed=embed)

client.run(TOKEN)
