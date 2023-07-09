# coding: utf-8
import discord
from discord.ext import commands
import asyncio
from datetime import datetime as dt
import os
import sys
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
    LoadedTime = str(dt.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f"))[:-3]+"초"
    bot.LoadedTime = LoadedTime
    print('┌──────────────────────────────────────────────────────────────────────┐')
    print('│'+tui.fixedWidth(f'{bot.user.name}(#{bot.user.id})으로 로그인되었습니다.',70,1)+'│')
    print('│'+tui.fixedWidth(f'봇이 시작된 시각 : {LoadedTime}',70,1)+'│')
    print('└──────────────────────────────────────────────────────────────────────┘')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='코코아와 리제의 노래를'))

def load_extensions():
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            bot.load_extension('Cogs.{}'.format(filename[:-3]))

load_extensions()

with open('token.txt','r') as token:
    bot.run(token.readline())
