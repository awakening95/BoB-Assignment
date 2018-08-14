import os
import re
import sys
import time
import hashlib
import threading

# time1 = time.time()


class FindFile(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.file = file

    def run(self):
        every = paths + "\\" + file  # 경로 + \ + 파일명
        try:
            f = open(every, "rb")
            content = f.read()
            file_size = os.path.getsize(every)  # 파일 사이즈
            file_md5 = hashlib.md5(content).hexdigest()  # 파일의 md5 해시 값
            file_md5 = int(file_md5, 16)  # 문자열을 정수형으로 변환
            # print("1.", every, file_md5, file_size)
            # print("2.", every, md5, size)
            if file_md5 == md5 and file_size == size:
                print(every)
        except PermissionError:
            pass


path = sys.argv[1]  # 경로
path = path + "\\"  # 디렉토리 경로 끝에 \ 추가
md5 = sys.argv[2]
md5 = int(md5, 16)
size = sys.argv[3]
size = int(size, 0)

path = re.sub("'*(?P<PATH>[^']*)'*", '\\g<PATH>', path)  # 경로 양 끝에 '가 있다면 제거
path = re.sub(r'[\\/]+', r'\\\\', path)  # 연속적인 \, /를 입력받으면 해당 문자열을 \\로 변환

# ?, *가 있는 경로의 이전 경로까지 pathPart에 할당(os.walk를 활용하기 위해)
pathPart = re.sub(r'[\\]+', r'\\', path)  # \\를 \로 변경
i = 0
realPathPart = ""
while i < len(pathPart):
    if pathPart[i] == "?" or pathPart[i] == "*":
        break
    else:
        realPathPart = realPathPart + pathPart[i]
        i = i + 1
# realPathPart 할당된 문자열 끝이 \가 아니면 \가 나올 때까지 문자열 길이를 1씩 줄임
while realPathPart[-1] != "\\":
    realPathPart = realPathPart[0:-1]

# 실제 정규식에 사용할 경로 및 파일
pathAll = re.sub('[(]', '\(', path)  # (를 \(로 변경, 파이썬에서 정규표현식으로 (는 그룹을 의미
pathAll = re.sub('[)]', '\)', pathAll)  # )를 \)로 변경, 파이썬에서 정규표현식으로 )는 그룹을 의미
pathAll = re.sub('[+]', '\+', pathAll)  # +를 \+로 변경, 파이썬에서 정규표현식으로 +는 앞 패턴이 하나 이상
pathAll = re.sub('[.]', '\.', pathAll)  # .를 \.로 변경, 파이썬에서 정규표현식으로 .은 하나의 문자
pathAll = re.sub('[?]', '.', pathAll)  # ?를 .으로 변경, 파이썬에서 정규표현식으로 .은 하나의 문자
pathAll = re.sub('[*]', '.*', pathAll)  # *을 .*로 변경 파이썬에서 정규표현식으로 .*은 0개 혹은 N개의 아무 문자열

compiled_path = re.compile(pathAll)  # pathAll 정규식 컴파일

for paths, dirs, files in os.walk(realPathPart):
    if compiled_path.search(paths):
        for file in files:
            t = FindFile(file)
            t.start()

# time2 = time.time()
# print(time2-time1)
