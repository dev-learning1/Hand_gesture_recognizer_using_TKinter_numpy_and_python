import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lin
import matplotlib.image as mpimg
#from cut import *

## 배경(그라데이션) 빼기 ##
def background(filename) :
    
    o_img=mpimg.imread(str(filename))   
    ## 정규화 ##
    img=np.round(((o_img-np.min(o_img))/(np.max(o_img)-np.min(o_img)))*255)
    w=np.where(img>=0)
    x=[]
    y=[]

    ## 원본 각 모서리를 크기가 30x30인 부분 추출 ##
    LU=np.where((w[0]<30)&(w[1]<30))
    x1,y1=np.meshgrid(w[1][LU],w[0][LU])
    x+=[x1[0]]
    y+=[y1.T[0]]
    box1=img[y1.T[0],x1[0]].reshape(30,30)
    RU=np.where((w[0]<30)&(w[1]>=170))
    x2,y2=np.meshgrid(w[1][RU],w[0][RU])
    x+=[x2[0]]
    y+=[y2.T[0]]
    box2=img[y2.T[0],x2[0]].reshape(30,30)
    LD=np.where((w[0]>=170)&(w[1]<30))
    x3,y3=np.meshgrid(w[1][LD],w[0][LD])
    x+=[x3[0]]
    y+=[y3.T[0]]
    box3=img[y3.T[0],x3[0]].reshape(30,30)
    RD=np.where((w[0]>=170)&(w[1]>=170))
    x4,y4=np.meshgrid(w[1][RD],w[0][RD])
    x+=[x4[0]]
    y+=[y4.T[0]]
    box4=img[y4.T[0],x4[0]].reshape(30,30)
    x=np.array(x).reshape(1,np.size(x))
    y=np.array(y).reshape(1,np.size(y))

    ## 추출한 각 모서리를 하나의 큰 박스로 만든다 ##
    box_u = np.concatenate((box1,box2), axis=1)    #가로로 두 행렬을 이어붙인다
    box_d = np.concatenate((box3,box4), axis=1)
    box = np.concatenate((box_u,box_d), axis=0)    #세로로 두 행렬을 이어붙인다
    
    ## 원본이미지의 좌표 ##
    tw=np.array([x[0],y[0],[1]*len(x[0])]).T  

    ## 그라데이션의 계수(s) ##
    br=box.reshape(np.size(box),1)
    s=lin.pinv(tw).dot(br)
    print(s)

    ## 그라데이션 빼기 ##
    iw=np.array([w[1],w[0],[1]*len(w[1])]).T
    z=iw.dot(s)
    z=z.reshape(np.shape(img))
    img1=o_img-z
    
    ## 정규화 ##
    img1=np.round(((img1-np.min(img1))/(np.max(img1)-np.min(img1)))*255)
    
    Binary(img1)
    return R_box1
'''
    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(o_img)
    plt.subplot(2,2,2)
    plt.imshow(img)
    plt.subplot(2,2,3)
    plt.imshow(img1)
    plt.subplot(2,2,4)
'''
def Weight_b(no) :
    global Wb_Sum
    Wb_Sum=0
    for i in range(no) :
        Wb_Sum=Wb_Sum+num[i]
    return Wb_Sum/np.size(img)

## 평균 ##
def Mean_b(no) :
    if Wb_Sum==0 :
        return 0
    Sum=0
    for i in range(no) :
        Sum = Sum + (i*num[i])
    return Sum/Wb_Sum

## 분산 ##
def Variance_b(no) :
    if Wb_Sum==0 :
        return 0
    Sum=0
    for i in range(no) :
        Sum = Sum + ((i-Mb[-1])**2 * num[i])
    return Sum/Wb_Sum

def Weight_f(no) :
    global Wf_Sum
    Wf_Sum=0
    for i in range(no,256) :
        Wf_Sum=Wf_Sum+num[i]
    return Wf_Sum/np.size(img)

## 평균 ##
def Mean_f(no) :
    if Wf_Sum==0 :
        return 0
    Sum=0
    for i in range(no,256) :
        Sum = Sum + (i*num[i])
    return Sum/Wf_Sum

## 분산 ##
def Variance_f(no) :
    if Wf_Sum==0 :
        return 0
    Sum=0
    for i in range(no,256) :
        Sum = Sum + ((i-Mf[-1])**2 * num[i])
    return Sum/Wf_Sum

## 내에서 클래스 분산 ##
## intra-class variance(최소화) ##
def WCV() :
    return Wb[-1]*Vb[-1] + Wf[-1]*Vf[-1]

## inter-class variance(최대화) ##
def BCV() :
    M=Wb[-1]*Mb[-1] + Wf[-1]*Mf[-1]
    return Wb[-1]*((Mb[-1]-M)**2) + Wf[-1]*((Mf[-1]-M)**2)

