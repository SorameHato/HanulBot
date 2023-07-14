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
    
    @tasks.loop(time=time(hour=5,minute=15,tzinfo=tz(td(hours=9))))
    async def daily_init(self):
        with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'rb') as f:
            fishingList = pickle.load(f)
        informChannel = self.bot.get_channel(1126893408892502028)
        channelList = list()
        for item in fishingList:
            channelList.append(item[0])
        for i in range(len(channelList)):
            channel = self.bot.get_channel(channelList[i])
            last_message = await channel.fetch_message(channel.last_message_id)
            if last_message.edited_at == None:
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
                    await informChannel.send(f'{channel.id} 채널을 지우는 중 오류가 발생했어요! 해당 채널은 낚시터가 아닌 것 같아요. 하토를 불러주세요!')
        await informChannel.send(f'낚시터 정리에 성공했어요! 정리되지 않은 낚시터 : {fishingList}')
            
    
    @commands.slash_command(name='낚시터',guild_ids = guild_ids, description='낚시터를 만들거나 낚시터 안에서 사용하면 낚시터를 없애요!')
    async def prob(self, ctx):
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
            await ctx.respond(f'이미 생성된 낚시터가 있어요! 채널 맨 아래쪽을 확인해주세요! <#{b}>')
        else:
            perm = {ctx.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.get_member(693818502657867878) : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    ctx.guild.get_member(1126891143968346214) : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    ctx.guild.get_member(1129095389459529880) : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    ctx.author : discord.PermissionOverwrite(read_messages=True, send_messages=True)}
            cname = '낚시터-'+str(random.randint(0,9999)).zfill(4)
            channel = await ctx.guild.create_text_channel(cname,reason='하늘봇 낚시터 자동생성',position=len(ctx.guild.channels)-len(ctx.guild.categories),topic='자동으로 생성된 낚시터에요! 새벽 5시 15분 기준으로 채팅이 1시간 이상 없는 경우 자동으로 삭제될 예정이에요!',overwrites=perm)
            fishingList.append([channel.id, ctx.author.id])
            await channel.send(f'<@{ctx.author.id}> 낚시터가 만들어졌어요! 여기서 이프봇을 자유롭게 사용하시면 돼요!\n낚시터는 새벽 5시 15분 기준으로 채팅이 1시간 이상 없는 경우 자동으로 삭제돼요! 그 전에 지우고 싶으시면 이 채널 안에서 /낚시터 명령어를 다시 한 번 사용해주세요!')
            await ctx.respond(f'낚시터가 생성되었어요! 채널 맨 아래쪽을 확인해주세요! <#{channel.id}>')
            with open(pathlib.PurePath(__file__).parent.with_name('fishingList.pickle'),'wb') as f:
                pickle.dump(fishingList, f)


def setup(bot):
    bot.add_cog(fishingPlace(bot))