import sqlite3, csv, pathlib
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from datetime import date, time
from SkyLib import tui
from typing import Union
chatPoint = 1
dayPoint = 19

'''
자세한 주석은 에루봇의 파일을 참고할 것

테이블 구조
CREATE TABLE IF NOT EXISTS "hanul_exp" (
    "uid"           INTEGER UNIQUE PRIMARY KEY,
    "first_call"    TEXT,
    "last_call"     TEXT,
    "chat_count"    INTEGER DEFAULT 1,
    "day_count"     INTEGER DEFAULT 1,
    "exp"           INTEGER DEFAULT 0,
    "silent"        INTEGER DEFAULT 0,
    "attend_room"   INTEGER DEFAULT 0
);

uid : 말 그대로 디코 id
first_call : 하늘봇에 등록한 날짜, 이건 절대로 수정되면 안 됨
last_call : 마지막으로 호출한 시간
chat_count : 채팅 횟수
day_count : 출석 일수 (매일 5시 15분 초기화)
exp : 활동점수 raw값
silent : 멘션 하는지 안 하는지 여부
attend_room : 하루종일 출석체크방에만 있었는지 여부

CREATE TABLE IF NT EXISTS "hanul_exp_final" (
    "uid"         INTEGER UNIQUE PRIMARY KEY,
    "exp_final"   INTEGER,
    "increase"    INTEGER,
    FOREIGN KEY("uid") REFERENCES "hanul_exp"("uid") ON DELETE CASCADE
);

exp_final : 어제의 exp 최종값
increase : 어제의 exp 중가값

명령어 사용 한 번 : 1 (1분당 한 번)
하루 최초 한 번 : 19

뭔가 채팅이 오면 무조건적으로 event를 발생시켜서
chatCallCalc 함수를 호출


UPDATE hanul_exp SET chat_count=chat_count+1;
-- 결과: , 53 행이 영향 받았습니다 데이터베이스에 쿼리가 성공적으로 실행되었습니다. 0ms 걸렸습니다
-- 2번째 줄:
UPDATE hanul_exp SET exp=day_count*19+chat_count;
-- 결과: , 53 행이 영향 받았습니다 데이터베이스에 쿼리가 성공적으로 실행되었습니다. 0ms 걸렸습니다
-- 3번째 줄:
SELECT * FROM hanul_exp ORDER BY exp DESC;
-- 결과: 7ms의 시간이 걸려서 53 행이 반환되었습니다
'''

def __connectDB__():
    '''
    DB에 연결한 다음 con과 cur을 return하는 함수
    이 함수를 쓸 때에는 sql_con, sql_cur = __connectDB__() 처럼
    앞에 변수를 2개 줘서 써야 한다!
    '''
    sql_con = sqlite3.connect(pathlib.PurePath(__file__).with_name('exp_test2.db'))
    sql_cur = sql_con.cursor()
    return sql_con, sql_cur

def __logWrite__(uid,task:str,text:Union[str,list]):
    '''
    로그에 데이터를 기록하는 함수
    현재시간(dt형),uid,task,text 와 같은 형식의 csv로 저장된다.
    uid : 말 그대로 유저의 디스코드 아이디
    task : 작업명 또는 함수명 (변경, 커밋, 생성, 조회 등)
    text : 상세한 작업 내역 (친밀도 1024.50 (1130,300,0) → 1027.50 (1131,301,0) 변경 처럼 어떤 걸 어떻게 변경했는 지 등을 상세하게 기록)
    '''
    with open(pathlib.PurePath(__file__).with_name('log_test.csv'),'a',encoding='utf-8',newline='') as a:
        writer = csv.writer(a)
        if isinstance(text,list):
            tmpList = [dt.now(tz(td(hours=9))),uid,task]
            tmpList.extend(text)
            writer.writerow(tmpList)
        else:
            writer.writerow([dt.now(tz(td(hours=9))),uid,task,text])

def __commit__(sql_con,closeCon=False):
    '''
    데이터를 커밋하고 로그에 커밋했다는 사실을 기록하는 함수
    덤으로 closeCon = True로 하면 연결도 끊어준다
    '''
    sql_con.commit()
    __logWrite__('-','커밋','커밋 완료')
    if closeCon:
        __closeCon__(sql_con)

def __closeCon__(sql_con):
    '''
    연결을 끊는 함수
    조회함수 같은 건 커밋을 할 필요가 없으니까
    closeCon을 단독으로 사용하기
    '''
    sql_con.close()
    __logWrite__('-','closeCon','DB 연결 종료')

