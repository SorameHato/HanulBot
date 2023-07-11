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
    
    @commands.slash_command(name='역할제거',guild_ids = guild_ids, description="역할을 제거하는 명령어에요!")
    async def prob(self, ctx, role_name:discord.Option(str,'어떤 역할을 제거할 지 선택해주세요!', name='역할명', choices=['레식','글옵발로','미호요','리듬게임'])):
        match role_name:
            case '레식':
                role_id = 1127588554780987453
            case '글옵발로':
                role_id = 1127588815679279154
            case '미호요':
                role_id = 1127588341152485407
            case '리듬게임':
                role_id = 1127588698062585917
            case _:
                return
        try:
            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, id=role_id), reason=f'하늘봇 {role_name} 자동제거')
        except Exception as e:
            channel = self.bot.get_channel(1126877960574619648)
            embed = discord.Embed(title=f'{ctx.author}님께 {role_name} 역할을 제거하는 동안 오류가 발생했어요!',description=f'오류 내용 : {e}',color=0xccffff)
            embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
            await channel.send(embed=embed)
            raise e
        else:
            await ctx.respond(f'{role_name} 역할을 성공적으로 제거했어요!')
    
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
    bot.add_cog(errorHandling(bot))