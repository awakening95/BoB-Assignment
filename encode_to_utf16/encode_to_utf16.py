f = open("homework.dat", "rb")
file = f.read()
size = f.tell()  # 파일의 현재 위치 반환. 즉, 파일 끝
f.close()

f = open("homework.txt", "wb")
value = b'\xff\xfe\x0d\x00\x0a\x00'
f.write(value)

i = 4
j = 4

while True:
    if file[i] == 0x0d and file[i+1] == 0x00 and file[i+2] == 0x00 and file[i+3] == 0x00 and file[i+4] == 0x0a and file[i+5] == 0x00 and file[i+6] == 0x00 and file[i+7] == 0x00:  # UTF-32
        enc = file[j:i+8]
        uni = enc.decode('UTF-32')
        utf16 = uni.encode('UTF-16-LE')
        f.write(utf16)
        i = i + 8
        j = i

    elif file[i] == 0x0d and file[i+1] == 0x00 and file[i+2] == 0x0a and file[i+3] == 0x00:  # UTF-16-LE
        enc = file[j:i+4]
        f.write(enc)
        i = i + 4
        j = i

    elif file[i] == 0x0d and file[i+1] == 0x0a:  # UTF-8 or EUC-KR
        enc = file[j:i + 2]

        try:  # UTF-8
            uni = enc.decode('UTF-8')
            utf16 = uni.encode('UTF-16-LE')

        except UnicodeDecodeError:  # EUC-KR
            try:
                uni = enc.decode('EUC-KR')
                utf16 = uni.encode('UTF-16-LE')

            except UnicodeDecodeError:  # EUC-KR을 디코딩할 때 0x57을 인식하지 못해 해당 부분을 하드코딩하기 위한 코드
                x = 0

                while enc[x] != 0x8a or enc[x + 1] != 0x57:
                    x = x + 1

                length = len(enc)

                uni = enc[0:x].decode('EUC-KR')
                utf16 = uni.encode('UTF-16-LE')
                f.write(utf16)

                utf16 = '둙'.encode('UTF-16-LE')
                f.write(utf16)

                uni = enc[x+2:length].decode('EUC-KR')
                utf16 = uni.encode('UTF-16-LE')

        f.write(utf16)
        i = i + 2
        j = i

    else:
        i = i + 1

    if i >= size - 1:
        break

f.close()