import discord
import os
import sys
import json
import random
import asyncio
import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
client = discord.Client()
async def CheckLink(m:discord.message, ch:discord.TextChannel, chID:int, guild:dict) -> None:
    ms = m.content.split(" ")
    urls = list()
    a = 0
    if("." in m.content):
        for i in ms:
            if("." in i):
                if(("https://" in i) or ("http://" in i)):  
                    try:
                        res = urlopen(i)
                        urls.append(i)
                        a = a + 1
                    except:
                        urls.append("None")
                        a = a + 1
                else:
                    try:
                        res = urlopen("https://" + i)
                        urls.append(i)
                        a = a + 1
                    except:
                        urls.append("None")
                        a = a + 1
    while "None" in urls:
        urls.remove("None")
    if(not len(urls) == 0):
        rule = 0
        desc = ""
        for i in guild["rules"]:
            if(i["Type"] == "NoLink"):
                break
            rule = rule + 1
        desc = guild["rules"][rule]["Description"]
        await ch.send(f"{m.author.mention} 규칙 {rule+1} 을 위반하셨습니다.\n```{desc}```")
        await ch.guild.get_channel(guild["managech"]).send(embed=discord.Embed(title = "규칙 위반 알림", description = f"{m.author.mention} 님이 {m.channel.mention} 에서 {rule+1}번째 규칙을 위반하셨습니다.\n[메세지로 이동하기](https://discord.com/channels/{m.channel.guild.id}/{m.channel.id}/{m.id})\n\n메세지 내용```{m.content}```", color = randomColor()))

async def CheckInvite(m:discord.message, ch:discord.TextChannel, chID:int, guild:dict) -> None:
    if("discord.gg/" in m.content):
        rule = 0
        desc = ""
        for i in guild["rules"]:
            if(i["Type"] == "NoInvite"):
                break
            rule = rule + 1
        desc = guild["rules"][rule]["Description"]
        if(guild["rules"][rule]["Way"] == "delete"):
            await m.delete()
        await ch.send(f"{m.author.mention} 규칙 {rule+1} 을 위반하셨습니다.\n```{desc}```")
        await ch.guild.get_channel(guild["managech"]).send(embed=discord.Embed(title = "규칙 위반 알림", description = f"{m.author.mention} 님이 {m.channel.mention} 에서 {rule+1}번째 규칙을 위반하셨습니다.\n[메세지로 이동하기](https://discord.com/channels/{m.channel.guild.id}/{m.channel.id}/{m.id})\n\n메세지 내용```{m.content}```", color = randomColor()))

def randomColor() -> int:
    return random.randint(0, 16777215)
@client.event
async def on_ready() -> None:
    print("log in")
@client.event
async def on_message(msg):
    if(msg.author.bot):
        return
    send = msg.channel.send
    embed = discord.Embed
    if(msg.author.id == 418023987864403968 and msg.content == "*restart"):
        await send(embed = embed(title="Checker Module Restart", color = randomColor()))
        os.system("cls")
        os.system("python check.py")
        sys.exit()
    with open(f"data/guilds/{msg.guild.id}/info.json", "r", encoding='UTF-8') as fp:
        guild:dict = json.loads(fp.read())
    for i in guild["rules"]:
        if(i["Type"] == "NoLink"):
            await CheckLink(msg, msg.channel, guild["managech"], guild)
        if(i["Type"] == "NoInvite"):
            await CheckInvite(msg, msg.channel, guild["managech"], guild)

client.run(os.environ["TOKEN"])