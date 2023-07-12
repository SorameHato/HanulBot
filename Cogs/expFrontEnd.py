# coding: utf-8
import discord
from discord.ext import commands, tasks
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from datetime import time
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids
from Exp import getChatCount, getDayCount, getRegisterDate, getExp, chatCallCalc, getAllData
from SkyLib.tui import fixedWidth, fixedWidthAlt

class expFrontEnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.hanul_color=0x28d3d8
    
    def __showRanking__(self,ctx,since,until=None):
        data = getAllData()
        a = 0
        result=''
        if until == None:
            until = len(data)
        if since > until:
            since = until
        for i in range(since-1, until):
            row = data[i]
            user = ctx.guild.get_member(row[0]).nick
            if user == None:
                user = ctx.guild.get_member(row[0]).display_name
            if i <= 2:
                result += '\n**' + fixedWidth(i+1,3,2) + '등 ' + fixedWidthAlt(user,20) + fixedWidthAlt('('+str(row[1])+')',10,1) + '**'
            else:
                result += '\n' + fixedWidth(i+1,3,2) + '등 ' + fixedWidthAlt(user,20) + fixedWidthAlt('('+str(row[1])+')',10,1)
        return result
    
    @tasks.loop(time=time(hour=9,second=5,tzinfo=tz(td(hours=9))))
    async def morning_inform(self):
        now = dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일")
        channel = self.bot.get_channel(1126792316003307670)
        await channel.send(f'{now} 오전 9시 기준 랭킹 현황이에요! 더욱 많은 활동 부탁드릴게요!{self.__showRanking__(ctx,1,5)}')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            try:
                f_arg, d_arg = chatCallCalc(message.author.id, dt.now(tz(td(hours=9))))
            except Exception as e:
                raise e
            else:
                match d_arg:
                    case 0:
                        pass # 날짜가 변하지 않은 경우이므로 아무것도 하지 않음
                    case 1:
                        e_title = f'{message.author}님, 오늘도 오셨네요!'
                        e_desc = '자동으로 출석이 완료되었어요! 앞으로도 매일매일 스카이방을 찾아주세요!'
                    case 2:
                        e_title = f'{message.author}님, 어제는 바쁜 일이 있으셨나요?'
                        e_desc = '스카이방을 이틀만에 찾아주셨어요! 자동으로 출석이 완료되었어요!'
                    case 3 | 4 | 5:
                        e_title = f'{message.author}님, 요즘 바쁘신건가요?'
                        e_desc = f'스카이방을 {d_arg}일만에 찾아주셨어요! 조금 더 자주 오셨으면 좋겠는데... 그래도 이렇게라도 찾아주셔서 감사해요. 자동으로 출석이 완료되었어요!'
                    case _:
                        e_title = f'{message.author}님, 오랫만이네요.'
                        e_desc = f'스카이방을 {d_arg}일만에 찾아주셨어요! 자주자주 오셨으면 좋겠는데... 그래도 가끔씩이라도 얼굴 비춰주셔서 감사해요. 자동으로 출석이 완료되었어요!'
                if d_arg:
                    channel = self.bot.get_channel(1126822172468449325)
                    embed = discord.Embed(title=e_title,description=e_desc,color=self.bot.hanul_color)
                    embed.add_field(name='현재 경험치',value=f_arg,inline=False)
                    await channel.send(f'<@{message.author.id}>',embed=embed)
    
    @commands.slash_command(name='경험치',guild_ids=guild_ids,description='자신의 경험치 현황을 볼 수 있어요!')
    async def exp_FrontEnd(self, ctx):
        embed = discord.Embed(title=f'현재 {ctx.author}님의 경험치는 {getExp(ctx.author.id)}(이)에요!',color=self.bot.hanul_color)
        embed.add_field(name='하늘봇과 함께 하기 시작한 날짜',value=getRegisterDate(ctx.author.id),inline=False)
        embed.add_field(name='스카이방과 함께한 날',value=f'{getDayCount(ctx.author.id)}일',inline=True)
        embed.add_field(name='채팅 집계 횟수',value=f'{getChatCount(ctx.author.id)}회',inline=True)
        await ctx.respond(embed=embed)
    
    @commands.slash_command(name='랭킹',guild_ids=guild_ids,description='전체 랭킹을 볼 수 있어요!')
    async def rank(self,ctx,arg:discord.Option(str,'몇 등까지 표시할 지 입력해주세요!', name='등수', choices=['10등','전체'])='전체'):
        if arg=='10등':
            await ctx.respond(f'랭킹 현황이에요!{self.__showRanking__(ctx,1,10)}')
        else:
            await ctx.respond(f'랭킹 현황이에요!{self.__showRanking__(ctx,1)}')


def setup(bot):
    bot.add_cog(expFrontEnd(bot))