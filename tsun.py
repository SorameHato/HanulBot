import sqlite3, pathlib
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from datetime import date, time

'''
sqlite> CREATE TABLE IF NOT EXISTS 'tsun_count'(
   ...> 'uid' INTEGER UNIQUE PRIMARY KEY,
   ...> 'date' TEXT,
   ...> 'count' INTEGER DEFAULT 0,
   ...> 'level' INTEGER DEFAULT 0);
'''

def __connectDB__():
    '''
    DB에 연결한 다음 con과 cur을 return하는 함수
    이 함수를 쓸 때에는 sql_con, sql_cur = __connectDB__() 처럼
    앞에 변수를 2개 줘서 써야 한다!
    '''
    sql_con = sqlite3.connect(pathlib.PurePath(__file__).with_name('tsun.db'))
    sql_cur = sql_con.cursor()
    return sql_con, sql_cur

def __commit__(sql_con,closeCon=False):
    '''
    데이터를 커밋하고 로그에 커밋했다는 사실을 기록하는 함수
    덤으로 closeCon = True로 하면 연결도 끊어준다
    '''
    sql_con.commit()
    if closeCon:
        __closeCon__(sql_con)

def __closeCon__(sql_con):
    '''
    조회함수 같은 건 커밋을 할 필요가 없으니까
    closeCon을 단독으로 사용하기
    '''
    sql_con.close()

def __register__(uid):
    sql_con, sql_cur = __connectDB__()
    now = dt.now(tz(td(hours=9)))
    sql_cur.execute('INSERT INTO tsun_count(uid, date, count) VALUES(:uid, :dt, 1);',{'uid':uid,'dt':now})
    __commit__(sql_con, True)

def __getData__(uid:int, data_name:str):
    '''
    tsun_count 테이블에서 uid에 대한 data_name의 값을 가지고 오는 함수
    '''
    if data_name in ['uid', 'date', 'count', 'level', '*'] and (type(uid) is int or uid is None):
        sql_con, sql_cur = __connectDB__()
        if uid is None:
            sql_cur.execute(f'SELECT {data_name} FROM tsun_count;')
            dType = 2
        else:
            sql_cur.execute(f'SELECT {data_name} FROM tsun_count WHERE uid=:uid;',{'uid':uid})
            dType = 0
        sql_data = sql_cur.fetchall()
        if data_name == '*':
            dType += 1
        match dType:
            case 0:
                result = sql_data[0][0]
            case 1:
                result = sql_data[0]
            case 2:
                result = []
                for item in data:
                    result.append(item[0])
            case 3:
                result = sql_data
        __closeCon__(sql_con)
        return result
    else:
        return 0

def __dataCheck__(uid, data_name, amount, funcInfo):
    '''데이터가 잘못된 부분이 없는 지 확인하는 코드
    funcInfo는 해당 코드가 add인지 set인지 / add나 set이 아니라면 Exception
    dataList는 해당 명령어에서 처리할 수 있는 attribute의 목록
    잘못된 부분이 있으면 Exception을 raise하고 False를 반환
    잘못된 부분이 없으면 True를 반환
    dataList
    add : ['count', 'level']
    set : ['date', 'count', 'level']
    
    '''
    if funcInfo == 'add':
        dataList = ['count', 'level']
    elif funcInfo == 'set':
        dataList = ['date', 'count', 'level']
    else:
        raise ValueError(f'dataCheck 함수에서 코드 종류가 잘못 지정되었습니다. add 또는 set이 지정되어야 하는데 {funcInfo}가 지정되었습니다.')
    
    try:
        # dataList의 이름 체크
        if data_name not in dataList:
            raise ValueError(f'__{funcInfo}Data__에 지정된 attribute 이름이 잘못되었습니다. 지정된 attribute 이름은 {data_name}입니다.')
        # uid가 int인지 체크
        if type(uid) != int:
            raise TypeError(f'uid의 타입이 잘못되었습니다. uid는 int형이여야 합니다. uid의 타입 : {type(uid)}')
        # data_name이 각 형식 별 형식에 맞는지 체크
        # date : dt형
        # count, level : int형
        elif data_name == 'date':
            if type(amount) != dt and type(amount) != str:
                raise TypeError(f'amount의 타입이 잘못되었습니다. amount는 datetime형이여야 합니다. amount의 타입 : {type(amount)}')
        else:
            if type(amount) != int:
                raise TypeError(f'amount의 타입이 잘못되었습니다. amount는 int형이여야 합니다. amount의 타입 : {type(amount)}')
    except Exception as exceptA:
        raise exceptA
        return False
    else:
        return True

