# coding: utf-8
import discord, pathlib
from discord.ext import commands, tasks
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from datetime import time
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids

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
            channel.send('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
        except Exception as e:
            raise e
        raise error
    
    
    @commands.slash_command(name='상태확인',guild_ids=guild_ids,description='수면 모드가 작동하는 동안 하늘봇이 제대로 작동하는 지 알기 위한 명령어에요!')
    async def checkIfRun(self, ctx):
        await ctx.respond(f'정상적으로 작동 중이에요! 마지막으로 다시 시작된 시간 : {self.bot.LoadedTime}')
    
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

def setup(bot):
    bot.add_cog(info(bot))