import discord
from discord.ext import commands
from datetime import datetime as dt
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids

class giveRole(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #org_message = bot.get_message(payload.message_id)
        #bot.get_message가 작동하지 않으므로 아래와 같이
        #guild를 얻고 그 안에서 channel을 얻고 그 채널에서 메세지와 멤버를
        #검색해야 한다
        #이건 반응을 남긴 사람이 아닌 원본 메세지를 보낸 사람!
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = await guild.fetch_member(message.author.id)
        # message를 봇이 보낸 게 아님 && 원 채널 아이디가 인증방인가?
        if not message.author.bot:
            if payload.channel_id == 1126871862287274145:
                # 반응을 남긴 사람의 roles의 id만 뽑아서 리스트로 만드는 작업
                roles = [i.id for i in payload.member.roles]
                # 반응을 남긴 사람의 role에 서버장이나 어드민이 있는가?
                # 1126793481151598663 : 어드민
                # 1126793415728824372 : 주인장
                # 1126793565612281926 : 즐거운 게이머
                # 1126878856582807592 : 서버 가이드 & 개발자
                if 1126793481151598663 in roles or 1126793415728824372 in roles:
                    # 즐거운 게이머 역할이 없는가?
                    roles2 = [i.id for i in member.roles]
                    if 1126793565612281926 not in roles:
                        # 즐거운 게이머 역할 추가
                        # 권한 부족이나 api 문제 등으로 인한 오류를 감지하기 위해
                        # try except 사용
                        try:
                            await member.add_roles(discord.utils.get(guild.roles, id=1126793565612281926), reason='하늘봇 즐거운 게이머 자동부여')
                        except Exception as e :
                            embed = discord.Embed(title=f'{member}님께 역할을 부여하는 동안 오류가 발생했어요!',description=f'오류 내용 : {e}',color=0xccffff)
                            embed.add_field(name='역할을 부여한 관리자',value=payload.member,inline=False)
                            embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
                            await message.channel.send(embed=embed)
                            raise e
                        else:
                            embed = discord.Embed(title=f'{member}님, 스카이와 함께하는 즐거운 게임방에 오신 것을 다시 한 번 환영합니다!',description='\'즐거운 게이머\' 역할을 부여해드렸어요! 활발한 활동 부탁드려요!\n친밀도, 출석 등의 집계를 위해 하늘봇에도 회원가입 부탁드릴게요! -★ /회원가입 명령어로 가입할 수 있어요!',color=0xccffff)
                            embed.add_field(name='역할을 부여한 관리자',value=payload.member,inline=False)
                            embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
                            await message.channel.send(f'<@{member.id}>',embed=embed)
            #1127588554780987453> 레식     1127593201885261966
            #1127588815679279154> 글옵발로 1127590110372827196
            #1127588341152485407> 미호요   1127589522763423805
            #1127588698062585917> 리듬게임 1127593088177668206
            elif payload.channel_id == 1126791814804942949:
                match payload.emoji.id:
                    case 1127593201885261966:
                        role_name = '레식'
                        role_id = 1127588554780987453
                    case 1127590110372827196:
                        role_name = '글옵발로'
                        role_id = 1127588815679279154
                    case 1127589522763423805:
                        role_name = '미호요'
                        role_id = 1127588341152485407
                    case 1127593088177668206:
                        role_name = '리듬게임'
                        role_id = 1127588698062585917
                    case _:
                        return
                try:
                    await payload.member.add_roles(discord.utils.get(guild.roles, id=role_id), reason=f'하늘봇 {role_name} 자동부여')
                except Exception as e:
                    channel = self.bot.get_channel(1126877960574619648)
                    embed = discord.Embed(title=f'{payload.member}님께 {role_name} 역할을 부여하는 동안 오류가 발생했어요!',description=f'오류 내용 : {e}',color=0xccffff)
                    embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
                    await channel.send(embed=embed)
                    raise e
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            channel = self.bot.get_channel(1126871862287274145)
            embed = discord.Embed(title=f'{member}님, 스카이와 함께하는 즐거운 게임방에 오신 것을 환영합니다!',description='인증방에 간단한 자기소개를 남겨주세요!',color=0xccffff)
            embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
            await channel.send(f'<@{member.id}>',embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            channel = self.bot.get_channel(1126790937448820878)
            embed = discord.Embed(title=f'{member}, 스카이방 지하에 묻히다.',description=f'{member}님께서 떠나셨어요.',color=0xccffff)
            embed.set_footer(text=f'하늘봇 버전 {self.bot.hanul_ver}')
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(giveRole(bot))