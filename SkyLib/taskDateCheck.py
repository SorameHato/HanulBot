from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from datetime import time


def initDateSet(now=None):
    # 여기서 now는 반드시 tzinfo=tz(td(hours=9))인 datetime 객체여야 한다!
    if now is None:
        now = dt.now(tz(td(hours=9)))
    if now.time() >= time(5,15):
        return dt.combine(now.date(),time(5,15),tzinfo=tz(td(hours=9)))+td(days=1)
    else:
        return dt.combine(now.date(),time(5,15),tzinfo=tz(td(hours=9)))

def initDateCheck(botDate):
    # 여기도 마찬가지로 tzinfo=tz(td(hours=9))인 datetime 객체여야 한다!
    now = dt.now(tz(td(hours=9)))
    if botDate <= now:
        return True
    else:
        return False
    
    
