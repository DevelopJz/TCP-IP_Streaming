import socket 
import cv2
import numpy
from queue import Queue
import _thread
import sys

enclosure_queue = Queue()

# 쓰레드 함수 
def threaded(client_socket, addr, queue): 
    
    #클라이언트의 IP, PORT 번호 출력
    print('Connected by :', addr[0], ':', addr[1]) 

    while True: 

        try:
            #클라이언트 소켓부에서 보내는 정보 data에 저장
            data = client_socket.recv(1024)
            #데이터에 정보가 오지 않을 때 그 IP에서의 정보 전달 차단
            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break
            #받은 데이터 변수에 str형식으로 인코딩 후 전송
            stringData = queue.get()
            #공백16개를 만들고 왼쪽 정렬후 클라이언트 소켓으로 전송
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.send(stringData)

        except ConnectionResetError as e:
            #ConnectionResetError 발생시 연결 해제
            print('Disconnected by ' + addr[0],':',addr[1])
            break
    #클라이언트 소켓 종료
    client_socket.close()


def webcam(queue):

    #웹캠 카메라 연결
    capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    while True:
        #카메라 값 읽기 ret(값을 제대로 읽었을 때 True, 읽지 못할 때 False)
        #frame(비디오 한 프레임씩 읽기)
        ret, frame = capture.read()
        #frame=cv2.resize(frame,(100,100))
        if ret == False:
            continue
        #추출한 비디오 프레임(이미지)를 string 형태로 변환시키는 과정
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        #result에 비디오 프레임(이미지) 저장, rgb값의 배열로 저장
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        #print("imgencode : ",imgencode)
        #data는 위의 rgb값이 저장되어 있는 배열을 행렬화
        data = numpy.array(imgencode)
        #print("data : ",data)
        #저장된 행렬을 문자열로 변환
        stringData = data.tobytes()
        #queue에 변환된 문자열을 보냄
        queue.put(stringData)
        #웹캠에서 촬영된 비디오 출력
        cv2.imshow('server_Image', frame)
        #esc를 누르면 창닫힘
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break

#호스트 IP, 포트 설정
HOST = 'localhost'
PORT = 8090

#소켓 객체 작성, 주소 체계로 IPv4, 소켓 타입으로 TCP 사용(SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#포트 사용중이라 연결할 수 없음(WinError 10048 에러 해결) 재실행 시 포트를 해제했다가 다시 연결
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind 함수 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는 데 사용
server_socket.bind((HOST, PORT)) 
#서버가 클라이언트의 접속 대기 상태
server_socket.listen() 

print('server start\n')



while True: 

    print('wait\n')

    #클라이언트가 소켓에 접속하는 것 대기 후 접속하면 허용
    client_socket, addr = server_socket.accept()
    
    #정의한 threaded 함수를 진입점으로 지정, 함수의 입력변수 쪽에 인자 전달
    _thread.start_new_thread(threaded, (client_socket, addr, enclosure_queue,))
    
    #_thread 라이브러리의 start_new_thread : 스레드 진입점을 전달, 독립적인 스레드 생성, 전달한 스레드 진입점부터 작업 수행
    #_thread.start_new_thread(스레드 진입점, (스레드 진입점에 전달할 인자))
    _thread.start_new_thread(webcam, (enclosure_queue,))
    
    #스트리밍 종료 후 프로그램 종료 유도
    shut=input("\nProgram Close? y/n\n")
    if shut=="y":
        cv2.destroyAllWindows()
        server_socket.close()
        #sys.exit()
        _thread.exit()
        break
        #sys.exit()
    else:
        pass
    