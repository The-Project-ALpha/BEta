import discord
import os
import sys
import json
import random

with open("data/info.json", "r") as fp:
    j = fp.read()
data = json.loads(j)
intents = discord.Intents.all()
client = discord.Client(intents = intents)
def randomColor() -> int:
    return random.randint(0, 16777215)

@client.event
async def on_ready() -> None:
    print("log in")

@client.event
async def on_message(msg:discord.Message) -> None:
    if(not msg.content.startswith("*")):
        return
    c:str = msg.content
    send = msg.channel.send
    embed = discord.Embed
    if(c == "*info"):
        await send(embed = embed(title="Info", description = f"""
Discord.py Version - {discord.__version__}
BEta Bot Version - {data["VERSION"]}


""", color = randomColor()))


    if(msg.author.id == 418023987864403968 and msg.content == "*restart"):
        await send(embed = embed(title="Restart", color = randomColor()))
        os.system("python main.py")
        sys.exit()
    
@client.event
async def on_guild_join(guild:discord.Guild):
    embed = discord.Embed(title = "👋안녕하세요!", description = f"BEta 봇을 {guild.name} 서버에 추가해주셔서 감사합니다.\n`*help` 명령어로 사용법을 확인 가능하니 참고해주세요!", color = randomColor())    
    embed.set_author(name = "Project ALpha.", url = "https://discord.gg/JGd5R6D5ep", icon_url = "https://cdn.discordapp.com/avatars/783157437745725451/5da3bbdcb4e0574374040420e8ac519c.png?size=128")
    await guild.owner.send(embed=embed)


client.run(data["TOKEN"])