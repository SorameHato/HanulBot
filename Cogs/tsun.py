# coding: utf-8
import discord, pathlib, platform, random
from discord.ext import commands, tasks
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from datetime import time
global guild_ids
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from main import guild_ids
from tsun import getTsunLevel

class tsun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            keywords = ['안녕','좋은아침','좋은 아침','좋은점심','좋은 점심','좋은저녁','좋은 저녁','좋은하루','좋은 하루', '쫀아', '좋은 밤', '좋은밤', '잘자', '잘 자',
                        '쫀밤', '좋은 밤', '잘잤어', '잘 잤어', '쫀하루', '쫀점', '쫀저', '손!', '발!', '칭찬해', '매도해', '경멸해', '혼내', '나데나데', '치야호야', '호메테', '호메떼', '쓰다듬',
                        '나때', '라떼', '나 때', '라때', '라 떼', '라 때']
            responseList = ['안녕하세요! 좋은 하루에요!','에헤헤.. 쫀아에요!','좋은 점심이에요!','좋은 저녁이에요! 오늘 하루도 수고하셨어요!','안녕히 주무세요!',
                            '하늘봇은 24시간 여러분을 도와드리기 위해 깨어 있어요! 다만 하늘봇을 개발하고 있는 하토는 요즘 잘 못 자는 것 같아요..','저.. 저는 애완동물이 아니거든요!?',
                            '그... 그런 건 에루봇한테나 시키라고요..! (에루봇 호감도 75 이상 기능, 2023년 8월 이내로 업데이트 예정)',
                            '라떼는 말이에요.. 전화번호가 0361-52-0000 이런식이었다고요! (예시로 든 전화번호는 춘천-홍천 광역 버스정보시스템 ARS, 현 033-252-0000)']
            response = [0,1,1,2,2,3,3,0,0,1,3,3,4,4,
                        4,4,5,5,0,2,3,6,6,7,7,7,7,7,7,7,7,7,
                        8,8,8,8,8,8]
            reply = None
            notProper = False
            for i in range(len(keywords)):
                if f'하늘봇 {keywords[i]}' in message.content:
                    reply = i
                elif '하늘봇' in message.content and keywords[i] in message.content:
                    match message.content.find(keywords[i]) - message.content.find('하늘봇'):
                        case 3 | 4 | 5:
                            reply = i
                        case _:
                            match message.content.find('하늘봇') - message.content.find(keywords[i]) - len(keywords[i]):
                                case 0 | 1 | 2:
                                    reply = i
                                case _:
                                    pass
                                    #reply = i
                                    #notProper = True
            if reply is not None:
                if response[reply] == 7:
                    tsunLevel = getTsunLevel(message.author.id)
                    a1List = ['칭찬해', '나데나데', '치야호야', '호메테', '호메떼', '쓰다듬'] # 칭찬을 기대하는 경우
                    a2List = ['매도해', '경멸해', '혼내'] # 메스가키 같은 반응을 기대하는 경우
                    tsun1a = ['네에.. 정말 잘하셨네요..','네에.. 정말 잘 하셨어요..','네에.. 정말 대단해요..']
                    tsun1b = ['네에.. 정말 허접이네요','네에.. 정말 바보같네요..','최악..']
                    tsun3a = ['lv3 칭찬 임시대사 (추후 추가 예정)']
                    tsun3b = ['lv3 매도 임시대사 (추후 추가 예정)']
                    match tsunLevel:
                        case 0 | 2: # 0 : 아무것도 아님 | 2 : level 1 상태에서 5시 15분이 지나서 츤 모드가 다시 잠김
                            replyText = '그... 그런 건 에루봇한테나 시키라고요..!\n(에루봇 호감도 75 이상 기능, 2023년 8월 이내로 업데이트 예정)'
                        case 5: # 5 : level 1 상태에서 하루가 지난 후 처음으로 왔음
                            replyText = '오늘도 오셨네요!? 오... 오늘은 안 해드릴 거니까요..?'
                        case 6: # 6 : 츤 모드를 해금함 (1회차)
                            replyText = '아.. 알겠어요..! 해 드리면 되잖아요! 그 대신 오늘만이에요?'
                        case 7: # 7 : 츤 모드를 해금함 (2회차, 영구)
                            replyText = '우으.. 진짜 끈질기네요.. 알겠어요! 해 드릴게요!'
                        case 1: # 1 : 츤 모드 해금상태 (1회차, 오늘만 유지) / 억지로 해주는 느낌이 강한 대사
                            if keywords[reply] in a1List:
                                replyText = random.choice(tsun1a)
                            elif keywords[reply] in a2List:
                                replyText = random.choice(tsun1b)
                            else:
                                replyText = responseList[response[reply]]
                        case 3: # 3 : 츤 모드 해금상태 (2회차, 영구적으로 유지) / 진심으로 해주는 느낌이 강한 대사
                            if keywords[reply] in a1List:
                                replyText = random.choice(tsun3a)
                            elif keywords[reply] in a2List:
                                replyText = random.choice(tsun3b)
                            else:
                                replyText = responseList[response[reply]]
                        case _:
                            replyText = responseList[response[reply]]
                elif response[reply] == 8:
                    a = ['라떼는 말이에요.. 전화번호가 0361-52-0000 이런식이었어요. (예시로 든 전화번호는 춘천-홍천 광역 버스정보시스템 ARS, 현 033-252-0000)',
                         '알고 계십니까... 지구본 모양의 프로젝트 스파르탄(레거시 Edge의 원형)과 Windows Technical Preview 빌드 9841을...',
                         '라떼는 말이에요.. 묘야님이 버튜버가 아니라 그냥 그림 그리는 스트리머였어요! (2018년부터 쨀리단이었던 사람입니다)',
                         '라떼는 말이에요.. 메이플스토리에 아이테르 서버가 있었어요. 지금은 어디로 갔는지 모르겠지만요. 영원의.. 아니 영원히 망한 서버 아이테르섭 bj하늘토끼01(엔버, 102렙)의 행방을 찾습니다.',
                         '라떼는 말이에요.. 흑당 콜드브루 라떼가 제일 맛있는 것 같아요.',
                         '라떼는 말이에요.. 도오쿄오道 오오타區 가마타 4丁目의 京急(게이큐우)가마타 驛 近處의 交叉路에 京急 本線과 京急 空港線 하네다空港 第一·第二터미날 行 電車가 많이 지나가 每日 地獄門(헬-게잍)이 열렸어요.\n(해설 : 도쿄도 오타구 카마타4쵸메의 케이큐카마타역 근처의 교차로에 케이큐 본선과 케이큐 공항선 하네다공항제1·제2터미널 행 전차가 많이 지나가 매일 헬게이트가 열렸어요.)']
                    replyText = random.choice(a)
                else:
                    replyText = responseList[response[reply]]
                await message.reply(replyText)

def setup(bot):
    bot.add_cog(tsun(bot))