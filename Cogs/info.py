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
        embed = discord.Embed(title='자세한 내용',description=error,color=0xfae5fa)
        embed.add_field(name="보낸 분",value=ctx.author,inline=False)
        embed.add_field(name="보낸 내용",value=ctx.message,inline=False)
        embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
        embed.set_image(url='https://i.ibb.co/7KNJZh4/lapis10-mp4-snapshot-08-40-2023-05-26-01-52-32.png')
        await ctx.respond('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
        raise error
    
    
    @commands.slash_command(name='상태확인',guild_ids=guild_ids,description='수면 모드가 작동하는 동안 하늘봇이 제대로 작동하는 지 알기 위한 명령어에요!')
    async def checkIfRun(self, ctx):
        await ctx.respond(f'정상적으로 작동 중이에요! 마지막으로 다시 시작된 시간 : {self.bot.LoadedTime}')
    
    
    @commands.slash_command(name='버전확인',guild_ids=guild_ids,description='리로드 확인용 임시 명령어')
    async def checkVer(self, ctx):
        await ctx.respond(f'package version : {self.bot.repack_no}, version no : 2')
    
    # @commands.slash_command(name='역할목록',guild_ids=guild_ids)
    # async def test1(self, ctx):
        # await ctx.respond(ctx.guild.roles)
    
    # @commands.slash_command(name='권한목록',guild_ids=guild_ids)
    # async def test2(self, ctx, role_id:discord.Option(str,'역할번호',name='역할번호')):
        # role_id = int(role_id)
        # role = discord.utils.get(ctx.guild.roles, id=role_id)
        # await ctx.respond(role.permissions.value)
    
    # @commands.slash_command(name='변경',guild_ids=guild_ids)
    # async def test3(self,ctx):
        # role_id =  1126790936723210290
        # role = discord.utils.get(ctx.guild.roles, id=role_id)
        # await role.edit(permissions=discord.Permissions(permissions=111022861306433))
        # await ctx.respond(role.permissions)
        
    # @commands.slash_command(name='변경',guild_ids=guild_ids)
    # async def test4(self,ctx):
        # role_id =  1126790936723210290
        # role = discord.utils.get(ctx.guild.roles, id=role_id)
        # channel = self.bot.get_channel(1126790937448820878)
        # overwrite = discord.PermissionOverwrite()
        # overwrite.read_messages = True
        # overwrite.send_messages = False
        # await channel.set_permissions(role, overwrite=overwrite)
        # await ctx.respond(channel.overwrites[0][1].pair())
        

def setup(bot):
    bot.add_cog(info(bot))