def __setData__(uid:int, data_name:str, amount):
    '''
    데이터 수동 수정 용으로 만든 함수임!
    date 설정하는 경우가 아니라면 절대로 함수 안에서 사용하지 말 것!
    tsun_count 테이블에서 uid에 대한 data_name의 값을
    amount로 설정하는 함수
    '''
    if __dataCheck__(uid, data_name, amount, 'set'):
        sql_con, sql_cur = __connectDB__()
        sql_cur.execute(f'UPDATE tsun_count SET {data_name}=:amount WHERE uid=:uid;',{'uid':uid,'amount':amount})
        __commit__(sql_con, True)

def __addData__(uid:int, data_name:str, amount):
    '''
    tsun_count 테이블에서 uid에 대한 data_name의 값을
    amount만큼 바꾸는 함수
    amount가 음수라도 정상적으로 작동한다!
    기존 add~ 함수 어짜피 내부에서만 쓰이니까 전부 합쳐버림
    '''
    if __dataCheck__(uid, data_name, amount, 'add'):
        sql_con, sql_cur = __connectDB__()
        sql_cur.execute(f'UPDATE tsun_count SET {data_name}={data_name}+:amount WHERE uid=:uid;',{'uid':uid,'amount':amount})
        __commit__(sql_con,True)

##############################################################
##############################################################
##### 더 이상 이 아래에서는 __connectDB__ 사용하지 말 것 #####
##############################################################
##############################################################

def getTsunLevel(uid:int):
    '''
    츤츤 레벨을 가지고 오는 함수
    DB상 레벨
    0 : 아무것도 아님
    1 : 츤 모드 해금상태 (1회차, 5시 15분이 지나면 lv를 2로 올려야 함)
    2 : 이전에 카운트 8회를 달성해서 츤 모드를 해금한 적이 있었음 (지금은 잠김)
    3 : 카운트 8회를 두 번 달성해서 영구적으로 츤 모드 유지
    return값
    0 : 아무것도 아님
    1 : 츤 모드 해금상태 (1회차, 오늘만 유지) / 억지로 해주는 느낌이 강한 대사
    2 : level 1 상태에서 5시 15분이 지나서 츤 모드가 다시 잠김
    3 : 츤 모드 해금상태 (2회차, 영구적으로 유지) / 진심으로 해주는 느낌이 강한 대사
    # 특별 메세지
    5 : level 1 상태에서 하루가 지난 후 처음으로 왔음
    6 : 츤 모드를 해금함 (1회차)
    7 : 츤 모드를 해금함 (2회차, 영구)
    '''
    try:
        level = __getData__(uid, 'level')
    except IndexError as e:
        __register__(uid)
        return 0
    if level == 3:
        return 3
    date = dt.strptime(__getData__(uid, 'date'),'%Y-%m-%d %H:%M:%S.%f%z')
    now = dt.now(tz(td(hours=9)))
    __setData__(uid,'date',now)
    if now.time() >= time(5,15):
        todayStart = dt(now.year, now.month, now.day, 5, 15, tzinfo=tz(td(hours=9)))
    else:
        todayStart = dt(now.year, now.month, now.day, 5, 15, tzinfo=tz(td(hours=9)))-td(days=1)
    if date < todayStart: #날짜가 바뀐 경우
        if level == 1:
            __setData__(uid,'count',1)
            __setData__(uid,'level',2)
            return 5
        else:
            __setData__(uid,'count',1)
            return level
    else: #날짜가 바뀌지 않은 경우
        if level == 1:
            return 1
        else:
            __addData__(uid,'count',1)
            count = __getData__(uid,'count')
            if count >= 8:
                if level == 0:
                    __setData__(uid,'count',0)
                    __setData__(uid,'level',1)
                    return 6
                elif level == 2:
                    __setData__(uid,'count',0)
                    __setData__(uid,'level',3)
                    return 7
                else:
                    return level
            else:
                return level
        