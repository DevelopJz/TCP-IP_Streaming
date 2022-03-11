# Python3 연습 과제
## 3-Python3 TCP-IP_Streaming

### 사용 언어
**Python 3.7.6**  
**Anaconda 4.8.2**

### 사용 환경
**Windows**

### 라이브러리
socket  
cv2  
numpy  
queue  
_thread  
sys

### 라이브러리 설치
```python

python -m pip install 라이브러리명

```

### 코드 설명
**CAM_server.py**  

TCP/IP 통신에서 서버 역할의 코드  
서버에서 웹캠의 영상 스트리밍, Byte화하여 클라이언트에 송신  
클라이언트에서 접속 후 영상 전송  
서버에서 출력되는 영상 확인  

**CAM_client.py**  

TCP/IP 통신에서 클라이언트 역할의 코드  
클라이언트에서 서버로 접속  
서버에서 보내는 Byte 정보 디코드 하여 영상 수신  
클라이언트로 수신된 영상 확인

출처 : https://webnautes.tistory.com/1382

### txt 파일
**jpeg 분석 파일**  

서버에서 보내는 Byte 정보 분석  
서버에서 프레임을 보낼 때 저장된 바이트의 의미 분석