def __createDB__():
    '''
    이 함수는 수동으로만 사용되어야 하는 함수!
    에루봇을 처음 가동하기 전이나 DB 파일을 날려먹었을 때 등
    테이블이 전부 날라가거나 생성되지 않은 상황에서만 사용
    day_count가 기본값이 1인 이유는 register을 할 때 last_call이
    현재 시간으로 기록되기 때문에 따로 처리를 안 해주면 day_count가
    0부터 시작하기 때문! 첫째 날도 빼먹으면 안 되니까
    '''
    sql_con, sql_cur = __connectDB__()
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS "hanul_exp" (
    "uid"           INTEGER UNIQUE PRIMARY KEY,
    "first_call"    TEXT,
    "last_call"     TEXT,
    "chat_count"    INTEGER DEFAULT 1,
    "day_count"     INTEGER DEFAULT 1,
    "exp"           INTEGER DEFAULT 0,
    "silent"        INTEGER DEFAULT 0,
    "attend_room"   INTEGER DEFAULT 0
    );''')
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS "hanul_exp_final" (
    "uid"         INTEGER UNIQUE PRIMARY KEY,
    "exp_final"   INTEGER,
    "increase"    INTEGER,
    FOREIGN KEY("uid") REFERENCES "hanul_exp"("uid") ON DELETE CASCADE
    );''')
    __logWrite__('-','생성','테이블 생성 완료')
    __commit__(sql_con,True)
    __closeCon__(sql_con)

def __dataCheck__(func, uid, data_name, amount=None):
    '''데이터가 잘못된 부분이 없는 지 확인하는 코드
    func : 해당 코드가 add인지 set인지 get인지 / add나 set, get이 아니라면 Exception
    uid : 해당 유저의 디스코드 아이디
    data_name, amount : 요청받은 data_name, amount (get은 amount는 없음)
    
    잘못된 부분이 있으면 Exception을 raise하고 False를 반환
    잘못된 부분이 없으면 True를 반환'''
    if func == 'add':
        dataList = ['chat_count', 'day_count', 'exp']
    elif func == 'set':
        dataList = ['last_call', 'chat_count', 'day_count', 'exp', 'silent', 'attend_room']
    elif func == 'get':
        dataList = ['uid', 'first_call', 'last_call', 'chat_count', 'day_count', 'exp', 'silent', 'increase', 'attend_room', '*']
        # increase는 exp - hanul_exp_final.exp_final 인 가상의 열
    else:
        raise ValueError(f'dataCheck 함수에서 코드 종류가 잘못 지정되었습니다. add, set, get 중 하나가 지정되어야 하는데 {func}가 지정되었습니다.')
    try:
        # dataList의 이름 체크
        if data_name not in dataList:
            raise ValueError(f'__addData__에 지정된 attribute 이름이 잘못되었습니다. 지정된 attribute 이름은 {data_name}입니다.')
        # uid가 int인지 체크
        if not isinstance(uid,int):
            if not (func == 'get' and uid is None):
                raise TypeError(f'uid의 타입이 잘못되었습니다. uid는 int형이여야 합니다. uid의 타입 : {type(uid)}')
        if func != 'get':
            # data_name이 각 형식 별 형식에 맞는지 체크
            # last_call : dt형
            # 그 외(command_count, day_count) : int형
            if amount is None:
                raise TypeError('amount가 없습니다.')
            else:
                if data_name == 'last_call':
                    if not(isinstance(amount,dt) or isinstance(amount,str)):
                        raise TypeError(f'amount의 타입이 잘못되었습니다. amount는 datetime형이여야 합니다. amount의 타입 : {type(amount)}')
                else:
                    if not isinstance(amount,int):
                        raise TypeError(f'amount의 타입이 잘못되었습니다. amount는 int형이여야 합니다. amount의 타입 : {type(amount)}')
    except Exception as e:
        raise e
    else:
        return True

