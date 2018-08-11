import os
import re
import sys

path = sys.argv[1]
keyword = sys.argv[2]

path = path + "\\"  # 디렉토리 경로 끝에 \ 추가

# 정규표현식
path = re.sub('"*(?P<PATH>[^"]*)"*', '\\g<PATH>', path)  # " 제거
path = re.sub("'*(?P<PATH>[^']*)'*", '\\g<PATH>', path)  # ' 제거

path = re.sub(r'[\\/]+', r'\\\\', path)  # 연속적인 \, /를 입력받으면 해당 문자열을 \\로 변환

keyword = re.sub('"*(?P<KEYWORD>[^"]*)"*', '\\g<KEYWORD>', keyword)  # " 제거
keyword = re.sub("'*(?P<KEYWORD>[^']*)'*", '\\g<KEYWORD>', keyword)  # ' 제거

# ?, *가 있는 경로의 이전 경로까지 pathPart에 할당, os.walk를 활용하기 위해
pathPart = re.sub(r'[\\]+', r'\\', path)  # \\를 \로 변경

i = 0
realPathPart = ""
while True:
    if pathPart[i] == "?" or pathPart[i] == "*":
        break
    else:
        realPathPart = realPathPart + pathPart[i]
        i = i + 1
# pathPart에 할당된 문자열 끝이 \가 아니면 \가 나올 때까지 문자열 길이를 1씩 줄임
while realPathPart[-1] != "\\":
    realPathPart = realPathPart[0:-1]

pathAll = re.sub('[?]', '.', path)  # ?를 .으로 변경, 파이썬에서 정규표현식으로 .은 하나의 문자
pathAll = re.sub('[*]', '.*', pathAll)  # *을 .*로 변경 파이썬에서 정규표현식으로 .*은 0개 혹은 N개의 아무 문자열

keywordAll = re.sub('[?]', '.', keyword)  # ?를 .으로 변경, 파이썬에서 정규표현식으로 .은 하나의 문자
keywordAll = re.sub('[*]', '.*', keywordAll)  # *을 .*로 변경 파이썬에서 정규표현식으로 .*은 0개 혹은 N개의 아무 문자열

compiled_path = re.compile(pathAll)  # pathAll 정규식 컴파일
compiled_keyword = re.compile(keywordAll)  # keywordAll 정규식 컴파일

for paths, dirs, files in os.walk(realPathPart):
    for file in files:  # 파일 탐색
        every = paths + "\\" + file  # 경로 + \ + 파일명
        if compiled_path.search(every):  # every에 저장된 문자열이 컴파일된 정규식 compiled_path와 일치한다면
            if compiled_keyword.search(file):  # file에 저장된 문자열이 컴파일된 정규식 compiled_keyword와 일치한다면
                print(every)
