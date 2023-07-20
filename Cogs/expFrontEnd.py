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
from Exp import getChatCount, getDayCount, getRegisterDate, getExp, chatCallCalc, getAllData, getYesterdayData, dailyDBInit
from SkyLib.tui import fixedWidth, fixedWidthAlt

class expFrontEnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.hanul_color=0x28d3d8
        self.morning_inform.start()
        self.daily_init_exp.start()
    
    def __time__(self, hour, minute=0, second=0):
        return time(hour=hour, minute=minute, second=second, tzinfo=tz(td(hours=9)))
    
    def __showRanking__(self,guild,since,until=None,yesterday=False,modern=False,todayOrder=False):
        if yesterday:
            data = getYesterdayData(todayOrder)
        else:
            data = getAllData(todayOrder)
        a = 0
        result=''
        if until == None or until == 0:
            until = len(data)
        if since > until:
            since = until
        for i in range(since-1, until):
            row = data[i]
            user = guild.get_member(row[0])
            nick = user.nick
            if nick == None:
                try:
                    # 2.5버전 업데이트 전 임시 코드
                    nick = user.global_name
                except AttributeError:
                    pass
                except Exception as e:
                    raise e
                    return
                finally:
                    if nick == None:
                        nick = user.display_name
            if modern:
                result += '\n' + fixedWidth(i+1,3,2) + '등 ' + fixedWidth(nick,20) + fixedWidth(str(row[1])+' (▲'+str(row[2])+', '+str(row[3])+'일차)',25,2)
            else:
                if i <= 2:
                    result += '\n**' + fixedWidth(i+1,3,2) + '등 ' + nick + ' (' +str(row[1])+' ▲'+str(row[2])+', '+str(row[3])+'일차)**'
                else:
                    result += '\n' + fixedWidth(i+1,3,2) + '등 ' + nick + ' (' +str(row[1])+' ▲'+str(row[2])+', '+str(row[3])+'일차)'
        return result
    
    @tasks.loop(time=time(hour=9,second=5,tzinfo=tz(td(hours=9))))
    async def morning_inform(self):
        now = dt.now(tz(td(hours=9)))
        tcode = self.__time__(now.hour, now.minute, now.second)
        if tcode >= self.__time__(8, 59) and tcode < self.__time__(9, 2):
            now = dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일")
            channel = self.bot.get_channel(1126792316003307670)
            await channel.send(f'{now} 오전 5시 15분 기준 랭킹 현황이에요! 더욱 많은 활동 부탁드릴게요!{self.__showRanking__(channel.guild,1,5,yesterday=True)}')
    
    @tasks.loop(time=time(hour=5,minute=15,second=1,tzinfo=tz(td(hours=9))),reconnect=False)
    async def daily_init_exp(self):
        now = dt.now(tz(td(hours=9)))
        tcode = self.__time__(now.hour, now.minute, now.second)
        if tcode >= self.__time__(5, 14) and tcode < self.__time__(5, 15, 2):
            dailyDBInit()
            now = dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일")
            channel = self.bot.get_channel(1126792316003307670)
            await channel.send(f'{now} 일일 DB 초기화 완료! 어제의 랭킹이에요!```{self.__showRanking__(channel.guild,1,5,yesterday=True,modern=True,todayOrder=True)}```')
            return
        else:
            return
    
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
    
    @commands.slash_command(name='랭킹',guild_ids=guild_ids,description='경험치 랭킹을 볼 수 있어요!')
    async def rank(self,ctx,todayOrder:discord.Option(int,'누적 순위를 표시할지 오늘 올린 경험치 순위만 표시할 지 선택해주세요!',name='정렬',choices=[discord.OptionChoice(name='누적 순위',value=0),discord.OptionChoice(name='오늘 순위',value=1),discord.OptionChoice(name='어제 순위',value=2)],default=0),arg:discord.Option(int,'몇 등까지 표시할 지 입력해주세요!', name='등수', choices=[discord.OptionChoice('5등',5),discord.OptionChoice('10등',10),discord.OptionChoice('전체',value=0)],default=0),isModern:discord.Option(int,'출력 스타일을 선택해주세요!',name='스타일',choices=[discord.OptionChoice(name='모던',value=1),discord.OptionChoice(name='텍스트',value=0)],default=1)):
        if todayOrder==2:
            if isModern:
                await ctx.respond(f'랭킹 현황이에요!```{self.__showRanking__(ctx.guild,1,arg,modern=True,todayOrder=True,yesterday=True)}```')
            else:
                await ctx.respond(f'랭킹 현황이에요!{self.__showRanking__(ctx.guild,1,arg,todayOrder=True,yesterday=True)}')
        else:
            if isModern:
                await ctx.respond(f'랭킹 현황이에요!```{self.__showRanking__(ctx.guild,1,arg,modern=True,todayOrder=todayOrder)}```')
            else:
                await ctx.respond(f'랭킹 현황이에요!{self.__showRanking__(ctx.guild,1,arg,todayOrder=todayOrder)}')
    
    # @commands.slash_command(name='유저테스트',guild_ids=guild_ids,description='유저 테스트용 명령어')
    # async def userTest(self,ctx,user:discord.Option(discord.SlashCommandOptionType.user,'소지금을 설정할 사용자를 입력해주세요.',name='사용자')):
        # result = 'get_member\n'
        # a = ctx.guild.get_member(user.id)
        # for att in dir(a):
            # result += att + ' : ' + str(getattr(a, att)) + '\n'
        # b = await ctx.guild.fetch_member(user.id)
        # result += 'fetch_member\n'
        # for att in dir(b):
            # result += att + ' : ' + str(getattr(b, att)) + '\n'
        # c = self.bot.get_user(user.id)
        # result += 'get_user\n'
        # for att in dir(c):
            # result += att + ' : ' + str(getattr(c, att)) + '\n'
        # with open('/workspace/HanulBot/output.txt', 'wt', encoding='utf-8') as a:
            # a.write(result)
        # await ctx.respond('파일을 /workspace/HanulBot/output.txt 에 저장했어요!')


def setup(bot):
    bot.add_cog(expFrontEnd(bot))
