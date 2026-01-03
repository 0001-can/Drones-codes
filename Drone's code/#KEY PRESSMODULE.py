#KEY PRESSMODULE tuşlara basıldığında drone'un hareket etmesini sağlayan modül
from tello import Tello 
from time import sleep
import keyPresssModule as kp # keyPresssModule modülünü ekledik
kp.init() # keyPresssModule modülünü başlattık
me=tello.Tello() 
me.connect() 
print(me.get_battery())

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

    if kp.getKey("Z"):yv=me.land() # 'Z' tuşuna basıldığında drone iner
    if kp.getKey("H"): yv=me.takeoff() # 'H' tuşuna basıldığında drone uçar
    return[lr,fb,ud,yv] 


me.takeoff() # Drone'u havalandırdık
sleep(0.1) # 0.1 saniye bekledik

while True: 
    vals=getKeyboardInput() 
    me.send_rc_control(vals[0],vals[1],vals[2],vals[3]) 
    sleep(0.85)

