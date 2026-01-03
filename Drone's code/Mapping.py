#MAPPİNG drone haritalama modülü
# Bu modül, drone'un hareketlerini ve konumunu haritalamak için kullanılır
# Drone'un hareketlerini ve konumunu takip eder ve harita üzerinde gösterir
from djitellopy import tello 
import KEYPRESSMODULE as kp 
import numpy as np 
from time import sleep 
import cv2
import math
global aspeed
######PARAMETERS######
fSpeed=117/10 #ileri hız cm/sn (15cm/sn)
aSpeed=360/10 #açısal hız derece/sn (50 d/sn)
interval=0.25 #her döngüde bekleme süresi (0.25 saniye)

dInterval=fSpeed*interval #her döngüde ileri hareket mesafesi (cm)
aInterval=aSpeed*interval #her döngüde açısal hareket (derece /sn)
##############################



x,y=500,500 # başlangıç koordinatları (500,500) piksel
a=0 # başlangıç açısı 0 derece


kp.init() 
me=tello.Tello()
me.connect()
print(me.get_battery())

points=[(0,0),(0,0)] # başlangıç noktaları (0,0) piksel
points[0]=(x,y) # başlangıç noktasını (500,500) piksel olarak ayarlıyoruz



def getKeyboardInput():# tuşlara basıldığında drone'un hareket etmesini sağlayan fonksiyon
    lr,fb,ud,yv=0,0,0,0 # lr: left-right, fb: forward-backward, ud: up-down, yv: sapma hızı
    speed=15
    aspeed=50 # aspeed: açısal hız
    global x,y,yaw,a 
    d=0 
    if kp.getKey("left"): # sol tuşuna basıldığında drone sola hareket eder
        lr=-speed # sol hareket
        d=dInterval # ileri hareket
        a=-180 # 180 derece



    elif kp.getkey("right"): # sağ tuşuna basıldığında drone sağa hareket eder
        lr=speed # sağ hareket
        d=-dInterval # ileri hareket
        a=180 # 180 derece

    if kp.getKey("up"): # yukarı tuşuna basıldığında drone yukarı hareket eder
        fb=speed # ileri hareket
        d=dInterval # yukarı hareket
        a=270 # 270 derece
    elif kp.getKey("down"): # aşağı tuşuna basıldığında drone aşağı hareket eder
        fb=-speed # geri hareket
        d=-dInterval # aşağı hareket
        a=-90 # -90 derece
    
    if kp.getKey("w"): # 'W' tuşuna basıldığında drone yukarı hareket eder
        ud=speed # yukarı hareket
    elif kp.getKey("s"): # 'S' tuşuna basıldığında drone aşağı hareket eder
        ud=-speed # aşağı hareket

    if kp.getKey("a"): # 'A' tuşuna basıldığında drone sola sapar
        yv=-aSpeed # sola sapma
        yaw-= aInterval # açısal hareket
    elif kp.getKey("d"): # 'D' tuşuna basıldığında drone sağa sapar
        yv=-speed # sağa sapma
        yaw+= aInterval # açısal hareket

    if kp.getKey("Z"):yv=me.land();time.sleep(3) # 'Z' tuşuna basıldığında drone iner ve 3 saniye bekler
    if kp.getKey("H"): yv=me.takeoff() # 'H' tuşuna basıldığında drone uçar

    sleep(interval) 
    a+=yaw # açıyı güncelliyoruz
    x+=int(d*math.cos(math.radians(a))) # x koordinatını güncelliyoruz
    y+=int(d*math.sin(math.radians(a))) # y koordinatını güncelliyoruz

    if kp.getKey("z"): # 'z' tuşuna basıldığında görüntü kaydedilir
        cv2.imwrite(f"Resources/Images/{time.time()}.jpg",img) # img değişkenindeki görüntü kaydedilir


me.takeoff()

def drawPoints(img,points): # Harita üzerinde noktaları çizen fonksiyon
    for point in points: # Noktaları çiziyoruz
        cv2.circle(img,(point[0],point[1]),10,(0,0,255),cv2.FILLED) # Noktaları kırmızı renkte çiziyoruz
    cv2.circle(img,points[-1],13,(0,255,0),cv2.FILLED)
    cv2.putText(img,f"({(points[-1][0]-500)/100},{(points[-1][1]-500)/100})m",(points[-1][0]+10,points[-1][1]+30),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),1)# Koordinatları gösteriyoruz



while True: 
    vals=getKeyboardInput() 
    me.send_rc_control(vals[0],vals[1],vals[2],vals[3])# Drone'a kontrol sinyalleri gönderiyoruz

    img=np.zeros((1000,1000,3),np.uint8) # Boş bir görüntü oluşturuyoruz
    if (points[-1][0]!=vals[4] or points[-1][1]!=vals[5]):  # Eğer son nokta ile yeni nokta farklıysa
        points.append((x,y))# Yeni noktayı ekliyoruz
    drawPoints(img,points) # Harita üzerinde noktaları çiziyoruz
    cv2.imshow("Output",img) # Görüntüyü gösteriyoruz
    cv2.waitKey(1)
    
    

   

    


    
    