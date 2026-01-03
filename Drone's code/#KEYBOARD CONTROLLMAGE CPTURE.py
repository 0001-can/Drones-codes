#KEYBOARD CONTROLLMAGE CPTURE bunu klavye kontrolü ile görüntü yakalama modülü olarak kullanacağız
from djitellopy import tello 
import KEYPRESSMODULE as kp 
import cv2 
kp.init() # klavye modülünü başlattık
me=tello.Tello()
me.connect()
print(me.get_battery())
global img # img değişkenini global olarak tanımladık

def getKeyboardInput(): # tuşlara basıldığında drone'un hareket etmesini sağlayan fonksiyon
    lr,fb,ud,yv=0,0,0,0 # lr: left-right, fb: forward-backward, ud: up-down, yv: sapma hızı
    speed=50 
    if kp.getKey("LEFT"):lr=-speed # sol tuşuna basıldığında drone sola hareket eder
    elif kp.getkey("RİGHT"):lr=speed # sağ tuşuna basıldığında drone sağa hareket eder

    if kp.getKey("UP"):fb=speed # yukarı tuşuna basıldığında drone yukarı hareket eder
    elif kp.getKey("DOWN"):fb=-speed # aşağı tuşuna basıldığında drone aşağı hareket eder
    
    if kp.getKey("W"):ud=speed # 'W' tuşuna basıldığında drone yukarı hareket eder
    elif kp.getKey("s"):ud=-speed # 'S' tuşuna basıldığında drone aşağı hareket eder  

    if kp.getKey("A"):yv=speed # 'A' tuşuna basıldığında drone sola sapar
    elif kp.getKey("D"):yv=-speed # 'D' tuşuna basıldığında drone sağa sapar

    if kp.getKey("Z"):yv=me.land();time.sleep(3) # 'Z' tuşuna basıldığında drone iner ve 3 saniye bekler
    if kp.getKey("H"): yv=me.takeoff() # 'H' tuşuna basıldığında drone uçar

    if kp.getKey("z"): # 'z' tuşuna basıldığında görüntü kaydedilir
        cv2.imwrite(f"Resources/Images/{time.time()}.jpg",img)  # img değişkenindeki görüntü kaydedilir
    return[lr,fb,ud,yv] 


me.takeoff() 

while True: # Drone'u havalandırdık
    vals=getKeyboardInput() 
    me.send_rc_control(vals[0],vals[1],vals[2],vals[3]) # Drone'a kontrol sinyalleri gönderilir
    img=me.get_frame_read().frame # Drone'un kamerasından görüntü alınır
    img=cv2.resize(img,(360,240))   # Görüntü boyutu ayarlanır
    cv2.imshow("Image",img) # Görüntü gösterilir
    cv2.waitKey(1) 
     
    sleep(0.85)

