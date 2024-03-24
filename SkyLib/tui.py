import unicodedata

def __charLen__(text:str):
    '''입력받은 텍스트의 너비를 구하는 함수
    \u001b는 무시하도록 짜여져 있긴 하지만 \n, \t 같은 건 1로 치니까 주의할 것
    아래의 fullWidth와 연관되어서 사용하고 디버그용으로 단독 호출도 가능하게 했음
    실제 배포시엔 단독 호출은 불가능하게 해야겠지..? 근데 아마 배포할 일 같은 건 없을거야 아마
    text : 글자수를 알고 싶은 텍스트'''
    a = 0
    ps = False
    for header in text:
        if header == '\u001b':
            ps = True
        if ps == True:
            if header == 'm':
                ps = False
        else:
            a += 1 if unicodedata.east_asian_width(header) not in 'WF' else 2
    return a

def __charCut__(text:str,len:int):
    '''입력받은 텍스트의 너비를 지정한 len 전까지 자르고 뒤에 …을 붙이는 함수
    text : 텍스트
    len : 글자수'''
    a = 0
    returnText = ''
    ps = False
    for header in text:
        if header == '\u001b':
            ps = True
        if ps == True:
            returnText += header
            if header == 'm':
                ps = False
        else:
            byte = 1 if unicodedata.east_asian_width(header) not in 'WF' else 2
            if a + byte < len:
                a += byte
                returnText += header
            else:
                returnText += '\u001b[0m…' + (' '*(len-a-1))
                break
    return returnText

def fullWidth(leftText:str,rightText:str):
    '''입력받은 텍스트 두 개를 하나는 왼쪽 정렬로, 하나는 오른쪽 정렬로 해서 출력하는 함수
    난 ANSI 이스케이프 코드 중 커서를 움직이는 것 같은 건 모르니까 그냥 공백을 출력하는 것으로 구현했음
    먼저 leftText를 출력하고, 그 다음 터미널의 너비에서 leftText의 너비, rightText의 너비를 뺀 너비만큼 공백을 출력하고
    그 다음에 rightText를 출력하고 \n을 출력하는 함수
    즉 예전에 했던 걸 자동화(?)한거라고 보면 됨
    charLen 함수와 연동되어서 작동함'''
    resultText = str(leftText)
    blanks = 50 - __charLen__(leftText) - __charLen__(rightText)
    resultText += ' '*blanks
    resultText += str(rightText)
    return resultText

def fixedWidth(text:str,length:int,array:int=0):
    '''입력받은 텍스트를 왼쪽 정렬, 가운데 정렬, 또는 오른쪽 정렬로 해서 고정된 넓이로 출력하는 함수
    예를 들어 길이 11로 가나다라라는 텍스트를 출력하는 경우
    array : 0 (왼쪽 정렬)   '가나다라   '
    array : 1 (가운데 정렬) ' 가나다라  ' (만약 글자수가 정확히 반으로 안 나누어 떨어지면 (2의 배수가 아니면) 왼쪽으로, 공백을 오른쪽이 더 많게)
    array : 2 (오른쪽 정렬) '   가나다라'
    array : 3 (가운데 정렬) '  가나다라 ' (만약 글자수가 정확히 반으로 안 나누어 떨어지면 (2의 배수가 아니면) 오른쪽으로, 공백을 왼쪽이 더 많게)
    fullWidth를 적용하긴 조금 그렇고 각 열의 데이터의 글자수가 일정한 열 3개 이상의 표를 만들 때 유용
    만약 text의 길이가 length보다 길면 text를 width에 맞게 잘라서 return함'''
    # text가 str형이 아닌 경우를 대비하기 위한 전처리
    text = str(text)
    # 먼저 text의 길이를 체크
    txtLen = __charLen__(text)
    # 그 다음 text의 길이가 length보다 긴지 아닌지 체크
    if txtLen > length:
        return __charCut__(text,length)
    elif txtLen == length:
        return text
    # 그 다음 array의 종류를 체크, 0이나 2면 단순히 txtLen - length 만큼의 공백을 붙인 str열을 return
    # 1이나 3이면 txtLen - length가 짝수면 단순히 양쪽에 int((txtLen - length) / 2) 만큼의 공백을 붙여서 출력하고
    # 만약 홀수라면 array가 1이면 왼쪽은 int((txtLen - length) / 2) 오른쪽은 int((txtLen - length) / 2) + 1
    #              array가 3이면 왼쪽은 int((txtLen - length) / 2) + 1 오른쪽은 int((txtLen - length) / 2)
    if array == 0:
        return text + (' '*(length - txtLen))
    elif array == 2:
        return (' '*(length - txtLen)) + text
    elif array == 1 or array == 3:
        halfLen = int((length - txtLen) / 2)
        if (length - txtLen)%2 == 0:
            return (' '*halfLen) + text + (' '*halfLen)
        else:
            if array == 1:
                return (' '*halfLen) + text + (' '*(halfLen+1))
            else:
                return (' '*(halfLen+1)) + text + (' '*halfLen)
    else:
        return text

