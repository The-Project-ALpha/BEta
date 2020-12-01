import discord
import os
import sys

client = discord.Client()

@client.event
async def on_ready():
    print("log in")

@client.event
async def on_message(msg):
    if(msg.author.id == 418023987864403968 and msg.content == "*restart"):
        print("Restart...")
        os.system("python main.py")
        sys.exit()
client.run('TOKEN')