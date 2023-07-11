import sqlite3, csv, pathlib
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from datetime import date, time
from SkyLib import tui
chatPoint = 1
dayPoint = 29

'''
자세한 주석은 에루봇의 파일을 참고할 것

테이블 구조 : uid INTEGER, first_call TEXT, last_call TEXT, chat_count INTEGER, day_count INTEGER, exp INTEGER
명령어 사용 한 번 : 1 (1분당 한 번)
하루 최초 한 번 : 29

뭔가 채팅이 오면 무조건적으로 event를 발생시켜서
chatCallCalc 함수를 호출
'''

def __connectDB__():
    '''
    DB에 연결한 다음 con과 cur을 return하는 함수
    이 함수를 쓸 때에는 sql_con, sql_cur = __connectDB__() 처럼
    앞에 변수를 2개 줘서 써야 한다!
    '''
    sql_con = sqlite3.connect(pathlib.PurePath(__file__).parent.parent.joinpath('EluBot').joinpath('FriendlyRate.db'))
    sql_cur = sql_con.cursor()
    return sql_con, sql_cur

def __logWrite__(uid,task:str,text:str):
    '''
    로그에 데이터를 기록하는 함수
    현재시간(dt형),uid,task,text 와 같은 형식의 csv로 저장된다.
    uid : 말 그대로 유저의 디스코드 아이디
    task : 작업명 또는 함수명 (변경, 커밋, 생성, 조회 등)
    text : 상세한 작업 내역 (친밀도 1024.50 (1130,300,0) → 1027.50 (1131,301,0) 변경 처럼 어떤 걸 어떻게 변경했는 지 등을 상세하게 기록)
    '''
    with open(pathlib.PurePath(__file__).with_name('log.csv'),'a',encoding='utf-8',newline='') as a:
        writer = csv.writer(a)
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
    조회함수 같은 건 커밋을 할 필요가 없으니까
    closeCon을 단독으로 사용하기
    '''
    sql_con.close()
    __logWrite__('-','closeCon','DB 연결 종료')


def __createDB__(sql_con,sql_cur):
    '''
    이 함수는 수동으로만 사용되어야 하는 함수!
    에루봇을 처음 가동하기 전이나 DB 파일을 날려먹었을 때 등
    테이블이 전부 날라가거나 생성되지 않은 상황에서만 사용
    day_count가 기본값이 1인 이유는 register을 할 때 last_call이
    현재 시간으로 기록되기 때문에 따로 처리를 안 해주면 day_count가
    0부터 시작하기 때문! 첫째 날도 빼먹으면 안 되니까
    '''
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS hanul_lv (
    uid INTEGER UNIQUE PRIMARY KEY,
    first_call TEXT,
    last_call TEXT,
    chat_count INTEGER DEFAULT 0,
    day_count INTEGER DEFAULT 1,
    exp INTEGER DEFAULT 0);''')
    __logWrite__('-','생성','테이블 생성 완료')
    __commit__(sql_con,True)


