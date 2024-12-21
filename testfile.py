import discord
from discord.ext import commands
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import random
import os
from discord.utils import get

client = commands.Bot(command_prefix=">>", intents=discord.Intents.all())

current_time = lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=9)


def is_moderator(member):
    return "운영진" in map(lambda x: x.name, member.roles)


def is_dcstaff(member):
    return "스텝-DC" in map(lambda x: x.name, member.roles)


@client.event
async def on_ready():
    global Garam
    await client.wait_until_ready()
    game = discord.Game("즐거운 발로란트")
    print("login: MYJW Main")
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

        if content == "팀편성":
            await message.channel.send(
                "@here 팀편성 해주세요!\n" + "https://tenor.com/view/thinking-think-tap-tapping-spongebob-gif-5837190")
            return

        if content == "봇":
            embed = discord.Embed(title=":robot:MYJW bot:robot:", description="ditto!", color=3066993)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/708306592465944591/723914634116988988/3b53af51b6da75d2.png")
            await channel.send(embed=embed)
            return

        if content == "명령어":
            embed = discord.Embed(title="명령어 모음", description="봇 문의사항은 박디도에게 전달해주세요", color=12745742)
            embed.add_field(name="LINK for Everything", value="카톡방, 회칙", inline=False)
            embed.add_field(name="운영진 및 스탭 목록", value="운영진", inline=False)
            embed.add_field(name="Utility", value="로또, 주사위, 맵추천, 공수추천, 팀편성", inline=False)
            await channel.send(embed=embed)
            return

        if content == "운영진":
            staff_list = ':pen_ballpoint: 모토aka뷔\n:construction_worker: 박디도\n:construction_worker: NEXT\n:construction_worker: NEXT\n:construction_worker: NEXT'
            embed = discord.Embed(title="운영진 리스트입니다. 인게임 친구추가 부탁드려요", description=staff_list, color=3447003)
            await channel.send(embed=embed)
            return

        #if content == "건의및신고":
         #   embed = discord.Embed(title="건의및신고", description="https://discord.com/channels/1318944505977770005/1319700286893195326",
         #                        color=0xE86222)
         #   await channel.send(embed=embed)
         #   return

        if content == "카톡방":
            embed = discord.Embed(title="카톡방",
                                  description="https://invite.kakao.com/tc/h17zJMGC30",
                                  color=0xE86222)
            await channel.send(embed=embed)
            return

        #if content == "공지방":
        #    embed = discord.Embed(title="공지방",
        #                          description="https://open.kakao.com/o/gN6wLj4e",
        #                          color=0xE86222)
        #    await channel.send(embed=embed)
        #    return

        #if content == "네이버카페":
        #    await message.channel.send("https://cafe.naver.com/orangec7sck")
        #    return

        if content == "회칙":
            embed = discord.Embed(title="회칙 링크", description="신입클랜원분들은 해당 사항 한 번씩 읽어주세요!!", color=0xFF5733)
            embed.add_field(name="디스코드 안내 링크", value="https://discord.com/channels/1318944505977770005/1318944505977770008", inline=False)
            await channel.send(embed=embed)
            return

        #if content == "한줄소개설문지":
        #    await message.channel.send("https://forms.gle/We9udWooJ1C9q9S5A")
        #    return

        if content == "주사위":
            dice = "0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 5 5 5 5 5 5 5 6 6 6 6 6 6 777"
            dicechoice = dice.split(" ")
            dicenumber = random.randint(1, len(dicechoice))
            print(len(dicechoice))
            print(dicenumber)
            diceresult = dicechoice[dicenumber - 1]
            await message.channel.send("오늘 당신의 주사위는....!  **||   " + diceresult + "   ||**!!!!")
            return

        if content == "로또":
            lotteryNumbers = []

            for i in range(0, 6):
                number = random.randint(1, 45)
                while number in lotteryNumbers:
                    number = random.randint(1, 45)
                lotteryNumbers.append(number)

            lotteryNumbers.sort()
            lotto = ' '.join(map(str, lotteryNumbers))
            await message.channel.send("Good luck!\n" + lotto)
            return

        if content == "맵추천":
            maps = "선셋 로터스 펄 프랙처 브리즈 아이스박스 바인드 헤이븐 스플릿 어센트"
            mapchoice = maps.split(" ")
            mapnumber = random.randint(1, len(mapchoice))
            mapresult = mapchoice[mapnumber - 1]
            await message.channel.send("디도가 추천드리는 오늘의 맵은....!  **||" + mapresult + "||**")
            return

        if content == "공수추천":
            choices = "공격이 수비가"
            choice = choices.split(" ")
            number = random.randint(1, len(choice))
            result = choice[number - 1]
            await message.channel.send("나는요 " + result + " 좋은거헐! (짝짝) 오또케!")
            return


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
