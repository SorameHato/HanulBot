# coding: utf-8
import discord
import os
import asyncio
from discord.ext import commands
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from SkyLib import tui
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
hanul_ver = "0.0 rev 1 build 1 @ 20230704"
guild_ids = [
    1030056186915082262, #테스트용 서버
    1126790936723210290 #스카이형 서버
    ]
bot.hanul_ver = hanul_ver


@bot.event
async def on_ready():
    global LoadedTime
    LoadedTime = str(dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f"))[:-3]+"초"
    bot.LoadedTime = LoadedTime
    print('┌──────────────────────────────────────────────────────────────────────┐')
    print('│'+tui.fixedWidth(f'{bot.user.name}(#{bot.user.id})으로 로그인되었습니다.', 70, 1)+'│')
    print('│'+tui.fixedWidth(f'봇이 시작된 시각 : {LoadedTime}', 70, 1)+'│')
    print('└──────────────────────────────────────────────────────────────────────┘')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='구름IDE에서 동작'))


@bot.slash_command(name="리로드", guild_ids=guild_ids, description='봇의 모든 기능을 재시작하는 기능이에요!')
async def reload_extension(ctx):
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            try:
                await bot.unload_extension(f"Cogs.{filename[:-3]}")
            except (commands.ExtensionNotLoaded, commands.ExtensionNotFound):
                pass
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
            except commands.ExtensionNotFound:
                channel = self.bot.get_channel(1126877960574619648)
                await channel.send(f":x: '{filename[:-3]}'을(를) 파일을 찾을 수 없습니다!")
            except (commands.NoEntryPointError, commands.ExtensionFailed):
                channel = self.bot.get_channel(1126877960574619648)
                await channel.send(f":x: '{filename[:-3]}'을(를) 불러오는 도중 에러가 발생했습니다!")
    await ctx.respond(f"하늘봇의 리로드가 완료되었습니다.")
        

def load_extensions():
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            bot.load_extension('Cogs.{}'.format(filename[:-3]))

load_extensions()

with open('token.txt','r') as token:
    bot.run(token.readline())