def __getData__(sql_cur, uid:int, data_name:str, outside=False):
    '''
    friendly_rate 테이블에서 uid에 대한 data_name의 값을 가지고 오는 함수
    '''
    if data_name in ['first_call', 'last_call', 'chat_count', 'day_count', 'exp'] and type(uid) is int:
        sql_cur.execute(f'SELECT {data_name} FROM hanul_lv WHERE uid=:uid;',{'uid':uid})
        sql_data = sql_cur.fetchall()
        result = sql_data[0][0]
        if outside:
            __logWrite__(uid,'조회(외부)',f'{data_name}={result}')
        else:
            __logWrite__(uid,'조회(내부)',f'{data_name}={result}')
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
    add : ['command_count', 'day_count', 'total_penalty', 'friendly_rate']
    set : ['last_call', 'gunba', 'command_count', 'day_count', 'total_penalty', 'friendly_rate']
    
    '''
    if funcInfo == 'add':
        dataList = ['chat_count', 'day_count', 'exp']
    elif funcInfo == 'set':
        dataList = ['last_call', 'chat_count', 'day_count', 'exp']
    else:
        raise Exception(f'dataCheck 함수에서 코드 종류가 잘못 지정되었습니다. add 또는 set이 지정되어야 하는데 {funcInfo}가 지정되었습니다.')
    
    try:
        # dataList의 이름 체크
        if data_name not in dataList:
            raise Exception(f'__addData__에 지정된 attribute 이름이 잘못되었습니다. 지정된 attribute 이름은 {data_name}입니다.')
        # uid가 int인지 체크
        if type(uid) != int:
            raise ValueError(f'uid의 타입이 잘못되었습니다. uid는 int형이여야 합니다. uid의 타입 : {type(uid)}')
        # data_name이 각 형식 별 형식에 맞는지 체크
        # last_call : dt형
        # 그 외(command_count, day_count) : int형
        if data_name == 'last_call':
            if type(amount) != dt and type(amount) != str:
                raise ValueError(f'amount의 타입이 잘못되었습니다. amount는 datetime형이여야 합니다. amount의 타입 : {type(amount)}')
        else:
            if type(amount) != int:
                raise ValueError(f'amount의 타입이 잘못되었습니다. amount는 int형이여야 합니다. amount의 타입 : {type(amount)}')
    except Exception as exceptA:
        raise exceptA
        return False
    else:
        return True

def __setData__(sql_con, sql_cur, uid:int, data_name:str, amount, sep=False):
    '''
    데이터 수동 수정 용으로 만든 함수임!
    군바나 last_call, friendly_rate 설정하는 경우가 아니라면 절대로 함수 안에서 사용하지 말 것!
    friendly_rate 테이블에서 uid에 대한 data_name의 값을
    amount로 설정하는 함수
    '''
    if __dataCheck__(uid, data_name, amount, 'set'):
        sql_cur.execute(f'UPDATE hanul_lv SET {data_name}=:amount WHERE uid=:uid;',{'uid':uid,'amount':amount})
        if sep:
            func = 'Set(내부 수동)'
        else:
            func = 'Set(내부 자동)'
        __logWrite__(uid,func,f'{data_name} ─→ {amount}')
        __commit__(sql_con)
        if sep:
            __calcFriendlyRate__(sql_con,sql_cur,uid)
            __commit__(sql_con)

def __addData__(sql_con, sql_cur, uid:int, data_name:str, amount, sep=False):
    '''
    friendly_rate 테이블에서 uid에 대한 data_name의 값을
    amount만큼 바꾸는 함수
    amount가 음수라도 정상적으로 작동한다!
    기존 add~ 함수 어짜피 내부에서만 쓰이니까 전부 합쳐버림
    '''
    if __dataCheck__(uid, data_name, amount, 'add'):
        sql_cur.execute(f'UPDATE hanul_lv SET {data_name}=(SELECT {data_name} FROM hanul_lv WHERE uid=:uid)+:amount WHERE uid=:uid;',{'uid':uid,'amount':amount})
        if sep:
            func = 'Add(내부 수동)'
        else:
            func = 'Add(내부 자동)'
        if amount >= 0:
            __logWrite__(uid,func,f'{data_name} + {amount}')
        else:
            __logWrite__(uid,func,f'{data_name} - {abs(amount)}')
        __commit__(sql_con)
        if sep:
            __calcFriendlyRate__(sql_con, sql_cur, uid)
            __commit__(sql_con)

def __getDataFromOutside__(uid:int, attribute:str):
    '''코드가 비슷한 것 같아서 그냥 4개를 전부 합쳐버림'''
    sql_con, sql_cur = __connectDB__()
    result = __getData__(sql_cur,uid,attribute,True)
    __closeCon__(sql_con)
    return result

def getChatCount(uid:int):
    return __getDataFromOutside__(uid, 'chat_count')

def getDayCount(uid:int):
    return __getDataFromOutside__(uid, 'day_count')

def getLastCallDate(uid:int):
    return __getDataFromOutside__(uid, 'last_call')
    #str형으로 반환, 내부에서 작업할 때는 %Y-%m-%d %H:%M:%S.%f 형식으로 datetime형으로 변환해야 함

def getRegisterDate(uid:int):
    return __getDataFromOutside__(uid, 'first_call')

def getExp(uid:int):
    return __getDataFromOutside__(uid, 'exp')

def __updateLastCallDate__(sql_con, sql_cur, uid:int, date:dt, sep=False):
    '''
    마지막으로 부른 날짜를 현재 시간으로 바꾸고 마지막 호출 시간이 오늘이 아니면 day_count를 1 올리고 접속을 며칠만에 했는지에 따라 그에 따른 처리를 하는 함수
    return값은
    0 : 날짜가 바뀌지 않았음
    1 : 날짜가 바뀜
    '''
    #In [46]: dt.strptime('2023-05-01 12:34:56.789','%Y-%m-%d %H:%M:%S.%f')
    #Out[46]: datetime.datetime(2023, 5, 1, 12, 34, 56, 789000)
    __logWrite__(uid,'날짜 계산','해당 유저의 날짜계산 요청 접수')
    last_call = dt.strptime(__getData__(sql_cur, uid, 'last_call'),'%Y-%m-%d %H:%M:%S.%f')
    now = dt.now(tz(td(hours=9)))
    __setData__(sql_con, sql_cur,uid,'last_call',now)
    if now.time() >= time(5,15):
        todayStart = dt(now.year, now.month, now.day, 5, 15)
    else:
        todayStart = dt(now.year, now.month, now.day, 5, 15)-td(days=1)
    if last_call < todayStart:
        #왜 abs냐면 음수로 나와서
        #In [64]: last_call = dt.strptime('2023-07-08 05:14:59.000','%Y-%m-%d %H:%M:%S.%f')
        #In [65]: last_call - todayStart
        #Out[65]: datetime.timedelta(days=-1, seconds=86399)
        __addData__(sql_con, sql_cur, uid, 'day_count', 1)
        restDay = abs((last_call - todayStart).days)
        if restDay > 2 and restDay <= 7:
            gunba = __getData__(sql_cur,uid,'gunba')
            if not gunba:
                __addData__(sql_con, sql_cur,uid,'total_penalty',3)
            else:
                __logWrite__(uid,'commandCallCalc',f'해당 유저는 gunba가 True이므로 패널티를 부여하지 않았음')
        else:
            __addData__(sql_con, sql_cur,uid,'total_penalty',14+2*(restDay-8))
        __logWrite__(uid,'날짜 계산',f'오늘 첫 사용, 미접속일 : {restDay}일')
        returnArg = restDay
    else:
        returnArg = 0
    if sep:
        __calcFriendlyRate__(sql_con, sql_cur, uid)
    return returnArg
        

def __calcFriendlyRate__(sql_con, sql_cur, uid:int):
    '''
    현재 기록된 command_count, day_count, total_penalty의 값을 기준으로 friendly_rate를 계산하고 올바른 값으로 갱신하는 함수
    return값은 변경된 friendly_rate
    '''
    command_count = __getData__(sql_cur, uid, 'command_count')
    day_count = __getData__(sql_cur, uid, 'day_count')
    total_penalty = Decimal(str(__getData__(sql_cur, uid, 'total_penalty')))
    friendly_rate = command_count * commandPoint + day_count * dayPoint - total_penalty
    __logWrite__(uid, '친밀도 계산', f'friendly_rate = {friendly_rate}')
    __setData__(sql_con, sql_cur, uid, 'friendly_rate', float(friendly_rate))
    return friendly_rate

def commandCallCalc(uid:int, date:dt):
    '''
    먼저 sql_con과 sql_cur을 얻고
    command_count를 1 올리고
    __updateLastCallDate__을 호출해서 날짜 관련 계산을 하고
    __calcFriendlyRate__를 호출해서 친밀도를 계산한 다음
    모든 것을 커밋하고 sql 연결을 닫고
    친밀도와 lastCallArg을 리턴하는 함수
    return값은 두 개! friendlyRateArg, lastCallArg = commandCallCalc(uid, dt) 이런 식으로 적어야 함
    friendlyRateArg : 변경된 친밀도
    lastCallArg : __updateLastCallDate__의 주석 참고
    '''
    __logWrite__(uid,'commandCallCalc','해당 유저의 commandCallCalc 요청 접수')
    sql_con, sql_cur = __connectDB__()
    lastCallArg = __updateLastCallDate__(sql_con, sql_cur, uid, date)
    friendlyRateArg = __calcFriendlyRate__(sql_con, sql_cur, uid)
    __commit__(sql_con,True)
    __logWrite__(uid,'commandCallCalc',f'해당 유저의 commandCallCalc 요청 처리 완료 | lastCallArg는 {lastCallArg}')
    return friendlyRateArg, lastCallArg

if __name__ == '__main__':
    print('┌──────────────────────────┐')
    print('│   업무를 선택해주세요.   │')
    print('├───────────────┬──────────┤')
    print('│ 봇 이름       │ 데이터명 │')
    print('├───────────────┼──────────┤')
    print('│ 에루봇        │  친밀도  │')
    print('├───────────────┴──────────┤')
    print('│ 번호                메뉴 │')
    print('│ 1.           데이터 조회 │')
    print('│ 2.           데이터 설정 │')
    print('│ 3.           데이터 수정 │')
    print('│ 4.           테이블 생성 │')
    print('│ 5.             유저 등록 │')
    print('│ 6.      호감도 수동 계산 │')
    print('│ (9).        치르노(바보) │')
    print('└──────────────────────────┘')
    arg = int(input('번호 입력 : '))
    if arg == 9:
        print('BPM 999의 산수교실을 즐겨봐요!')
    elif arg == 1:
        uid = input('조회할 유저의 uid를 입력해주세요. 만약 모든 유저의 데이터를 조회하시려면 그냥 엔터를 쳐 주세요. : ')
        sql_con, sql_cur = __connectDB__()
        try:
            uid = int(uid)
        except:
            sql_cur.execute('SELECT * FROM friendly_rate;')
        else:
            sql_cur.execute('SELECT * FROM friendly_rate where uid=:uid;',{'uid':uid})
        finally:
            sql_data = sql_cur.fetchall()
            print(f'데이터 개수 : {len(sql_data)}')
            print(tui.fixedWidth('uid',20,1)+tui.fixedWidth('최초 등록 시간',27,1)+tui.fixedWidth('마지막 호출 시간',27,1)+'군바'+tui.fixedWidth('command',9,2),tui.fixedWidth('day',9,2),tui.fixedWidth('penalty',12,2),tui.fixedWidth('호감도',12,2))
            for row in sql_data:
                print(tui.fixedWidth(row[0],20)+tui.fixedWidth(row[1],27)+tui.fixedWidth(row[2],27)+tui.fixedWidth(row[3],4,1)+tui.fixedWidth(row[4],9,2),tui.fixedWidth(row[5],9,2),tui.fixedWidth(format(row[6],".2f"),12,2),tui.fixedWidth(format(row[7],".2f"),12,2))
            
    elif arg == 2:
        uid = int(input('설정할 유저의 uid를 입력해주세요. : '))
        data_name = input('설정할 attribute를 입력해주세요. : ')
        amount = input('설정할 값을 입력해주세요. : ')
        sql_con, sql_cur = __connectDB__()
        if data_name in ['total_penalty','friendly_rate']:
            amount = float(amount)
        elif data_name == 'last_call':
            pass
        else:
            amount = int(amount)
        __setData__(sql_con, sql_cur, uid, data_name, amount, True)
        __closeCon__(sql_con)
        print('설정 작업이 완료되었습니다. 데이터가 반영되었는지는 조회 메뉴에서 조회해주세요.')
    elif arg == 3:
        uid = int(input('변경할 유저의 uid를 입력해주세요. : '))
        data_name = input('변경할 attribute를 입력해주세요. : ')
        amount = input('얼만큼 변경할 지 값을 입력해주세요. (값을 늘리려면 양수, 값을 줄이려면 음수) : ')
        if data_name in ['total_penalty','friendly_rate']:
            amount = float(amount)
        elif data_name == 'last_call':
            pass
        else:
            amount = int(amount)
        sql_con, sql_cur = __connectDB__()
        __setData__(sql_con, sql_cur, uid, data_name, amount, True)
        __closeCon__(sql_con)
        print('변경 작업이 완료되었습니다. 데이터가 반영되었는지는 조회 메뉴에서 조회해주세요.')
    elif arg == 4:
        sql_con, sql_cur = __connectDB__()
        __createDB__(sql_con,sql_cur)
        print('테이블 생성이 완료되었습니다.')
    elif arg == 5:
        uid = int(input('등록할 유저의 uid를 입력해주세요. : '))
        ret = register(uid)
        if ret == 1:
            print(f'{uid} 유저의 데이터가 등록되었습니다.')
        elif ret == -1:
            print(f'{uid} 유저의 데이터가 이미 등록되어 있습니다.')
        else:
            print(f'{uid} 유저의 데이터를 등록하는 중 오류가 발생했습니다.')
    elif arg == 6:
        uid = int(input('계산할 유저의 uid를 입력해주세요. : '))
        sql_con, sql_cur = __connectDB__()
        friendly_rate = __calcFriendlyRate__(sql_con, sql_cur, uid)
        print(f'{uid} 유저의 친밀도가 다시 계산되어, {friendly_rate}로 바뀌었습니다.')
