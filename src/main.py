import discord
import os
import sys
import json
import random
import asyncio
import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

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
    while True:
        await client.change_presence(activity=discord.Game(name = f"{len(client.guilds)} guilds, {len(client.users)} users", status=discord.Status.do_not_disturb))
        await asyncio.sleep(10)

@client.event
async def on_message(msg:discord.Message) -> None:
    if(msg.author.bot):
        return

    if(not msg.content.startswith("*")):
        return
    c:str = msg.content
    cs = c.split(" ")
    send = msg.channel.send
    embed = discord.Embed
    if(c == "*info"):
        await send(embed = embed(title="Info", description = f"""
Discord.py Version - {discord.__version__}
BEta Bot Version - {data["VERSION"]}
""", color = randomColor()))
        return
    if(cs[0] == "*rule"):
        def check(message):
            return message.author == msg.author
        if(not os.path.isfile(f"data/guilds/{msg.guild.id}/info.json")):
            os.makedirs(f"data/guilds/{msg.guild.id}")
            os.makedirs(f"data/guilds/{msg.guild.id}/users")
            with open(f"data/guilds/{msg.guild.id}/info.json", "w", encoding='UTF-8') as fp:
                d:dict = {"rules" : list(), "managech" : msg.channel.id}
                json.dump(d, fp, ensure_ascii=False)
        if(cs[1] == "list"):
            with open(f"data/guilds/{msg.guild.id}/info.json", "r", encoding='UTF-8') as fp:
                guild = json.loads(fp.read())
            r = guild["rules"]
            s = "```규칙이 없습니다.```"
            if(not len(r) == 0):
                s = "```"
                l = 1
                for i in r:
                    s = s + f"Rule {l} : " + i["Description"] + f"\nType : {i['Type']}\n처벌 : {i['Way']}\n\n"
                    l = l + 1
                s = s + "```"   
            await send(embed=embed(title="이 서버의 규칙", description = s, color = randomColor()))
        if(cs[1] == "add"):
            perm:discord.Permissions = msg.author.guild_permissions
            if(not perm.administrator):
                await send(embed=embed(title="규칙을 수정할 권한이 없습니다.", color = 0xff0000))
                return
            with open(f"data/guilds/{msg.guild.id}/info.json", "r", encoding='UTF-8') as fp:
                guild = json.loads(fp.read())
            d:dict = {}
            await send(embed=embed(title="규칙의 타입을 입력해 주세요.", description = "Type```NoLink : 링크 포스트 금지\nNoInvite : 서버 초대링크 포스트 금지```", color = randomColor()))
            try:
                m = await client.wait_for("message", timeout = 20.0, check=check)
                d["Type"] = m.content
            except asyncio.TimeoutError:
                await send(embed=embed(title="일정 시간동안 메세지를 입력하지 않아 취소되었습니다.", color = 0xff0000))
                return
            await send(embed=embed(title="규칙의 설명을 입력해 주세요.", color = randomColor()))
            try:
                m = await client.wait_for("message", timeout = 20.0, check=check)
                d["Description"] = m.content
            except asyncio.TimeoutError:
                await send(embed=embed(title="일정 시간동안 메세지를 입력하지 않아 취소되었습니다.", color = 0xff0000))
                return
            await send(embed=embed(title="규칙을 지키지 않을시의 처벌을 입력해 주세요.", description = "Type```delete : 메세지 삭제\nkick : 추방\nwarn : 경고 메세지\nban : 밴때리기```", color = randomColor()))
            try:
                m = await client.wait_for("message", timeout = 20.0, check=check)
                d["Way"] = m.content
            except asyncio.TimeoutError:
                await send(embed=embed(title="일정 시간동안 메세지를 입력하지 않아 취소되었습니다.", color = 0xff0000))
                return
            guild["rules"].append(d)
            with open(f"data/guilds/{msg.guild.id}/info.json", "w", encoding='UTF-8') as fp:
                json.dump(guild, fp, ensure_ascii=False)
            await send(embed=embed(title="성공적으로 규칙을 추가했습니다.", description = f"규칙의 타입 ```{d['Type']}```\n규칙의 설명 ```{d['Description']}```", color = randomColor()))
        if(cs[1] == "remove"):
            perm:discord.Permissions = msg.author.guild_permissions
            if(not perm.administrator):
                await send(embed=embed(title="규칙을 수정할 권한이 없습니다.", color = 0xff0000))
                return
            with open(f"data/guilds/{msg.guild.id}/info.json", "r", encoding='UTF-8') as fp:
                guild = json.loads(fp.read())
            r = guild["rules"]
            s = "```규칙이 없습니다.```"
            if(not len(r) == 0):
                s = "```"
                l = 1
                for i in r:
                    s = s + f"Rule {l} : " + i["Description"] + f"\nType : {i['Type']}\n처벌 : {i['Way']}\n\n"
                    l = l + 1
                s = s + "```"
            await send(embed=embed(title="이 서버의 규칙", description = s, color = randomColor()))
            await send(embed=embed(title="삭제할 규칙의 번호를 입력해주세요.", color = randomColor()))
            try:
                m = await client.wait_for("message", timeout = 20.0, check=check)
            except asyncio.TimeoutError:
                await send(embed=embed(title="일정 시간동안 메세지를 입력하지 않아 취소되었습니다.", color = 0xff0000))
                return
            del guild["rules"][int(m.content) - 1]
            with open(f"data/guilds/{msg.guild.id}/info.json", "w", encoding='UTF-8') as fp:
                json.dump(guild, fp, ensure_ascii=False)
            await send(embed=embed(title="성공적으로 규칙을 삭제했습니다.", color = randomColor()))
            with open(f"data/guilds/{msg.guild.id}/info.json", "r", encoding='UTF-8') as fp:
                guild = json.loads(fp.read())
            r = guild["rules"]
            s = "```규칙이 없습니다.```"
            if(not len(r) == 0):
                s = "```"
                l = 1
                for i in r:
                    s = s + f"Rule {l} : " + i["Description"] + f"\nType : {i['Type']}\n처벌 : {i['Way']}\n\n"
                    l = l + 1
                s = s + "```"   
            await send(embed=embed(title="이 서버의 규칙", description = s, color = randomColor()))
    if(msg.author.id == 418023987864403968 and msg.content == "*restart"):
        await send(embed = embed(title="Main Program Restart", color = randomColor()))
        os.system("cls")
        os.system("python main.py")
        sys.exit()
    if(cs[0] == "*set"):
        if(cs[1] == "channel"):
            perm:discord.Permissions = msg.author.guild_permissions
            if(not perm.administrator):
                await send(embed=embed(title="관리자 채널을 수정할 권한이 없습니다.", color = 0xff0000))
                return
            chid = int(re.findall(r"\d+", cs[2])[0])
            with open(f"data/guilds/{msg.guild.id}/info.json", "r", encoding='UTF-8') as fp:
                guild = json.loads(fp.read())
            guild["managech"] = chid
            with open(f"data/guilds/{msg.guild.id}/info.json", "w", encoding='UTF-8') as fp:
                json.dump(guild, fp, ensure_ascii=False)
            await send(embed=embed(title = "변경 성공", description = f"관리자 채널을 <#{chid}> 채널로 변경했습니다.", color = randomColor()))
    

    
    

    





@client.event
async def on_guild_join(guild:discord.Guild):
    embed = discord.Embed(title = "👋안녕하세요!", description = f"BEta 봇을 `{guild.name}` 서버에 추가해주셔서 감사합니다.\n`*help` 명령어로 사용법을 확인 가능하니 참고해주세요!", color = randomColor())    
    embed.set_author(name = "Project ALpha.", url = "https://discord.gg/JGd5R6D5ep", icon_url = "https://cdn.discordapp.com/avatars/783157437745725451/5da3bbdcb4e0574374040420e8ac519c.png?size=128")
    await guild.owner.send(embed=embed)
client.run(os.environ["TOKEN"])