from tkinter import *   #tkinter(파이썬에서 GUI 관련 모듈을 제공해주는 표준 윈도 라이브러리) 사용
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import ImageTk, Image
#[출처]https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window (PIL 사용법)( May 28 '14 at 7:43 Answer : NorthCat)
from tkinter import filedialog
import tkinter.messagebox as message
from lsm import *

imglist=[None]*10
filename=[]#[None]*10
tmpfilename=[]
no=0
correct=0
data=""

window = Tk()   #윈도우창이 화면에 출력. 기본이 되는 윈도를 반환 => 루 트 윈도(Root Window) 또는 베이스 윈도(Base Window)

## 템플릿 등록 ##
def tamplet() :
    global filename
    
    filename = filedialog.askopenfilenames(parent=window, initialdir = "C:/Users/삼성컴퓨터/Desktop/로봇영상2018_1758010_도희정_과제5/Hand image1/11",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    ## 파일 10개 선택할 때 까지 반복 ##
    while(len(filename)!=10) :
        message.showerror("오류창","파일을 "+str(len(filename))+"개 선택했습니다.\n파일을 10개 선택해주세요.")
        filename = filedialog.askopenfilenames(parent=window, initialdir = "C:/Users/삼성컴퓨터/Desktop/로봇영상2018_1758010_도희정_과제5/Hand image1/11",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

    ## 10개의 이미지를 각 레이블에 나타내기 ##
    for num in range(len(filename)) :
        img = Image.open(str(filename[num]))
        size = (67, 67)
        img.thumbnail(size)
        imglist[num] = ImageTk.PhotoImage(img)#(Image.open('1_'+str(num+1)+'_2.jpg'))
        label1[num].configure(image = imglist[num])    #이미지 출력
        label1[num].image=imglist[num]

## 인시 파일 선택 ##
def tempfile() :
    global tmpfilename
    
    tmpfilename = filedialog.askopenfilenames(parent=window, initialdir = "C:/Users/삼성컴퓨터/Desktop/로봇영상2018_1758010_도희정_과제5/Hand image1",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    img = ImageTk.PhotoImage(Image.open(str(tmpfilename[0])))
        
    label2.configure(image = img)    #이미지 출력
    label2.image=img

## 템플릿 매칭(인식파일 하나씩) ##
def template_matching() :
    global no, err, correct, data
    error=[]
    err=[]

    ## 인식파일 이미지를 바꿈 ##
    img = ImageTk.PhotoImage(Image.open(str(tmpfilename[no])))
    label2.configure(image = img)    #이미지 출력
    label2.image=img

    ## 10개의 템플릿과 하나의 인식파일간의 오차률 저장 ##
    for file in filename :
        img=background(file)
        tmpimg=background(tmpfilename[no])
        error=abs(img.astype(float)-tmpimg.astype(float))   #절대값
        #print(error)
        e=0
        for er in error :
            for i in er :
                e=e+i
        #print(e)
        err+=[e]

    ## 오차들을 적는 부분 ##
    n=0
    errorbox.delete(1.0,(len(error)+1)*10.0)
    #[출처]https://076923.github.io/posts/Python-tkinter-18/(delete(), 2018-05-29  /  윤대희  )
    for er in err :
        errorbox.insert(END,"\nClass"+str(n+1)+":\n"+str(er)+'\n')
        n+=1 
    errorbox.pack(side='left', fill=BOTH)

    ## 오차가 제일 작은 클래스와 인식파일의 이미지가 같을 때 ##
    if [str(np.argmin(err)+1)] == [str(10)] : 
        if [str(0)] == list(tmpfilename[no][-7]) :
        #[출처]https://hashcode.co.kr/questions/1235/%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%84-%EC%B2%A0%EC%9E%90-%ED%95%98%EB%82%98%EC%94%A9-%EB%81%8A%EC%96%B4-list%EB%A1%9C-%EC%A0%80%EC%9E%A5%ED%95%98%EB%A0%A4-%ED%95%A9%EB%8B%88%EB%8B%A4((list(), 작성자 : 풀입 2016.02.23)
            correct+=1
            print(correct)
    if [str(np.argmin(err)+1)] == list(tmpfilename[no][-7]) :
    #[출처]https://hashcode.co.kr/questions/1235/%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%84-%EC%B2%A0%EC%9E%90-%ED%95%98%EB%82%98%EC%94%A9-%EB%81%8A%EC%96%B4-list%EB%A1%9C-%EC%A0%80%EC%9E%A5%ED%95%98%EB%A0%A4-%ED%95%A9%EB%8B%88%EB%8B%A4((list(), 작성자 : 풀입 2016.02.23)
        correct+=1
        print(correct)

    ## 오차가 제일 작은 클래스와 여러가지 정보를 적는 부분 ##
    if no==0 :
        conclusion.delete(1.0,END)
        data=""
            
    conclusion.insert(END,"\n인식파일 : "+str(tmpfilename[no][-12:])+\
                          "\nClass : "+"C"+str(np.argmin(err)+1)+\
                          "\n오차 최소값 : "+str(err[np.argmin(err)])+\
                          "\n인식파일 선택한 개수 : "+str(len(tmpfilename))+\
                          "\n남은 인식파일 수 : "+str(len(tmpfilename)-(no+1))+\
                          "\n맞은 개수 : "+str(correct)+"\n"
                          )
    data+="\n인식파일 : "+str(tmpfilename[no][-12:])+\
          "\nClass : "+"C"+str(np.argmin(err)+1)+\
          "\n오차 최소값 : "+str(err[np.argmin(err)])+\
          "\n인식파일 선택한 개수 : "+str(len(tmpfilename))+\
          "\n남은 인식파일 수 : "+str(len(tmpfilename)-(no+1))+\
          "\n맞은 개수 : "+str(correct)+"\n"
    no+=1
    if no==len(tmpfilename) :
        conclusion.insert(END,"\n인식률 : "+str((correct/len(tmpfilename))*100)+"%"+"\n")
        data+="\n인식률 : "+str((correct/len(tmpfilename))*100)+"%"+"\n"
    conclusion.pack(side='left', fill=BOTH)

    
    ## 인식파일이 마지막이 되었을 때 ##
    if no==len(tmpfilename) :
        message.showinfo("안내창","인식파일의 마지막 파일입니다.\n인식파일을 다시 선택해 주세요.")
        correct=0;no=0

def All_template_matching() :
    global no, err, correct, data
    no=0; correct=0; data=""
    while(1) :
        error=[]
        err=[]

        ## 인식파일 이미지를 바꿈 ##
        img = ImageTk.PhotoImage(Image.open(str(tmpfilename[no])))
        label2.configure(image = img)    #이미지 출력
        label2.image=img

        ## 10개의 템플릿과 하나의 인식파일간의 오차률 저장 ##
        for file in filename :
            print("file : ",file)
            print("tmpfile : ",tmpfilename[no])
            img=background(file)
            tmpimg=background(tmpfilename[no])
            error=abs(img-tmpimg)#abs(img.astype(float)-tmpimg.astype(float))   #절대값
            e=0
            for er in error :
                for i in er :
                    e=e+i
            err+=[e]

        ## 오차들을 적는 부분 ##
        n=0
        errorbox.delete(1.0,(len(error)+1)*10.0)
        #[출처]https://076923.github.io/posts/Python-tkinter-18/(delete(), 2018-05-29  /  윤대희  )
        for er in err :
            errorbox.insert(END,"\nClass"+str(n+1)+":\n"+str(er)+'\n')
            n+=1 
        errorbox.pack(side='left', fill=BOTH)

        ## 오차가 제일 작은 클래스와 인식파일의 이미지가 같을 때 ##
        if [str(np.argmin(err)+1)] == [str(10)] : 
            if [str(0)] == list(tmpfilename[no][-7]) :
        #[출처]https://hashcode.co.kr/questions/1235/%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%84-%EC%B2%A0%EC%9E%90-%ED%95%98%EB%82%98%EC%94%A9-%EB%81%8A%EC%96%B4-list%EB%A1%9C-%EC%A0%80%EC%9E%A5%ED%95%98%EB%A0%A4-%ED%95%A9%EB%8B%88%EB%8B%A4((list(), 작성자 : 풀입 2016.02.23)
                correct+=1
                print(correct)
        if [str(np.argmin(err)+1)] == list(tmpfilename[no][-7]) :
        #[출처]https://hashcode.co.kr/questions/1235/%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%84-%EC%B2%A0%EC%9E%90-%ED%95%98%EB%82%98%EC%94%A9-%EB%81%8A%EC%96%B4-list%EB%A1%9C-%EC%A0%80%EC%9E%A5%ED%95%98%EB%A0%A4-%ED%95%A9%EB%8B%88%EB%8B%A4((list(), 작성자 : 풀입 2016.02.23)
            correct+=1
            print(correct)

        ## 오차가 제일 작은 클래스와 여러가지 정보를 적는 부분 ##
        if no==0 :
            conclusion.delete(1.0,END)
            data=""
            
        conclusion.insert(END,"\n인식파일 : "+str(tmpfilename[no][-12:])+\
                          "\nClass : "+"C"+str(np.argmin(err)+1)+\
                          "\n오차 최소값 : "+str(err[np.argmin(err)])+\
                          "\n인식파일 선택한 개수 : "+str(len(tmpfilename))+\
                          "\n남은 인식파일 수 : "+str(len(tmpfilename)-(no+1))+\
                          "\n맞은 개수 : "+str(correct)+"\n"
                          )
        data+="\n인식파일 : "+str(tmpfilename[no][-12:])+\
              "\nClass : "+"C"+str(np.argmin(err)+1)+\
              "\n오차 최소값 : "+str(err[np.argmin(err)])+\
              "\n인식파일 선택한 개수 : "+str(len(tmpfilename))+\
              "\n남은 인식파일 수 : "+str(len(tmpfilename)-(no+1))+\
              "\n맞은 개수 : "+str(correct)+"\n"
        no+=1
        if no==len(tmpfilename) :
            conclusion.insert(END,"\n인식률 : "+str((correct/len(tmpfilename))*100)+"%"+"\n")
            data+="\n인식률 : "+str((correct/len(tmpfilename))*100)+"%"+"\n"
        conclusion.pack(side='left', fill=BOTH)

        ## 인식파일이 마지막이 되었을 때 ##
        if no==len(tmpfilename) :
            message.showinfo("안내창","인식파일의 마지막 파일입니다.\n인식파일을 다시 선택해 주세요.")
            correct=0;no=0
            break

## 결과 저장 ##      
def Logfile() :
    logfile = open("C:/Users/삼성컴퓨터/Desktop/로봇영상2018_1758010_도희정_과제5/Hand image1/Logfile",'w')
    logfile.write(data)
    logfile.close()

## window 창 닫기 ##
def Exit() :
    window.quit()    #중지
    window.destroy()    #창을 끈다


## 템플릿을 나타내는 레이블, 레이블 위치를 정해줄 틀 생성 ##
f1=Frame()
#[출처]https://blog.naver.com/agdgdy00/221023056333(Frame(),grid(),작성자:김순돈, 2017. 6. 6. 20:49 )
label1=[""]*10
COUNT=0

photo = PhotoImage()    #이미지 파일 준비
for i in range(10):
    label1[i]=Label(f1,image=photo)

for i in range(2) :    #리스트에서 한개씩 추출
    for j in range(5) :
        label1[COUNT].grid(row=i,column=j)   #오른쪽으로 리스트 출력
        COUNT+=1
f1.grid(row=0,column=0)

## 인식파일을 나타내는 레이블, 레이블 위치를 정해줄 틀 생성 ##
f2=Frame()
label2 = Label(f2,image=photo)
label2.grid(row=0,column=0)

## 템플릿 매칭을 실행 시킬 버튼, 버튼의 위치를 정해줄 틀 생성 ##
f4=Frame(f2)
button = Button(f4, text='RUN!',width=18,height=5,relief="solid",command = template_matching)   #버튼 생성
button.grid(row=0,column=0)

button = Button(f4, text='All\nRUN!',width=18,height=5,relief="solid",command = All_template_matching)   #버튼 생성
button.grid(row=1,column=0)
f4.grid(row=0,column=1)
f2.grid(row=1,column=0)

## 오차를 나타낼 스크롤바가 있는 창, 창 위치를 정해줄 틀 생성 ##
f3=Frame()
scrollbar=Scrollbar(f3)
scrollbar.pack(side="right", fill="y")
errorbox=Text(f3,yscrollcommand=scrollbar.set)
scrollbar.config(command=errorbox.yview)
#[출처]https://076923.github.io/posts/Python-tkinter-16/(스크롤바, 작성자 : YUN DAE HEE, 2018.05.26 )
#[출처] [파이썬 기초]python 스크롤바 생성예제|작성자 복쌤(Text(), 작성자 : 복쌤, 2015. 12. 30. 17:35)
f3.grid(row=0,column=1)

## 여러 정보를 나타낼 스크롤바가 있는 창, 창 위치를 정해줄 틀 생성 ##
f4=Frame()
scrollbar=Scrollbar(f4)
scrollbar.pack(side="right", fill="y")
conclusion=Text(f4,yscrollcommand=scrollbar.set)
scrollbar.config(command=conclusion.yview)
f4.grid(row=1,column=1)

## 메뉴창 생성 ##
mainMenu = Menu(window)    #Menu(부모윈도)로 변수생성
window.config(menu = mainMenu)    #생성한 메뉴 자체를 윈도창의 메뉴로 지정

fileMenu = Menu(mainMenu)    #Menu(부모윈도)로 변수생성
mainMenu.add_cascade(label = "파일", menu = fileMenu)    #상위 메뉴인 [파일]을 생성. 메뉴 자체에 부착
fileMenu.add_command(label = "템플릿 등록하기",command=tamplet)    #[파일]을 선택하고 그 아래에 다른 메뉴가 확장되어야함으로 하위 [열기] 메뉴 준비. [열기]메뉴는 선택할 때 어떤 작동을 함
fileMenu.add_command(label = "인식파일 불러오기",command=tempfile)    #하위메뉴 [종료] 메뉴 준비. [종료]메뉴는 선택할 때 어떤 작동을 함
fileMenu.add_command(label = "실행결과 저장",command=Logfile)    #하위메뉴 [종료] 메뉴 준비. [종료]메뉴는 선택할 때 어떤 작동을 함
fileMenu.add_command(label = "끝내기",command=Exit)    #하위메뉴 [종료] 메뉴 준비. [종료]메뉴는 선택할 때 어떤 작동을 함

window.mainloop()
