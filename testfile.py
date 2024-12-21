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

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

url = "https://docs.google.com/spreadsheets/d/1G288YQemotpgNzet_HchHUaa8m7md1YSH38wldmCi0k/edit#gid=0"

current_time = lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=9)


def is_moderator(member):
    return "운영진" in map(lambda x: x.name, member.roles)


def is_dcstaff(member):
    return "스텝-DC" in map(lambda x: x.name, member.roles)


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

async def get_spreadsheet(ws_name):
    creds = ServiceAccountCredentials.from_json_keyfile_name("garam-382904-9603060e0307.json", scope)
    auth = gspread.authorize(creds)

    if creds.access_token_expired:
        auth.login()

    try:
        worksheet = auth.open_by_url(url).worksheet(ws_name)
    except gspread.exceptions.APIError:
        print("API Error")
        return
    return worksheet

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

        if content == "가람봇":
            embed = discord.Embed(title=":robot:가람봇:robot:", description="가람봇 ver1.0 온라인!", color=3066993)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/708306592465944591/723914634116988988/3b53af51b6da75d2.png")
            await channel.send(embed=embed)
            return


        if content == "한줄소개":
            spreadsheet = await get_spreadsheet('responses1')
            data = spreadsheet.col_values(3)
            data[0] = "한줄소개 명령어 리스트입니다!"
            await channel.send(data)
            return

        if content == "명령어":
            embed = discord.Embed(title="명령어 모음", description="가람봇 문의사항은 DITTO#31435에게 전달해주세요", color=12745742)
            embed.add_field(name="LINK for Everything", value="문의방, 수다방, 공지방, 네이버카페, 신입안내", inline=False)
            embed.add_field(name="운영진 및 스탭 목록", value="운영진", inline=False)
            embed.add_field(name="Utility", value="로또, 주사위, 맵추천, 공수추천, 팀편성, 한줄소개설문지", inline=False)
            await channel.send(embed=embed)
            return

        if content == "운영진":
            staff_list = ':pen_ballpoint: 가람#31413\n:construction_worker: 라루이라#3280\n:construction_worker: DITTO#31435\n:construction_worker: 황근출#3391\n:construction_worker: 비상#3132'
            embed = discord.Embed(title="운영진 리스트입니다. 친구추가 부탁드려요", description=staff_list, color=3447003)
            await channel.send(embed=embed)
            return

        if content == "문의방":
            embed = discord.Embed(title="문의방", description="총 인원 6명일 때 입장가능합니다. 7명 이상이면 대기! \n https://open.kakao.com/o/gOlu408e",
                                  color=0xE86222)
            await channel.send(embed=embed)
            return

        if content == "수다방":
            embed = discord.Embed(title="수다방",
                                  description="https://open.kakao.com/o/gQ2qa42e",
                                  color=0xE86222)
            await channel.send(embed=embed)
            return

        if content == "공지방":
            embed = discord.Embed(title="공지방",
                                  description="https://open.kakao.com/o/gN6wLj4e",
                                  color=0xE86222)
            await channel.send(embed=embed)
            return

        if content == "네이버카페":
            await message.channel.send("https://cafe.naver.com/orangec7sck")
            return

        if content == "신입안내":
            embed = discord.Embed(title="신입클랜원 안내 링크", description="신입클랜원분들은 해당 사항 한 번씩 읽어주세요!!", color=0xFF5733)
            embed.add_field(name="디스코드 안내 링크", value="https://cafe.naver.com/orangec7sck", inline=False)
            embed.add_field(name="가람 신입클랜원 안내 링크", value="https://cafe.naver.com/orangec7sck", inline=False)
            await channel.send(embed=embed)
            return

        if content == "한줄소개설문지":
            await message.channel.send("https://forms.gle/We9udWooJ1C9q9S5A")
            return

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
            # 파리 호라이즌
            mapchoice = maps.split(" ")
            mapnumber = random.randint(1, len(mapchoice))
            mapresult = mapchoice[mapnumber - 1]
            await message.channel.send("가람봇이 추천드리는 오늘의 맵은....!  **||" + mapresult + "||**")
            return

        if content == "공수추천":
            choices = "공격이 수비가"
            choice = choices.split(" ")
            number = random.randint(1, len(choice))
            result = choice[number - 1]
            await message.channel.send("나는요 " + result + " 좋은거헐! (짝짝) 오또케!")
            return

        spreadsheet = await get_spreadsheet('responses1')
        # 내전 팀편성
        if content.startswith("내전팀편성"):
            team1List = []
            team2List = []

            if len(content.split(" ")) != 13 and len(content.split(" ")) != 15:
                    data = "잘못 입력한 부분이 있습니다. 다시 입력해주세요."
                    await channel.send(data)
                    return
            if len(content.split(" ")) == 13:
                for idx in range(1, 13):
                    if idx < 7:
                        team1List.append(content.split(" ")[idx])
                    else:
                        team2List.append(content.split(" ")[idx])

                embed = discord.Embed(title="오늘의 내전 팀편성", description="해당 명령어 문의사항은 Bewhy에게 전달해주세요", color=0xFF5733)
                embed.add_field(name="1팀", value="[탱커] "+team1List[0]+"\t"+team1List[1]+"\n[딜러] "+team1List[2]+"\t"+team1List[3]+"\n[힐러] "+team1List[4]+"\t"+team1List[5], inline=False)
                embed.add_field(name="2팀", value="[탱커] "+team2List[0]+"\t"+team2List[1]+"\n[딜러] "+team2List[2]+"\t"+team2List[3]+"\n[힐러] "+team2List[4]+"\t"+team2List[5], inline=False)
                await channel.send(embed=embed)
                return

            if len(content.split(" ")) == 15:
                for idx in range(3, 15):
                    if idx < 9:
                        team1List.append(content.split(" ")[idx])
                    else:
                        team2List.append(content.split(" ")[idx])

                embed = discord.Embed(title="오늘의 내전 팀편성", description="해당 명령어 문의사항은 Bewhy에게 전달해주세요", color=0xFF5733)
                embed.add_field(name=content.split(" ")[1], value="[탱커] "+team1List[0]+"\t"+team1List[1]+"\n[딜러] "+team1List[2]+"\t"+team1List[3]+"\n[힐러] "+team1List[4]+"\t"+team1List[5], inline=False)
                embed.add_field(name=content.split(" ")[2], value="[탱커] "+team2List[0]+"\t"+team2List[1]+"\n[딜러] "+team2List[2]+"\t"+team2List[3]+"\n[힐러] "+team2List[4]+"\t"+team2List[5], inline=False)
                await channel.send(embed=embed)
                return

        spreadsheet = await get_spreadsheet('responses1')
        roles = spreadsheet.col_values(6)
        battletags = spreadsheet.col_values(2)
        nickname = spreadsheet.col_values(3)

        try:
            index = nickname.index(content) + 1
        except gspread.exceptions.CellNotFound:
            return
        except gspread.exceptions.APIError:
            return

        # mention = spreadsheet.cell(index, 1).value
        battletag = spreadsheet.cell(index, 2).value
        link = spreadsheet.cell(index, 4).value
        description = spreadsheet.cell(index, 5).value
        thumbnaillink = spreadsheet.cell(index, 6).value
        most1 = spreadsheet.cell(index, 7).value
        most2 = spreadsheet.cell(index, 8).value
        most3 = spreadsheet.cell(index, 9).value
        batteltags= spreadsheet.cell(index, 10).value

        print(index, battletag, link, description, thumbnaillink, most1, most2, most3)

        embed = discord.Embed(title="한줄소개", description=description, color=3447003)

        if link is not '':
            embed = discord.Embed(title="한줄소개", url=link, description=description, color=3447003)

        if thumbnaillink is not '':
            embed.set_thumbnail(url=thumbnaillink)

        embed.add_field(name='모스트 1', value=most1, inline=True)
        embed.add_field(name='모스트 2', value=most2, inline=True)
        embed.add_field(name='모스트 3', value=most3, inline=True)
        embed.add_field(name='부계리스트', value=batteltags, inline=True)

        await channel.send(embed=embed)




access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
