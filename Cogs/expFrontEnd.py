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
from Exp import *
from SkyLib.tui import fixedWidth, fixedWidthAlt

class expFrontEnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.hanul_color=0x28d3d8
        self.morning_inform.start()
        self.daily_init_exp.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.morning_inform_count = self.morning_inform.current_loop
        self.bot.morning_inform_next = self.morning_inform.next_iteration.astimezone(tz=tz(td(hours=9))) if self.morning_inform.next_iteration is not None else self.morning_inform.next_iteration
        self.bot.daily_init_exp_count = self.daily_init_exp.current_loop
        self.bot.daily_init_exp_next = self.daily_init_exp.next_iteration.astimezone(tz=tz(td(hours=9))) if self.daily_init_exp.next_iteration is not None else self.daily_init_exp.next_iteration
    
    
    async def __showRanking__(self,since,until=None,yesterday=False,modern=False,todayOrder=False):
        guild = self.bot.get_guild(1126790936723210290)
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
            try:
                user = await guild.fetch_member(row[0])
            except discord.NotFound:
                user = await self.bot.get_or_fetch_user(row[0])
                try:
                    # 2.5버전 업데이트 전 임시 코드
                    nick = user.global_name
                except AttributeError:
                    pass
                except Exception as e:
                    raise e
                    return
                finally:
                    nick = user.display_name
                    if nick == None:
                        nick = user.name
                    nick += '(탈퇴)'
            except Exception as e:
                raise e
            else:
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
                        if nick == None:
                            nick = user.name
            if modern:
                result += '\n' + fixedWidth(i+1,3,2) + '등 ' + fixedWidth(nick,20) + fixedWidth(str(row[1])+' (▲ '+str(row[2])+', '+str(row[3])+'일차)',25,2)
            else:
                if i <= 2:
                    result += '\n**' + fixedWidth(i+1,3,2) + '등 ' + nick.replace('_','\\_') + ' (' +str(row[1])+' ▲'+str(row[2])+', '+str(row[3])+'일차)**'
                else:
                    result += '\n' + fixedWidth(i+1,3,2) + '등 ' + nick.replace('_','\\_') + ' (' +str(row[1])+' ▲'+str(row[2])+', '+str(row[3])+'일차)'
        return result
    
    @tasks.loop(time=time(second=1,tzinfo=tz(td(hours=0))))
    async def morning_inform(self):
        now = dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일")
        dbgChannel = await self.bot.fetch_channel(1137764318830665748)
        mainChannel = await self.bot.fetch_channel(1126792316003307670)
        guild = self.bot.get_guild(1126790936723210290)
        self.bot.morning_inform_count = self.morning_inform.current_loop+1
        self.bot.morning_inform_next = self.morning_inform.next_iteration.astimezone(tz=tz(td(hours=9))) if self.morning_inform.next_iteration is not None else self.morning_inform.next_iteration
        await mainChannel.send(f'{now} 오전 5시 15분 기준 랭킹 현황이에요! 더욱 많은 활동 부탁드릴게요!{await self.__showRanking__(1,5,yesterday=True)}')
        await dbgChannel.send(f'exp morning_inform 다음 정기 알림 시간 : {self.bot.morning_inform_next}\n작동 횟수 : {self.bot.morning_inform_count}\n작동 여부 : {self.morning_inform.is_running()}\n실패 여부 : {self.morning_inform.failed()}')
    
    @tasks.loop(time=time(hour=20,minute=15,second=1,tzinfo=tz(td(seconds=0))),reconnect=False)
    async def daily_init_exp(self):
        now = dt.now(tz(td(hours=9))).strftime("%Y년 %m월 %d일")
        dbgChannel = await self.bot.fetch_channel(1137764318830665748)
        mainChannel = await self.bot.fetch_channel(1126792316003307670)
        guild = self.bot.get_guild(1126790936723210290)
        dailyDBInit()
        self.bot.daily_init_exp_count = self.daily_init_exp.current_loop+1
        self.bot.daily_init_exp_next = self.daily_init_exp.next_iteration.astimezone(tz=tz(td(hours=9))) if self.daily_init_exp.next_iteration is not None else self.daily_init_exp.next_iteration
        await mainChannel.send(f'{now} 일일 DB 초기화 완료! 어제의 랭킹이에요!```{await self.__showRanking__(1,5,yesterday=True,modern=True,todayOrder=True)}```')
        await dbgChannel.send(f'exp daily_init_exp0515 다음 정기 초기화 시간 : {self.bot.daily_init_exp_next}\n작동 횟수 : {self.bot.daily_init_exp_count}\n작동 여부 : {self.daily_init_exp.is_running()}\n실패 여부 : {self.daily_init_exp.failed()}')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.guild == self.bot.get_guild(1126790936723210290) and message.guild.get_role(1126793565612281926) in message.author.roles:
            try:
                f_arg, d_arg, c_arg = chatCallCalc(message.author.id, dt.now(tz(td(hours=9))))
            except Exception as e:
                raise e
            else:
                match d_arg:
                    case 0: # 날짜가 변경되지 않은 경우
                        if c_arg: # 첫 채팅이 출석채팅방인 경우 > 출석채팅방이 아닌 곳에서 채팅이 전송되면 attendance_only를 0으로 해야 함
                            if message.channel != self.bot.get_channel(1126822172468449325):
                                setAttendanceOnly(message.author.id,0)
                    case -1:
                        e_title = f'{message.author}님, 환영합니다!'
                        e_desc = f'출석 체크하던 도중에 오류가 발생했어요. 아마 출석 체크 자체는 되었을텐데 혹시라도 계속 멘션된다면 하토를 불러주세요.\n<@1030044541547454476> Exp.db에서 SELECT * FROM hanul_exp WHERE uid={message.author.id} 실행해서 last_call 변경되었는지, day_count 올라갔는지 확인할 것!'
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
                        e_title = f'{message.author}님, 오랜만이네요.'
                        e_desc = f'스카이방을 {d_arg}일만에 찾아주셨어요! 자주자주 오셨으면 좋겠는데... 그래도 가끔씩이라도 얼굴 비춰주셔서 감사해요. 자동으로 출석이 완료되었어요!'
                if d_arg:
                    channel = self.bot.get_channel(1126822172468449325)
                    if message.channel == channel:
                        if c_arg:
                            e_desc += '\n오늘 첫 채팅이 출석체크방에서 전송된 것 같아요. 하늘봇은 멤버 분들과 대화하다 보면 자동으로 출석을 체크해요! 스카이방에 자주 찾아와서 많이 대화해주시는 분들께 많은 이득을 드리기 위한 체계라서, 꼭 출석 명령어를 전송하지 않아도 아무 채널에서 채팅을 한 번이라도 보내면 자동으로 출석되니까 참고해주세요!'
                        else:
                            setAttendanceOnly(message.author.id,1)
                    embed = discord.Embed(title=e_title,description=e_desc,color=self.bot.hanul_color)
                    embed.add_field(name='스카이방과 함께한 날',value=f'{getDayCount(message.author.id)}일',inline=False)
                    embed.add_field(name='활동점수',value=f_arg,inline=False)
                    silentStatus = getSilentStatus(message.author.id)
                    if silentStatus:
                        await channel.send(embed=embed)
                    else:
                        await channel.send(f'<@{message.author.id}>',embed=embed)
                msg_list = [666,1004,2000]
                msg_selif = [['활동점수 666을 달성했어요!','크앙~ 악마에요! (?)'],
                             ['활동점수 1004를 달성했어요!','하늘에서 천사가~ ... 가 아니라 고인물의 반열에 끼셨네요!'],
                             ['활동점수 2000을 달성했어요!','히익.. 고인물...']
                            ]
                if d_arg == 0:
                    if f_arg in msg_list:
                        pass
                else:
                    pass
    
    exp_commands = discord.SlashCommandGroup(name="활동점수",description="활동점수의 현황과 랭킹을 보여주는 명령어에요!",guild_ids=guild_ids)
    
    @exp_commands.command(name='현황',guild_ids=guild_ids,description='자신의 활동점수 현황을 볼 수 있어요!')
    async def exp_FrontEnd(self, ctx):
        embed = discord.Embed(title=f'{ctx.author}님의 활동점수는 {getExp(ctx.author.id)} (▲ {getIncrease(ctx.author.id)})(이)에요!',color=self.bot.hanul_color)
        embed.add_field(name='하늘봇과 함께 하기 시작한 날짜',value=getRegisterDate(ctx.author.id),inline=False)
        embed.add_field(name='스카이방과 함께한 날',value=f'{getDayCount(ctx.author.id)}일',inline=True)
        embed.add_field(name='채팅 집계 횟수',value=f'{getChatCount(ctx.author.id)}회',inline=True)
        await ctx.respond(embed=embed)
    
    @exp_commands.command(name='랭킹',guild_ids=guild_ids,description='활동점수 랭킹을 볼 수 있어요!')
    async def exp_rank(self,ctx,todayOrder:discord.Option(int,'누적 순위를 표시할지 오늘 올린 점수 순위만 표시할 지 선택해주세요!',name='정렬',choices=[discord.OptionChoice(name='누적 순위',value=0),discord.OptionChoice(name='오늘 순위',value=1),discord.OptionChoice(name='어제 순위',value=2)],default=0),arg:discord.Option(int,'몇 등까지 표시할 지 입력해주세요!', name='등수', choices=[discord.OptionChoice('5등',5),discord.OptionChoice('10등',10),discord.OptionChoice('전체',value=0)],default=0),isModern:discord.Option(int,'출력 스타일을 선택해주세요!',name='스타일',choices=[discord.OptionChoice(name='모던',value=1),discord.OptionChoice(name='텍스트',value=0)],default=1)):
        respondMessage = await ctx.respond('> ⌛ 지금 랭킹을 집계하는 중이에요! 시간이 걸릴 수 있으니까 잠시만 기다려주세요!')
        if todayOrder==2:
            yesterday = True
            todayOrder = True
        else:
            yesterday = False
        if isModern:
            respond = f'활동점수 랭킹 현황이에요!```{await self.__showRanking__(1,arg,modern=True,todayOrder=todayOrder,yesterday=yesterday)}```'
        else:
            respond = f'활동점수 랭킹 현황이에요!{await self.__showRanking__(1,arg,todayOrder=todayOrder,yesterday=yesterday)}'
        try:
            #a = await respondMessage.original_response()
            #b = await a.edit(respond)
            await respondMessage.edit_original_response(content=respond)
        except discord.errors.NotFound:
            channel = self.bot.get_channel(ctx.channel.id)
            await channel.send(respond + f'\n<@{ctx.author.id}>인터렉션이 중간에 닫히는 문제가 발생해 별도의 채팅으로 전송했어요!')
        except Exception as e:
            raise e
    
    @exp_commands.command(name='멘션',guild_ids=guild_ids,description='출석 체크 시의 멘션을 켜고 끌 수 있어요!')
    async def exp_mention(self, ctx):
        result = changeSilentStatus(ctx.author.id)
        match result:
            case 0:
                respond = '성공적으로 멘션을 켰어요!'
            case 1:
                respond = '성공적으로 멘션을 껐어요!'
            case -1:
                respond = '오류가 발생했어요! (arg == 부울(bool)형 Method인 경우)'
            case -2:
                respond = '오류가 발생했어요! (arg == None인 경우)'
            case _:
                respond = f'오류가 발생했어요! (알 수 없는 오류, result : {result})'
        await ctx.respond(respond)


def setup(bot):
    bot.add_cog(expFrontEnd(bot))
