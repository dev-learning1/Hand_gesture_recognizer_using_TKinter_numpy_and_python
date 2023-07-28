# Hand_gesture_recognizer_using_TKinter_numpy_and_python
Hand gesture recognizer using TKinter, numpy, and python

※ TKinter와 numpy, python 을 이용하여 손 제스처 인식기를 만들어 보자. 아래와 같은 10
개의 클래스에 대해 17명으로부터 20번씩 입력 받은 200개의 영상이 있다. 

![image](https://github.com/dev-learning1/Hand_gesture_recognizer_using_TKinter_numpy_and_python/assets/115637631/85fa57a8-26e8-4e1e-be9c-85fecdf456b9)

200개의 파일중 각클래스의 1번 파일을 클래스를 대표하는 템플릿 𝑇𝑖 라 할 때, 임의로 입력 받
은 영상 X 를 읽어 들여 각 템플릿과 이 영상간 오차를 계산하고 가장 작은 오차를 기록하는 순
서에 기반하여 클래스를 인식하라. 

![image](https://github.com/dev-learning1/Hand_gesture_recognizer_using_TKinter_numpy_and_python/assets/115637631/af3924a5-4e76-4adc-9620-77a1417c6632)

1) 원본 파일 종류, 원본 파일 이름, 원본 파일 크기를 절대 수정하지 말 것. 
2) TKinter를 import 하여 다음의 화면을 구성하라. 
3) 붉은 색 영역 : 
메뉴 ‘파일’ 의 ‘템플릿 등록하기’를 실행하면 10개 클래스를 대표하는 10개의 영상을 선
택하고 선택한 파일을 붉은색 영역에 순서에 맞춰 표시할 것. 이때, 원본파일은 손상시키
지 않은 채 영상의 크기를 창의 크기를 고려해 축소할 것. 불러들인 파일이 10개가 아니
면 오류창 출력!
4) 파란색 영역 :
‘인식파일 불러오기’를 실행하면 임의 개수의 파일을 불러들이되, 파란색 영역에 인식순서
에 맞춰 차례대로 하나씩 그림을 출력할 것. 이때는 원본 영상의 크기를 그대로 살려서
출력. 
5) 녹색 영역 : 
위 상태에서 ‘Run!’ 버튼을 누르면 template matching을 실행
6) 노란색 영역 : 
현재 불러들인 파일과 각 원본 템플릿간 오차 계산 결과를 출력하는 창. 스크롤바를 장착
할 것. Run 버튼을 누를 때마다 내용을 새로 출력할 것. 
7) 보라색 영역 : 
읽어들인 파일의 클래스와 template matching이 결론낸 결과를 출력하고 비교하는 창. 스
크롤 바를 장착. Run 버튼을 누를 때마다 내용을 새로 출력할 것. 가령
‘1_1_1.jpg’  C1
‘2_1_1.jpg’  C2
그리고 다수 파일이 인식할 경우 실행한 결과를 정리하여 총 입력한 파일 개수와 맞춘
개수, 그리고 이에 기반한 인식률을 계산하세요. 
8) ‘실행 결과 저장’ 을 누르면 보라색 화면의 내용을 txt 파일로 저장시킬 것. 
9) 위에서 상술한 기본 기능은 반드시 포함되어야 하며 그 외는 제작자의 자율에 맡김. 

---------------------------------------------------------------------------------------------
### 결과

![image](https://github.com/dev-learning1/Hand_gesture_recognizer_using_TKinter_numpy_and_python/assets/115637631/720c133b-e11b-4ad3-9fa9-764b4aebc2a0)



