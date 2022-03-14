import socket 
import numpy as np
import cv2
import sys

exitflag=0

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
        #print("buf : ",buf)
    return buf

#접속할 IP, PORT 지정
HOST = 'localhost'
PORT = 8090

#소켓 객체 생성, 주소 체계 IPv4, 소켓 타입 TCP 사용
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#지정한 IP, PORT에 접속 시도
client_socket.connect((HOST, PORT)) 
print("connected")

while True: 

    message = '1'
    client_socket.send(message.encode())
    
    #서버에서 보낼 데이터의 크기를 미리 받음
    length = recvall(client_socket,16)
    #print("length : ",length)
    #받은 크기만큼 서버에서 데이터를 받음
    stringData = recvall(client_socket, int(length))
    #받은 데이터 변환
    data = np.frombuffer(stringData, dtype='uint8') 
    #print("data : ",data)
    #인코딩되어 들어온 데이터 디코드
    decimg=cv2.imdecode(data,1)
    #print("decimg : ",decimg)
    #서버로부터 받은 비디오 프레임 출력
    cv2.imshow('client_Image',decimg)
    
    #키 입력을 기다림
    key = cv2.waitKey(1)
    #키가 esc일 때 창 닫힘
    if key == 27:
        cv2.destroyAllWindows()
        #sys.exit()
        client_socket.close()
        #sys.exit()
        break
    