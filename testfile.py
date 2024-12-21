import discord
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import random
import os
from discord.utils import get

client = commands.Bot(command_prefix=">>", intents=discord.Intents.all())


@client.event
async def on_ready():
    global Garam
    await client.wait_until_ready()
    game = discord.Game("즐거운 오버워치")
    print("login: Garam Main")
    print(client.user.name)
    print(client.user.id)
    print("---------------")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel

    print('{} / {}: {}'.format(channel, author, content))

    if message.content.startswith(">>"):
        content = message.content
        content = content.split(">>")
        content = content[1]

        if content == '':
            return

        if content == "명령어":
            embed = discord.Embed(title="명령어 모음", description="가람봇 문의사항은 DITTO#31435에게 전달해주세요", color=12745742)
            embed.add_field(name="LINK for Everything", value="문의방, 수다방, 공지방, 네이버카페, 신입안내", inline=False)
            embed.add_field(name="운영진 및 스탭 목록", value="운영진", inline=False)
            embed.add_field(name="Utility", value="로또, 주사위, 맵추천, 공수추천, 팀편성, 한줄소개설문지", inline=False)
            await channel.send(embed=embed)
            return


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
