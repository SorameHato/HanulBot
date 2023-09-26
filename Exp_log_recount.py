#coding: utf-8
import csv
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from datetime import date, time

'''
이 파일은 csv 파일에서 chatCallCalc가 호출될 때 기록되는 '해당 유저의 chatCallCalc 요청 접수'라는 메세지에 적힌 시간을 가지고 chat 카운트를 다시 계산하는 파일
먼저 해당 열을 발견하면 uid가 정보가 담긴 dict에 있는지 확인
없으면 새로 등록하고 (최종 호출 시간 : 해당 열의 시간, chat카운트 : 1)
있으면 최종 호출 시간과 해당 열의 시간을 비교
1분이 안 됐다면 그냥 지나가고
1분이 넘었으면 최종 호출 시간을 해당 열의 시간으로 업데이트하고 chat카운트를 1 늘림
이 프로그램은 수동으로 실행되는 특성상 함수 따위는 집어치우고 인터프리터 언어의 특성을 살려 순차적으로 실행되게 짰음
'''

file_locate = input('[entr] 파일의 경로를 입력해주세요. : ')
bup_file_locate = input('[entr] 기존 chat count가 있는 파일의 경로를 입력해주세요. : ')
print('[info]파일 크기 계산 중...')
length = 0
with open(file_locate, encoding='utf-8',errors='ignore') as a:
    b = csv.reader(a)
    for row in b:
        length += 1
print(f'[info] 파일 크기 : {length}')
user_orig_dict = dict()
user_dict = dict()
print(f'[info] 변수 초기화 완료')
with open(bup_file_locate,encoding='utf-8',errors='ignore') as a:
    b = csv.reader(a)
    for row in b:
        user_orig_dict[int(row[0])] = int(row[1])
print(f'[info] 기존 데이터 초기화 완료')
from tqdm import tqdm
print(f'[info] 프로세스 바 초기화 완료')
pbar = tqdm(total=length)
with open(file_locate,encoding='utf-8',errors='ignore') as a:
    b = csv.reader(a)
    for row in b:
        if row[2] == 'chatCallCalc' and row[3] == '해당 유저의 chatCallCalc 요청 접수':
            chat_time = dt.fromisoformat(row[0])
            uid = int(row[1])
            if uid in user_dict:
                if chat_time - user_dict[uid][0] >= td(seconds=60):
                    user_dict[uid][0] = chat_time
                    user_dict[uid][1] += 1
            else:
                user_dict[uid] = [chat_time,1]
        pbar.update(1)
print('[info] 계산 완료')
print(user_dict)
for key, item in user_dict.items():
    print(f'{key} : {item[1]} (▲ {item[1]-user_orig_dict[key]})')
for key, item in user_dict.items():
    print(f'UPDATE hanul_exp SET chat_count=chat_count+{item[1]-user_orig_dict[key]} where uid={key};')