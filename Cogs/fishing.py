# coding: utf-8
import discord, random, pickle, pathlib
from discord.ext import commands, tasks
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from datetime import time
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids

class fishingPlace(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.daily_init.start()
    
    def listCheck(self, fishingList, channelID):
        '''
        낚시터가 리스트에 있는지 확인하는 함수
        있으면 True 없으면 False
        '''
        arg = False
        for item in fishingList:
            if channelID == item[0]:
                arg = True
        return arg
    
    def userCheck(self, fishingList, uid):
        '''
        유저가 이미 낚시터를 만들었는지 확인하는 함수
        있으면 낚시터 채널id 없으면 None
        '''
        arg = None
        for item in fishingList:
            if uid == item[1]:
                arg = item[0]
        return arg

    def popList(self, fishingList, channelID):
        '''
        리스트에서 해당 채널을 지우는 함수
        '''
        popList=None
        for item in fishingList:
            if channelID == item[0]:
                popList = item
        if popList != None:
            fishingList.remove(item)
        return fishingList
    
    @tasks.loop(time=time(hour=20,minute=15,tzinfo=tz(td(seconds=0))),reconnect=False)
    async def daily_init(self):
        with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'rb') as f:
            fishingList = pickle.load(f)
        dbgChannel = self.bot.get_channel(1132210917556359178)
        mainChannel = self.bot.get_channel(1126877960574619648)
        channelList = list()
        for item in fishingList:
            channelList.append(item[0])
        if channelList != []:
            for i in range(len(channelList)):
                channel = self.bot.get_channel(channelList[i])
                if channel is not None:
                    last_message = await channel.fetch_message(channel.last_message_id)
                    if last_message.edited_at is None:
                        lastWorkTime = last_message.created_at
                    else:
                        lastWorkTime = last_message.edited_at
                    if dt.now(tz(td(hours=9))) - lastWorkTime >= td(hours=1):
                        if channel.name.startswith('낚시터-'):
                            fishingList = self.popList(fishingList, channel.id)
                            with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'wb') as f:
                                pickle.dump(fishingList, f)
                            await channel.delete(reason=f'하늘봇 낚시터 자동제거(일일 초기화)')
                        else:
                            await mainChannel.send(f'{channel.id} 채널을 지우는 중 오류가 발생했어요! 해당 채널은 낚시터가 아닌 것 같아요. 하토를 불러주세요!')
            await mainChannel.send(f'정기 낚시터 정리에 성공했어요! 정리되지 않은 낚시터 : {fishingList}')
        else:
            await mainChannel.send(f'생성된 낚시터가 없어서 정기 낚시터 정리를 하지 않았어요!')
        await dbgchannel.send(f'fishing daily_init 다음 정기 정리 시간 : {self.daily_init.next_iteration.astimezone(tz=tz(td(hours=9))) if self.daily_init.next_iteration is not None else self.daily_init.next_iteration}\ncurrent_loop : {self.daily_init.current_loop}\n작동 여부 : {self.daily_init.is_running()}\n실패 여부 : {self.daily_init.failed()}')
    
    @commands.slash_command(name='산정호수긴급정지',guild_ids = guild_ids, description='낚시터 정리 프로세스가 오작동하는 경우, 긴급 정지할 수 있어요!')
    async def initStop(self, ctx, arg:discord.Option(int,'수행할 작업을 선택해주세요!(기본값 : 정지)',name='작업',choices=[discord.OptionChoice('정지',value=0),discord.OptionChoice('재시작',value=1),discord.OptionChoice('시작',value=2),discord.OptionChoice('강제 실행',value=3),discord.OptionChoice('강제 중지',value=4)],default=0)):
        match arg:
            case 0:
                self.daily_init.stop()
            case 1:
                self.daily_init.restart()
            case 2:
                self.daily_init.start()
            case 3:
                self.daily_init()
            case 4:
                self.daily_init.cancel()
            case _:
                pass
        await ctx.respond(f'요청하신 작업(case {arg})이 완료되었어요!')
    
    
    @commands.slash_command(name='산정호수',guild_ids = guild_ids, description='낚시터를 만들거나 낚시터 안에서 사용하면 낚시터를 없애요!')
    async def prob(self, ctx, arg:discord.Option(bool,'정기 정리까지 남은 시간을 표시할까요?',name='정리시간',default=False)):
        if arg:
            await ctx.respond(f'다음 정기 정리 시간 : {self.daily_init.next_iteration.astimezone(tz=tz(td(hours=9))) if self.daily_init.next_iteration is not None else self.daily_init.next_iteration}\ncurrent_loop : {self.daily_init.current_loop}\n작동 여부 : {self.daily_init.is_running()}\n실패 여부 : {self.daily_init.failed()}')
            return
        else:
            with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'rb') as f:
                fishingList = pickle.load(f)
            a = self.listCheck(fishingList, ctx.channel.id)
            b = self.userCheck(fishingList, ctx.author.id)
            if a:
                if ctx.channel.name.startswith('낚시터-'):
                    fishingList = self.popList(fishingList, ctx.channel.id)
                    with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'wb') as f:
                        pickle.dump(fishingList, f)
                    await ctx.channel.delete(reason=f'하늘봇 낚시터 자동제거({ctx.author} 사용자의 요청)')
                else:
                    ctx.respond('낚시터가 아닌 일반 채널을 지우려고 시도하시는 것 같아요! 만약 낚시터가 맞다면 어드민을 불러서 지워주세요!')
            elif b != None:
                await ctx.respond(f'이미 생성된 낚시터가 있어요! 채널 맨 아래쪽을 확인해주세요! <#{b}>',ephemeral=True)
            else:
                perm = {ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                        ctx.guild.get_member(693818502657867878) : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        ctx.guild.get_member(1126891143968346214) : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        ctx.guild.get_member(1129095389459529880) : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        ctx.author : discord.PermissionOverwrite(read_messages=True, send_messages=True)}
                cname = '낚시터-'+str(random.randint(0,9999)).zfill(4)
                channel = await ctx.guild.create_text_channel(cname,reason='하늘봇 낚시터 자동생성',position=len(ctx.guild.channels)-len(ctx.guild.categories),topic='자동으로 생성된 낚시터에요! 정기적으로 채팅이 1시간 이상 없는 경우 자동으로 삭제될 예정이에요!',overwrites=perm)
                fishingList.append([channel.id, ctx.author.id])
                await channel.send(f'<@{ctx.author.id}> 낚시터가 만들어졌어요! 여기서 이프봇을 자유롭게 사용하시면 돼요!\n낚시터는 채팅이 1시간 이상 없는 경우 자동으로 삭제돼요! 그 전에 지우고 싶으시면 이 채널 안에서 /산정호수 명령어를 다시 한 번 사용해주세요!')
                await ctx.respond(f'낚시터가 생성되었어요! 채널 맨 아래쪽을 확인해주세요! <#{channel.id}>',ephemeral=True)
                with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'wb') as f:
                    pickle.dump(fishingList, f)


def setup(bot):
    bot.add_cog(fishingPlace(bot))
