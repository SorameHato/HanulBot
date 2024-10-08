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
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.morning_greeting_count = self.morning_greeting.current_loop
        self.bot.morning_greeting_next = self.morning_greeting.next_iteration.astimezone(tz=tz(td(hours=9))) if self.morning_greeting.next_iteration is not None else self.morning_greeting.next_iteration
    
    @tasks.loop(time=time(hour=9,tzinfo=tz(td(hours=9))))
    async def morning_greeting(self):
        channel = self.bot.get_channel(1126792316003307670)
        dbgChannel = await self.bot.fetch_channel(1137764318830665748)
        await channel.send('오전 9시! 좋은 아침이에요! 모두 즐거운 하루 보내시고 힘내시는거에요-!')
        self.bot.morning_greeting_count = self.morning_greeting.current_loop+1
        self.bot.morning_greeting_next = self.morning_greeting.next_iteration.astimezone(tz=tz(td(hours=9))) if self.morning_greeting.next_iteration is not None else self.morning_greeting.next_iteration
        await dbgChannel.send(f'exp morning_greeting {self.bot.morning_greeting_count}번째 작동, 다음은 {self.bot.morning_greeting_next}')
    
    
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
    
    info_list=[discord.OptionChoice('전체',value=0),
               discord.OptionChoice('봇 정보',value=1),
               discord.OptionChoice('시스템',value=2),
               discord.OptionChoice('활동점수',value=3),
               discord.OptionChoice('작업(태스크)',value=4)]
    
    @commands.slash_command(name='정보',guild_ids=guild_ids,description='하늘봇의 정보에요!')
    async def hanul_info(self, ctx, info_select:discord.Option(int,'보고 싶은 정보를 선택해주세요! 선택하지 않으면 기본적으로 전체를 출력해요.',name='목록',choices=info_list,default=0)):
        expUserList, day1UserList, chatCountSum = getAllUser()
        guild = self.bot.get_guild(1126790936723210290)
        memberList = guild.members
        notJoin = []
        for member in memberList:
            if (member.id not in expUserList or member.id in day1UserList) and not member.bot:
                notJoin.append(str(member))
        now = dt.now(tz(td(hours=9)))
        compareDate = dt(2023,7,9,5,15,0,0,tzinfo=tz(td(hours=9)))
        if platform.system() == 'Linux' and platform.node() == 'goorm':
            pf_docker = 'Live(HanulMain)'
            pf_ver = platform.freedesktop_os_release()['NAME'] + ' ' + platform.freedesktop_os_release()['VERSION']
        elif platform.system() == 'Linux' and platform.node() == 'aohane':
            pf_docker = 'Live(AoHane)'
            pf_ver = platform.freedesktop_os_release()['NAME'] + ' ' + platform.freedesktop_os_release()['VERSION']
        elif platform.system() == 'Windows':
            pf_docker = 'Dev(AmeMizu)'
            pf_ver = platform.system() + ' ' + platform.win32_ver()[0] + ' 버전 ' + platform.win32_ver()[1] + ' ' + platform.win32_ver()[2]
        else:
            pf_docker = '인식할 수 없음'
            pf_ver = platform.system() + ' ' + platform.release() + ' ' + platform.version()
        bot_info = f'''* 봇 정보\n> 버전 : {self.bot.hanul_ver}
        > 마지막으로 다시 시작된 시간 : {self.bot.LoadedTime}
        > 제작자 : 하토(ghwls030306@s-r.ze.am)
        > 깃허브 리포지터리 : SorameHato/HanulBot
        > 기반 : 설레봇 버전 PJU 3.2 2023060403 rev 61 build 258
        > 인증키 : {"SKFLOW-KB5MDC-R5B3OS-BSHCM9 (유료(특별계약) 플랜)" if ctx.guild == guild else "DANBII-NYANYA-KAWAII-SUGIRU (유료(개발용) 플랜)"}
        > 유료 기능 계약 조건 : {"제가 서버 개발자로 있는 스카이형 서버는 평생 무료로 제공할 예정입니다." if ctx.guild == guild else"""~~카와이이한 아타시쟝은 평생 무료!~~
        테스트 서버 (DANBII-NYANYA-KAWAII-SUGIRU) : 테스트용 라이센스입니다.
        단비냐아 서버 (AMEAME-NYANYA-KAWAII-SUGIRU) : 하토에게 큰 힘이 되어주었던 아메는 평생 무료
        스카이방 (SKFLOW-KB5MDC-R5B3OS-BSHCM9) : 제가 서버 개발자로 있는 스카이형 서버는 평생 무료로 제공할 예정입니다.
        など / サーバー別に入力"""}'''
        bot_system = f'''* 시스템\n> 활성 Dev 도커 : AmeMizu
        > 활성 Live 도커 : AoHane@amene.co
        > 현재 하늘봇이 실행되고 있는 환경 : {pf_docker}
        > 운영체제 버전 : {pf_ver}
        > Python 버전 : {sys.version}
        > Pycord 버전 : {discord.__version__}-{discord.version_info[3]}'''
        bot_exp = f'''* 활동점수\n> 하늘봇 가동 일수 : {(now-compareDate).days}일
        > 등록된 유저 수 : {len(expUserList)}명 (서버에 있는 유저 {len(memberList)}명)
        > 채팅 집계 횟수 : {chatCountSum}회
        > * 하늘봇 가동 후 한 번도 채팅을 전송하지 않은 유저 목록
        > {", ".join(notJoin)}'''
        bot_task = f'''* 작업(discord.ext.tasks)\n> * info.py
        > morning_greeting : 작동 횟수 {self.bot.morning_greeting_count}회, 다음 작동 시간 : {self.bot.morning_greeting_next}
        > * expFrontEnd.py
        > daily_init_exp : 작동 횟수 {self.bot.daily_init_exp_count}회, 다음 작동 시간 : {self.bot.daily_init_exp_next}
        > morning_inform : 작동 횟수 {self.bot.morning_inform_count}회, 다음 작동 시간 : {self.bot.morning_inform_next}'''
        match info_select:
            case 0:
                await ctx.respond(f'{bot_info}\n{bot_system}\n{bot_exp}\n{bot_task}')
            case 1:
                await ctx.respond(bot_info)
            case 2:
                await ctx.respond(bot_system)
            case 3:
                await ctx.respond(bot_exp)
            case 4:
                await ctx.respond(bot_task)
            case _:
                await ctx.respond(f'{bot_info}\n{bot_system}\n{bot_exp}\n{bot_task}')
        
    
    @commands.slash_command(name='건의',guild_ids=guild_ids,description='하늘봇에 건의하실 게 있으시면 이 명령어를 이용해주세요!')
    async def 건의(self, ctx):
        await ctx.respond(f'<#1126893408892502028> 이 쪽에서 하토를 멘션해서 편하게 말씀해주세요! 저는 24시간 언제든지 괜찮으니까 편하게 멘션해주세요!',ephemeral=True)
    
    dbg_commands = discord.SlashCommandGroup(name="디버그",description="도박과 관련된 명령어에요!",guild_ids=guild_ids)
    
    @dbg_commands.command(name="전송", guild_ids=guild_ids, description='하토용 명령어 / 특정 채널에 메세지 전송')
    async def send_message(self, ctx, channel:discord.Option(discord.abc.GuildChannel,'채널을 선택해주세요',name='채널'),fileName:discord.Option(str,'파일명을 입력해주세요',name='파일명')='message.txt'):
        isowner = await self.bot.is_owner(ctx.author)
        if isowner:
            respondMessage = await ctx.respond('> ⌛ 전송 중이에요! 잠시만 기다려주세요!',ephemeral=True)
            with open(pathlib.PurePath(__file__).parent.parent.joinpath('msg',fileName),'r') as f:
                await channel.send(f.read())
            await respondMessage.edit_original_response(content='전송 완료!')
        else:
            await ctx.respond('이 기능은 하토만 이용할 수 있어요!')
    
    @dbg_commands.command(name='수정', guild_ids=guild_ids, description='하토용 명령어 / 메세지 수정')
    async def edit_message(self, ctx, msg_id:discord.Option(str,'메세지 ID를 입력해주세요',name='메세지id'),channel:discord.Option(discord.abc.GuildChannel,'채널을 선택해주세요',name='채널')=None,fileName:discord.Option(str,'파일명을 입력해주세요',name='파일명')='message.txt'):
        isowner = await self.bot.is_owner(ctx.author)
        if isowner:
            respondMessage = await ctx.respond('> ⌛ 수정 중이에요! 잠시만 기다려주세요!',ephemeral=True)
            try:
                msg = await ctx.fetch_message(msg_id)
            except discord.NotFound:
                if channel is None:
                    await respondMessage.edit_original_response(content='이 채널의 메세지가 아니거나 Fetch할 수 없는 메세지에요! 채널 ID를 입력해주세요!')
                else:
                    msg = await channel.fetch_message(msg_id)
            except Exception as e:
                raise e
            if 'msg' in dir() and msg is not None:
                if msg.author.id == self.bot.user.id:
                    with open(pathlib.PurePath(__file__).parent.parent.joinpath('msg',fileName),'r') as f:
                        await msg.edit(f.read())
                    await respondMessage.edit_original_response(content='수정 완료!')
                else:
                    await respondMessage.edit_original_response(content='하늘봇이 쓴 메세지가 아니에요!')
        else:
            await ctx.respond('이 기능은 하토만 이용할 수 있어요!')
    
    @dbg_commands.command(name='삭제', guild_ids=guild_ids, description='하토용 명령어 / 메세지 삭제')
    async def delete_message(self, ctx, msg_id:discord.Option(str,'메세지 ID를 입력해주세요',name='메세지id'),channel:discord.Option(discord.abc.GuildChannel,'채널을 선택해주세요',name='채널')=None):
        isowner = await self.bot.is_owner(ctx.author)
        if isowner:
            respondMessage = await ctx.respond('> ⌛ 삭제 중이에요! 잠시만 기다려주세요!',ephemeral=True)
            try:
                msg = await ctx.fetch_message(msg_id)
            except discord.NotFound:
                if channel is None:
                    await respondMessage.edit_original_response(content='이 채널의 메세지가 아니거나 Fetch할 수 없는 메세지에요! 채널 ID를 입력해주세요!')
                else:
                    msg = await channel.fetch_message(msg_id)
            except Exception as e:
                raise e
            if 'msg' in dir() and msg is not None:
                if msg.author.id == self.bot.user.id:
                    await msg.delete(reason='하늘봇의 버그나 수정 오류 등으로 인해 잘못된 메세지를 지우는 작업')
                    await respondMessage.edit_original_response(content='삭제 완료!')
                else:
                    await respondMessage.edit_original_response(content='하늘봇이 쓴 메세지가 아니에요!')
        else:
            await ctx.respond('이 기능은 하토만 이용할 수 있어요!')

def setup(bot):
    bot.add_cog(info(bot))
