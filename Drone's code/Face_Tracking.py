#Face_Tracking yüz takip modülü
import cv2 # OpenCV kütüphanesini ekledik
import numpy as np # numpy kütüphanesini ekledik bu iki kütüphane görüntü işleme için kullanılır
from tello.py import tello 
me=tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 0, 0) # Drone'u sabit tutmak için başlangıçta kontrol sinyalleri gönderiyoruz
time.sleep(2.2)



w, h = 640, 240  # Video karesinin genişliği ve yüksekliği
fbRange=[6200,6800]  # Yüz tespiti için aralık
pid=[0.4,0.4,0]  # Drone'u kontrol etmek için PID değerleri
pError=0 

def findFace(img): # Yüz tespiti fonksiyonu
    faceCascade= cvC2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml") # Yüz tespiti için Haar Cascade sınıflandırıcısını kullanıyoruz
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # Görüntüyü gri tonlamaya çeviriyoruz
    faces=faceCascade.detectMultiScale(imgGray,1.2,8) # Yüzleri tespit ediyoruz

    myFaceListC=[] # Yüz merkezlerini tutmak için liste
    myFaceListArea=[] # Yüz alanlarını tutmak için liste

    for (x,y,w,h) in faces: # Tespit edilen yüzlerin koordinatlarını alıyoruz
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) # Yüz etrafına dikdörtgen çiziyoruz
        cx=x+w//2 # Yüzün merkez koordinatını hesaplıyoruz
        cy=y+h//2 # Yüzün merkez koordinatını hesaplıyoruz
        area= w*h # Yüzün alanını hesaplıyoruz
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED) # Yüz merkezine daire çiziyoruz
        myFaceListC.append([cx,cy]) # Yüz merkezlerini listeye ekliyoruz
        myFaceListArea.append(area) # Yüz alanlarını listeye ekliyoruz
    if len(myFaceListArea) != 0: # Eğer yüz tespit edildiyse
        i=myFaceListArea.index(max(myFaceListArea)) # En büyük yüz alanını buluyoruz
        return img,[myFaceListC[i],myFaceListArea[i]] # Yüz merkezini ve alanını döndürüyoruz
        return img, [[0,0], 0] # Eğer yüz tespit edilmediyse, merkez koordinatını (0,0) ve alanı 0 olarak döndürüyoruz
        

def trackFace(info,w,pid,pError): # Yüz takip fonksiyonu
    area=info[1] # Yüz alanını alıyoruz
    x, y=info[0] # Yüz merkez koordinatlarını alıyoruz
    fb=0 # İleri-geri hareket için başlangıç değeri
    error= x-w//2 # Yüz merkezinin ekranın ortasından ne kadar uzak olduğunu hesaplıyoruz
    speed=pid[0]*error + pid[1]*(error-pError) # PID kontrolü ile hız hesaplıyoruz
    speed= int(np.clip(speed,-100,100)) # Hızı -100 ile 100 arasında sınırlıyoruz
    if area>fbRange[0] and area < fbRange[1]: # Eğer yüz alanı belirli bir aralıkta ise
        fb=0
    elif area> fbRange[1]: # Eğer yüz alanı belirli bir aralıktan büyükse
        fb=-20
    elif area < fbRange[0] and area != 0:  # Eğer yüz alanı belirli bir aralıktan küçükse
        fb=20

    if x==0: # Eğer yüz tespit edilmediyse
        speed=0
        error=0


    me.send_rc_control(0, fb, 0, speed) # Drone'a kontrol sinyalleri gönderiyoruz
    return error # Hata değerini döndürüyoruz, böylece bir sonraki döngüde kullanılabilir




while True:   # _, img=cap.read() # Video akışından kare alıyoruz
  
    img=me.get_frame_read().frame # Drone'un kamerasından görüntü alıyoruz
    img=cv2.resize(img, (w, h)) # Görüntüyü yeniden boyutlandırıyoruz
    img,info =findFace(img) # Yüz tespit ediyoruz
    pError=trackFace(info,w,pid,pError) # Yüzü takip ediyoruz
    cv2.imshow("Output",img) # Görüntüyü gösteriyoruz
    if cv2.waitKey(1) & 0xFF == ord('q'): # 'q' tuşuna basılırsa döngüden çıkıyoruz
       me.land() 
       break
