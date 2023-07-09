import discord
from discord.ext import commands
from datetime import datetime as dt
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids

class errorHandling(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        embed = discord.Embed(title='자세한 내용',description=error,color=0xfae5fa)
        embed.add_field(name="보낸 분",value=ctx.author,inline=False)
        embed.add_field(name="보낸 내용",value=ctx.message,inline=False)
        embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
        embed.set_image(url='https://i.ibb.co/7KNJZh4/lapis10-mp4-snapshot-08-40-2023-05-26-01-52-32.png')
        await ctx.respond('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
        raise error
    
    # @commands.slash_command(name='역할빼기',guild_ids = guild_ids, description="디코 수준 왜이럼")
    # async def prob(self, ctx,role_id:discord.Option(str,'역할번호',name='역할번호')):
        # role_id = int(role_id)
        # try:
            # await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, id=role_id), reason=f'하늘봇 {role_id} 자동제거')
        # except Exception as e:
            # channel = self.bot.get_channel(1126877960574619648)
            # embed = discord.Embed(title=f'{ctx.author}님께 {role_id} 역할을 제거하는 동안 오류가 발생했어요!',description=f'오류 내용 : {e}',color=0xccffff)
            # embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
            # await channel.send(embed=embed)
            # raise e
    
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

def setup(bot):
    bot.add_cog(errorHandling(bot))