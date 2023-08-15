import sqlite3, csv, pathlib
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from datetime import date, time
from SkyLib import tui
from tqdm import tqdm

def __connectDB__():
    '''
    DB에 연결한 다음 con과 cur을 return하는 함수
    이 함수를 쓸 때에는 sql_con, sql_cur = __connectDB__() 처럼
    앞에 변수를 2개 줘서 써야 한다!
    '''
    sql_con = sqlite3.connect(pathlib.PurePath(__file__).with_name('exp_test3.db'))
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
    연결을 끊는 함수
    조회함수 같은 건 커밋을 할 필요가 없으니까
    closeCon을 단독으로 사용하기
    '''
    sql_con.close()
    __logWrite__('-','closeCon','DB 연결 종료')

start = dt.now(tz(td(hours=9)))
sql_con, sql_cur = __connectDB__()
sql_cur.execute('UPDATE test SET (a, b, c, d, e, f, g, h, i, j) = (:a, :b, :c, :d, :e, :f, :g, :h, :i, :j) WHERE id=1;',{'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0})
__commit__(sql_con,True)
now = dt.now(tz(td(hours=9)))
print(f'spent {now - start}')

pbar = tqdm(total=2000)
start = dt.now(tz(td(hours=9)))
for i in range(1000):
    sql_con, sql_cur = __connectDB__()
    sql_cur.execute('UPDATE test SET (a, b, c, d, e, f, g, h, i, j) = (:a, :b, :c, :d, :e, :f, :g, :h, :i, :j) WHERE id=1;',{'a':i, 'b':i+1, 'c':i+2, 'd':i+3, 'e':i+4, 'f':i+5, 'g':i+6, 'h':i+7, 'i':i+8, 'j':i+9})
    __commit__(sql_con,True)
    pbar.update(1)
now = dt.now(tz(td(hours=9)))
print(f' spent {now - start}')

start = dt.now(tz(td(hours=9)))
for i in range(1000):
    sql_con, sql_cur = __connectDB__()
    sql_cur.execute('UPDATE test SET a=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET b=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET c=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET d=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET e=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET f=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET g=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET h=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET i=:a WHERE id=1;',{'a':i})
    sql_cur.execute('UPDATE test SET j=:a WHERE id=1;',{'a':i})
    __commit__(sql_con,True)
    pbar.update(1)
now = dt.now(tz(td(hours=9)))
print(f' spent {now - start}')