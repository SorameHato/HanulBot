# coding: utf-8
import discord, pathlib, platform
from discord.ext import commands, tasks
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from datetime import time
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids
from Exp import getAllUser

class info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.repack_no = '0.0 rev 0 pack 2 @ 20230710'
        self.morning_greeting.start()
    
    @tasks.loop(time=time(hour=9,tzinfo=tz(td(hours=9))))
    async def morning_greeting(self):
        channel = self.bot.get_channel(1126792316003307670)
        await channel.send('오전 9시! 좋은 아침이에요! 모두 즐거운 하루 보내시고 힘내시는거에요-!')
    
    
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        embed = discord.Embed(title='자세한 내용',description=error,color=self.bot.hanul_color)
        embed.add_field(name="보낸 분",value=ctx.author,inline=False)
        embed.add_field(name="보낸 내용",value=ctx.message,inline=False)
        embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
        embed.set_image(url='https://i.ibb.co/7KNJZh4/lapis10-mp4-snapshot-08-40-2023-05-26-01-52-32.png')
        try:
            await ctx.respond('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
        except discord.NotFound:
            channel = await self.bot.fetch_channel(1126893408892502028)
            await channel.send('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
        except Exception as e:
            raise e
        raise error
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            keywords = ['안녕','좋은아침','좋은 아침','좋은점심','좋은 점심','좋은저녁','좋은 저녁','좋은하루','좋은 하루', '쫀아', '좋은 밤', '좋은밤', '잘자', '잘 자', '쫀밤', '좋은 밤', '잘잤어', '잘 잤어']
            responseList = ['좋은 하루에요!','쫀아에요!','좋은 점심이에요!','좋은 저녁이에요! 오늘 하루도 수고하셨어요!','안녕히 주무세요!','하늘봇은 24시간 여러분을 도와드리기 위해 깨어 있어요! 그치만 하늘봇을 개발하고 있는 하토는 다행히 잘 잔 것 같아요!']
            response = [0,1,1,2,2,3,3,0,0,1,3,3,4,4,4,4,5,5]
            reply = None
            notProper = False
            for i in range(len(keywords)):
                if f'하늘봇 {keywords[i]}' in message.content:
                    reply = i
                elif '하늘봇' in message.content and keywords[i] in message.content:
                    match message.content.find(keywords[i]) - message.content.find('하늘봇'):
                        case 3 | 4 | 5:
                            reply = i
                        case _:
                            match message.content.find('하늘봇') - message.content.find(keywords[i]) - len(keywords[i]):
                                case 0 | 1 | 2:
                                    reply = i
                                case _:
                                    pass
                                    #reply = i
                                    #notProper = True
            if reply is not None:
                replyText = '안녕하세요! ' + responseList[response[reply]]
                if notProper:
                    replyText += ('\n이 기능은 2020년 7월 초기 개발 단계에서 개발이 중단된 AI 유설레봇(PJU - 2.6버전)의 코드를 활용해서 만들었어요. 맥락을 파악하는 기능을 구현하는 데 실패해서 '+
                                 f'각 봇 별 이름(설레봇, 유설레봇, 아로나봇, 에루봇, 하늘봇) + \'{responseList[response[reply]]}\'이라는 말이 들어가 있으면 무조건 반응하도록 설정되어 있으니까 혹시라도 하늘봇에게 인사하려던 게 아니었으면 죄송해요!')
                await message.reply(replyText)
    
    
    @commands.slash_command(name='정보',guild_ids=guild_ids,description='하늘봇의 정보에요!')
    async def checkIfRun(self, ctx):
        expUserList, day1UserList, chatCountSum = getAllUser()
        guild = self.bot.get_guild(1126790936723210290)
        memberList = guild.members
        notJoin = []
        for member in memberList:
            if (member.id not in expUserList or member.id in day1UserList) and not member.bot:
                notJoin.append(str(member))
        now = dt.now(tz(td(hours=9)))
        compareDate = dt(2023,7,9,0,0,0,0,tzinfo=tz(td(hours=9)))
        if platform.system() == 'Linux' and platform.node() == 'goorm':
            pf_docker = 'Live(HanulMain)'
            pf_ver = platform.freedesktop_os_release()['NAME'] + ' ' + platform.freedesktop_os_release()['VERSION']
        elif platform.system() == 'Windows':
            pf_docker = 'Dev(AmeMizu)'
            pf_ver = platform.system() + ' ' + platform.win32_ver()[0] + ' 버전 ' + platform.win32_ver()[1] + ' ' + platform.win32_ver()[2]
        else:
            pf_docker = '인식할 수 없음'
            pf_ver = platform.system() + ' ' + platform.release() + ' ' + platform.version()
        await ctx.respond(f'''* 봇 정보\n> 버전 : {self.bot.hanul_ver}
        > 마지막으로 다시 시작된 시간 : {self.bot.LoadedTime}
        > 제작자 : 하토(ghwls030306@s-r.ze.am)
        > 깃허브 리포지터리 : SorameHato/HanulBot
        > 기반 : 설레봇 버전 PJU 3.2 2023060403 rev 61 build 258
        * 시스템\n> 활성 Dev 도커 : AmeMizu
        > 활성 Live 도커 : HanulMain@utwiki.run.goorm.site
        > 현재 하늘봇이 실행되고 있는 환경 : {pf_docker}
        > 운영체제 버전 : {pf_ver}
        > Python 버전 : {sys.version}
        > Pycord 버전 : {discord.__version__}-{discord.version_info[3]}
        * 경험치\n> 하늘봇 가동 일수 : {(now-compareDate).days+1}일
        > 등록된 유저 수 : {len(expUserList)}명 (서버에 있는 유저 {len(memberList)}명)
        > 채팅 집계 횟수 : {chatCountSum}회
        > * 하늘봇 가동 후 한 번도 채팅을 전송하지 않은 유저 목록
        > {", ".join(notJoin)}
        * 작업(discord.ext.tasks)\n> * info.py
        > morning_greeting : 작동 횟수 {self.morning_greeting.current_loop}회, 다음 작동 시간 : {self.morning_greeting.next_iteration.astimezone(tz=tz(td(hours=9))) if self.morning_greeting.next_iteration is not None else self.morning_greeting.next_iteration}
        > * expFrontEnd.py
        > daily_init_exp : 작동 횟수 {self.bot.daily_init_exp_count}회, 다음 작동 시간 : {self.bot.daily_init_exp_next}
        > morning_inform : 작동 횟수 {self.bot.morning_inform_count}회, 다음 작동 시간 : {self.bot.morning_inform_next}
        > * fishing.py
        > daily_init : 작동 횟수 {self.bot.daily_init_count}회, 다음 작동 시간 : {self.bot.daily_init_next}''')
    
    @commands.slash_command(name="전송", guild_ids=guild_ids, description='하토용 명령어 / 특정 채널에 메세지 전송')
    async def send_message(self, ctx, channel:discord.Option(discord.abc.GuildChannel,'채널을 선택해주세요',name='채널'),fileName:discord.Option(str,'파일명을 입력해주세요',name='파일명')='message.txt'):
        isowner = await self.bot.is_owner(ctx.author)
        if isowner:
            with open(pathlib.PurePath(__file__).parent.parent.parent.joinpath('msg',fileName),'r') as f:
                await channel.send(f.read())
            await ctx.respond('전송 완료!')
        else:
            await ctx.respond('이 기능은 하토만 이용할 수 있어요!')
    
    @commands.slash_command(name='수정', guild_ids=guild_ids, description='하토용 명령어 / 메세지 수정')
    async def edit_message(self, ctx, msg_id:discord.Option(str,'메세지 ID를 입력해주세요',name='메세지id'),channel:discord.Option(discord.abc.GuildChannel,'채널을 선택해주세요',name='채널')=None,fileName:discord.Option(str,'파일명을 입력해주세요',name='파일명')='message.txt'):
        isowner = await self.bot.is_owner(ctx.author)
        if isowner:
            try:
                msg = await ctx.fetch_message(msg_id)
            except discord.NotFound:
                if channel is None:
                    await ctx.respond('이 채널의 메세지가 아니거나 Fetch할 수 없는 메세지에요! 채널 ID를 입력해주세요!')
                else:
                    msg = await channel.fetch_message(msg_id)
            except Exception as e:
                raise e
            if 'msg' in dir() and msg is not None:
                if msg.author.id == self.bot.user.id:
                    with open(pathlib.PurePath(__file__).parent.parent.parent.joinpath('msg',fileName),'r') as f:
                        await msg.edit(f.read())
                    await ctx.respond('수정 완료!')
                else:
                    await ctx.respond('하늘봇이 쓴 메세지가 아니에요!')
        else:
            await ctx.respond('이 기능은 하토만 이용할 수 있어요!')
    
    @commands.slash_command(name='삭제', guild_ids=guild_ids, description='하토용 명령어 / 메세지 삭제')
    async def delete_message(self, ctx, msg_id:discord.Option(str,'메세지 ID를 입력해주세요',name='메세지id'),channel:discord.Option(discord.abc.GuildChannel,'채널을 선택해주세요',name='채널')=None,fileName:discord.Option(str,'파일명을 입력해주세요',name='파일명')='message.txt'):
        isowner = await self.bot.is_owner(ctx.author)
        if isowner:
            try:
                msg = await ctx.fetch_message(msg_id)
            except discord.NotFound:
                if channel is None:
                    await ctx.respond('이 채널의 메세지가 아니거나 Fetch할 수 없는 메세지에요! 채널 ID를 입력해주세요!')
                else:
                    msg = await channel.fetch_message(msg_id)
            except Exception as e:
                raise e
            if 'msg' in dir() and msg is not None:
                if msg.author.id == self.bot.user.id:
                    await msg.delete(reason='하늘봇의 버그나 수정 오류 등으로 인해 잘못된 메세지를 지우는 작업')
                    await ctx.respond('삭제 완료!')
                else:
                    await ctx.respond('하늘봇이 쓴 메세지가 아니에요!')
        else:
            await ctx.respond('이 기능은 하토만 이용할 수 있어요!')

def setup(bot):
    bot.add_cog(info(bot))