def fixedWidthAlt(text:str,length:int,array:int=0):
    '''입력받은 텍스트를 왼쪽 정렬, 가운데 정렬, 또는 오른쪽 정렬로 해서 고정된 넓이로 출력하는 함수
    예를 들어 길이 11로 가나다라라는 텍스트를 출력하는 경우
    array : 0 (왼쪽 정렬)   '가나다라   '
    array : 1 (오른쪽 정렬) '   가나다라'
    fullWidth를 적용하긴 조금 그렇고 각 열의 데이터의 글자수가 일정한 열 3개 이상의 표를 만들 때 유용
    만약 text의 길이가 length보다 길면 그냥 그 text 자체를 추가 공백 없이 return 함'''
    # text가 str형이 아닌 경우를 대비하기 위한 전처리
    text = str(text)
    # 먼저 text의 길이를 체크
    txtLen = __charLen__(text)
    # 그 다음 text의 길이가 length보다 긴지 아닌지 체크
    if txtLen >= length:
        return text
    # 그 다음 array의 종류를 체크, 0이나 2면 단순히 txtLen - length 만큼의 공백을 붙인 str열을 return
    # 1이나 3이면 txtLen - length가 짝수면 단순히 양쪽에 int((txtLen - length) / 2) 만큼의 공백을 붙여서 출력하고
    # 만약 홀수라면 array가 1이면 왼쪽은 int((txtLen - length) / 2) 오른쪽은 int((txtLen - length) / 2) + 1
    #              array가 3이면 왼쪽은 int((txtLen - length) / 2) + 1 오른쪽은 int((txtLen - length) / 2)
    if array == 0:
        return text + ('　'*int((length - txtLen)/2)) + (' '*int((length - txtLen)%2))
    elif array == 1:
        return ('　'*int((length - txtLen)/2)) + (' '*int((length - txtLen)%2)) + text
    else:
        return text

def fixedWidthArray(arrayList:list,enter:bool=False,header:bool=False):
    '''fixedWidth로 표를 쉽게 출력하기 위한 함수
    리스트의 각 행별로 fixedWidth 표를 출력
    만약 enter = True면 마지막에 NewLine 문자를 붙여서 출력
    만약 header = True면 구분선도 출력'''
    returnText = ''
    for item in arrayList:
        returnText += fixedWidth(item[0],item[1],item[2] or 0) + ' '
    returnText = returnText[:-1]
    if header:
        returnText += '\n'
        for item in arrayList:
            returnText += ('-' * item[1]) + ' '
        returnText = returnText[:-1]
    if enter:
        returnText += '\n'
    return returnText

def fixedWidthTable(setting:list,table:list):
    '''fixedWidth로 표를 더 쉽게 출력하기 위한 함수
    setting : 각 행 별로 [헤더 텍스트, length, 헤더의 array, 내용의 array]가 담긴 이중 리스트
    table : 각 줄별 내용이 담긴 이중 리스트, 한 리스트 당 한 줄
    setting의 len과 table 안에 담긴 각 list (list 안의 list)의 len은 동일해야 함
    예를 들어
    번호  이름
    1     홍길동
    2     심청
    3     이춘향
    을 출력하려고 하는 경우
    setting : [['번호',4,0,0],['이름',6,0,0]]
    table : [['1','홍길동'],['2','심청'],['3','이춘향]]
    이런 식
    '''
    returnText = ''
    tmpArray = []
    for i in range(len(setting)):
        tmpArray.append([setting[i][0],setting[i][1],setting[i][2]])
    returnText += fixedWidthArray(tmpArray,True,True)
    for item in table:
        tmpArray.clear()
        for i in range(len(item)):
            tmpArray.append([item[i],setting[i][1],setting[i][3]])
        returnText += fixedWidthArray(tmpArray,True,False)
    return returnText