def __getData__(uid:int, data_name, outside=False):
    '''hanul_exp 테이블에서 uid에 대한 data_name의 값을 가지고 오는 함수
    uid : 디스코드 id
    data_name : 행의 이름을 담은 리스트나 str
    '''
    if isinstance(data_name,str):
        if ';' in data_name or not __dataCheck__('get',uid,data_name):
            raise ValueError(f'dataCheck를 실행하던 중 {data_name}에서 유효하지 않은 값이 발생했습니다.')
    elif isinstance(data_name,list):
        for item in data_name:
            if isinstance(item, str):
                if ';' in data_name or not __dataCheck__('get',uid,item):
                    raise ValueError(f'dataCheck를 실행하던 중 {data_name}에서 유효하지 않은 값이 발생했습니다.')
            else:
                raise TypeError('data_name은 str형이거나 int형이여야 합니다.')

    pass # 다시 짜야 함 : modern하게 type은 isinstance로 고치고 data 유효성 체크하는 것도 고치고 등등
    # if type(data_name) != list:
    #     data_name = [data_name]
    # for item in data_name:
    #     if ';' in item:
    #         return -2097152
    #     result = __dataCheck__('get', uid, item)
    #     if not result:
    #         break
    # if result:
    #     sql_con, sql_cur = __connectDB__()
    #     if 'increase' in data_name:
    #         data_name_new = []
    #         for item in data_name:
    #             if item != 'increase':
    #                 data_name_new.append(f'hanul_exp.{item}')
    #             else:
    #                 data_name_new.append('(hanul_exp.exp-hanul_exp_final.exp_final)')
    #         data_str = ', '.join(data_name_new)
    #         table = 'hanul_exp JOIN hanul_exp_final ON hanul_exp.uid=hanul_exp_final.uid'
    #     else:
    #         data_str = ', '.join(data_name)
    #         table = 'hanul_exp'
    #     if uid is None:
    #         sql_cur.execute(f'SELECT {data_str} FROM {table} ORDER BY hanul_exp.uid ASC;')
    #         dType = 2
    #     else:
    #         sql_cur.execute(f'SELECT {data_str} FROM {table} WHERE hanul_exp.uid=:uid;',{'uid':uid})
    #         dType = 0
    #     sql_data = sql_cur.fetchall()
    #     if data_name == ['*'] or len(data_name) > 1:
    #         dType += 1
    #     match dType:
    #         case 0:
    #             result = sql_data[0][0]
    #         case 1:
    #             result = sql_data[0]
    #         case 2:
    #             result = []
    #             for item in sql_data:
    #                 result.append(item[0])
    #         case 3:
    #             result = sql_data
    #     if outside:
    #         com = '조회(외부)'
    #     else:
    #         com = '조회(내부)'
    #     if dType < 2:
    #         __logWrite__(uid,com,f'{data_name}={result}')
    #     else:
    #         __logWrite__(uid,com,f'{data_name}을 전체 유저에 걸쳐서 조회')
    #     __closeCon__(sql_con)
    #     return result
    # else:
    #     return 0

def __updateData__(uid:int, func:str, data_info, sep=False):
    '''hanul_exp의 데이터를 amount로 설정/amount만큼 변경하는 함수
    uid : 디스코드 id
    type : add인지 set인지
    data_info : [행의 이름(data_name), 설정/변경값(amount)]을 담은 리스트
    sep : 수동으로 변경하는 경우
    
    UPDATE hanul_exp SET (chat_count, day_count, exp) = (10000, 1000, day_count*19+chat_count) WHERE uid=1030044541547454476;
    '''
    if func in ['add', 'set']:
        if isinstance(data_info,list):
            safe = True
            for item in data_info:
                if isinstance(item, list):
                    if (';' in item[0]) or (';' in str(item[1])) or (not __dataCheck__(func, uid, item[0], item[1])):
                        safe = False
                        error_item = item[0]
                else:
                    raise TypeError('data_info는 이중 list형이여야 합니다.')
            if safe:
                sql_con, sql_cur = __connectDB__()
                log_data = []
                for item in data_info:
                    if func == 'add':
                        sql_cur.execute(f'UPDATE hanul_exp SET {item[0]}={item[0]}+:amount WHERE uid=:uid',{'amount':item[1],'uid':uid})
                    else:
                        sql_cur.execute(f'UPDATE hanul_exp SET {item[0]}=:amount WHERE uid=:uid',{'amount':item[1],'uid':uid})
                    log_data.append(item[0])
                    log_data.append(item[1])
                if sep:
                    func += '(내부 수동)'
                else:
                    func += '(내부 자동)'
                __logWrite__(uid,func,log_data)
                # 친밀도 계산 함수 추가해야 하는 부분
                __commit__(sql_con,True)
            else:
                raise ValueError(f'dataCheck를 실행하던 중 {error_item}의 값에서 유효하지 않은 값이 발생했습니다.' or 'dataCheck를 실행하던 중 어디에선가 오류가 발생했습니다.')
        else:
            raise TypeError('data_info는 이중 list형이여야 합니다.')
    else:
        raise ValueError(f'func는 {func}이 아닌 add 또는 set이여야 합니다.')


    # if result:
    #     sql_con, sql_cur = __connectDB__()
    #     data_str = ', '.join(data_name)
    #     sql_cur.execute(f'UPDATE hanul_exp SET :data=:amount WHERE uid={uid};',{'data':tuple(data_name), 'amount':tuple(amount)})
    #     if sep:
    #         func = 'Set(내부 수동)'
    #     else:
    #         func = 'Set(내부 자동)'
    #     __logWrite__(uid,func,f'{data_name} ─→ {amount}')
    #     __commit__(sql_con,True)