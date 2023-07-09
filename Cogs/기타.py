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
        embed.set_footer(text=f'하늘봇 버전 {hanul_ver}')
        embed.set_image(url='https://i.ibb.co/7KNJZh4/lapis10-mp4-snapshot-08-40-2023-05-26-01-52-32.png')
        await ctx.respond('아무래도 바보토끼가 또 바보토끼 한 것 같아요. 하토를 불러주세요!',embed=embed)
        raise error

def setup(bot):
    bot.add_cog(errorHandling(bot))