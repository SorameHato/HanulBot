# coding: utf-8
import discord
import os
import asyncio
import pathlib
from discord.ext import commands
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
import platform
from SkyLib import tui
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
hanul_ver = "Final SP1 rev 191 (2024-01-15 10:59)"
guild_ids = [
    1030056186915082262, #테스트용 서버
    1126790936723210290 #스카이형 서버
    ]
bot.hanul_ver = hanul_ver
bot.if_loaded = 0


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='구름IDE에서 동작'))
    global LoadedTime
    if not bot.if_loaded:
        LoadedTime = str(dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f"))[:-3]+"초"
        bot.LoadedTime = LoadedTime
        if platform.system() == 'Linux' and platform.node() == 'goorm':
            bot.pf_docker = '구름IDE HanulMain (Live)'
        elif platform.system() == 'Windows':
            bot.pf_docker = 'AmeMizu (Dev)'
        else:
            bot.pf_docker = '인식할 수 없음'
        dbgChannel = await bot.fetch_channel(1137764318830665748)
        await dbgChannel.send(f'하늘봇이 {LoadedTime}에 시작되었습니다. 버전 : {bot.hanul_ver}, 환경 : {bot.pf_docker}')
        bot.if_loaded = 1
    else:
        await dbgChannel.send(f'하늘봇이 Discord 서버와 연결이 끊긴 후 {LoadedTime}에 다시 연결되었습니다. 버전 : {bot.hanul_ver}, 환경 : {bot.pf_docker}')
    print('┌──────────────────────────────────────────────────────────────────────┐')
    print('│'+tui.fixedWidth(f'{bot.user.name}(#{bot.user.id})으로 로그인되었습니다.', 70, 1)+'│')
    print('│'+tui.fixedWidth(f'봇이 시작된 시각 : {LoadedTime}', 70, 1)+'│')
    print('└──────────────────────────────────────────────────────────────────────┘')


# @bot.slash_command(name="리로드", guild_ids=guild_ids, description='봇의 모든 기능을 재시작하는 기능이에요!')
# async def reload_extension(ctx):
    # isowner = await bot.is_owner(ctx.author)
    # if isowner:
        # for filename in os.listdir(pathlib.PurePath(__file__).parent.joinpath('Cogs')):
            # if filename.endswith(".py"):
                # try:
                    # bot.reload_extension(f"Cogs.{filename[:-3]}")
                # except discord.ExtensionNotFound:
                    # channel = self.bot.get_channel(1126877960574619648)
                    # await channel.send(f":x: '{filename[:-3]}' 파일을 찾을 수 없습니다.")
                # except discord.ExtensionNotLoaded:
                    # channel = self.bot.get_channel(1126877960574619648)
                    # await channel.send(f":x: '{filename[:-3]}' 파일이 제대로 로드되지 않았습니다.")
                # except (discord.NoEntryPointError, discord.ExtensionFailed):
                    # channel = self.bot.get_channel(1126877960574619648)
                    # await channel.send(f":x: '{filename[:-3]}' 파일을 불러오는 도중 에러가 발생했습니다.")
                # else:
                    # print(f'{filename[:-3]} 파일 리로드 완료')
        # await ctx.respond(f"하늘봇의 리로드가 완료되었습니다. 새로운 패키지 번호는 {bot.repack_no}입니다.")
    # else:
        # await ctx.respond('이 명령어는 하토만 사용할 수 있습니다.')
        

def load_extensions():
    for filename in os.listdir(pathlib.PurePath(__file__).parent.joinpath('Cogs')):
        if filename.endswith('.py'):
            bot.load_extension('Cogs.{}'.format(filename[:-3]))

load_extensions()

with open(pathlib.PurePath(__file__).with_name('token.txt'),'r') as token:
    bot.run(token.readline())