## 이진화 ##
def Binary(img1) :
    global img, num, Mf, Wb, Vb,Wf, Vf, Mb, B_box
    #img=mpimg.imread(str(img1))   
    img=img1
    num=[]
    Wb_Sum=0; Wb=[]; Mb=[]; Vb=[]
    Wf_Sum=0; Wf=[]; Mf=[]; Vf=[]
    Vw=[];  VB=[]

    ## 각 픽셀에 해당하는 개수 ##
    for i in range(256) :
        num += [np.size(np.where(img==i))/2]

    for no in range(256) :
        Wb+=[Weight_b(no)]
        Mb+=[Mean_b(no)]
        Vb+=[Variance_b(no)]
        Wf+=[Weight_f(no)]
        Mf+=[Mean_f(no)]
        Vf+=[Variance_f(no)]
        Vw+=[WCV()]
        VB+=[BCV()]

    num=np.array(num)
    num.reshape(1,np.size(num))

    ## 임계점 찾기 ##
    t=np.where(Vw==np.min(Vw))
    t1=np.array(t)
    B_box=np.zeros(np.shape(img))
    t_w=np.where(img<np.max(t)) 
    B_box[t_w[0],t_w[1]]=1
    PCA(t_w)
    #return B_box
    #plt.imshow(B_box,cmap='gray')
    

#plt.figure("PCA")
## PCA(고유치,고유벡터 이용) ##
def PCA(t_w) :
    global R_box, R_box1,R_box2,R_box3#,c#ze1#,BOX#,y2
    ## pca ##
    Z=np.array([t_w[0],t_w[1]])
    m=np.mean(Z,1)
    m=m[:,np.newaxis]
    z=Z-m
    nn=z.shape[1]
    C=z.dot(z.T)/nn
    L,v=np.linalg.eig(C)
    c=np.argsort(L)
    v=np.vstack((v[:,np.max(c)],v[:,np.min(c)]))
    y=v.dot(Z)
    
    if(np.where(y[0]<0)) :
        y[0]=(y[0]-np.min(y[0])).astype(int)
    if(np.where(y[1]<0)) :
        y[1]=(y[1]-np.min(y[1])).astype(int)
    y=y.astype(int)
    print(y)
    R_box=np.zeros((np.max(y[1])+1,np.max(y[0])+1))
    R_box[y[1],y[0]]=1

    ## 보간 => 좌우에 1이 있으면 채운다 ##
    e=np.where(R_box==0)
    e=np.array(e).astype(int)
    num=0
    while(1) :
        a=e[1][num]-1
        b=e[1][num]+1
        c=e[0][num]
        if a < 0 :
            a=0
        if b>np.max(y[0]) :
            b=np.max(y[0])
        if (R_box[c,a]==1) & (R_box[c,b]==1) :
            R_box[e[0][num],e[1][num]]=1  
        num+=1
        if num==len(e[0]) :
            break

    ## 스케일링 ##
    ze=np.where(R_box)
    ze=np.array([ze[0],ze[1]])
    q=np.array([[200/(np.max(y[1])-np.min(y[1])),0],[0,200/(np.max(y[0])-np.min(y[0]))]])
    y1=q.dot(ze).astype(int)
    print(np.max(y1[0]),np.max(y1[1]))
    R_box1=np.zeros((201,201))
    R_box1[y1[0],y1[1]]=1

    ## 후진 사상 보간 ##
    ze1=np.where(R_box1==0)
    ze1=np.array([ze1[0],ze1[1]])
    y2=lin.inv(q).dot(ze1).astype(int)
    R_box1[ze1[0],ze1[1]]=R_box[y2[0],y2[1]]
'''
    ## 손목 자르기 ##
    o_w=np.where(R_box1==1)
    distance=[]
    for i in range(np.max(o_w[0])):
        a=np.where(o_w[0]==i)
        b=o_w[1][a]
        for j in range(len(b)) :
            if b[j]+1 not in b :
                distance+=[b[j]-b[0]]
                break
    distance=np.array(distance)
    c=np.where(distance==np.max(distance))
    c=(c[0][0]+c[0][-1])/2
    c=c.astype(int)
    print(distance)
    print(np.max(distance))
    print(c)
    d=c+(np.max(distance)/2)
    print(d)
    o_y=np.where(o_w[0]<=d)
    O_W=np.array([o_w[0][o_y],o_w[1][o_y]])
    R_box2=np.zeros((np.max(O_W[0])+1,np.max(O_W[1])+1))
    R_box2[O_W[0],O_W[1]]=1

    ## 스케일링 ##
    ze=np.where(R_box2)
    ze=np.array([ze[0],ze[1]])
    q=np.array([[200/(np.max(O_W[0])-np.min(O_W[0])),0],[0,200/(np.max(O_W[1])-np.min(O_W[1]))]])
    y1=q.dot(ze).astype(int)
    print(np.max(y1[0]),np.max(y1[1]))
    R_box3=np.zeros((201,201))
    R_box3[y1[0],y1[1]]=1
    

    ## 후진 사상 보간 ##
    ze1=np.where(R_box3==0)
    ze1=np.array([ze1[0],ze1[1]])
    y2=lin.inv(q).dot(ze1).astype(int)
    R_box3[ze1[0],ze1[1]]=R_box2[y2[0],y2[1]]
'''

