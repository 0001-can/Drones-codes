#BASİC MONEMENTS
#temel hareketler

from tello.py import tello 
from time import sleep # tello kütüphanesini ekledik ve zaman modülünden sleep fonksiyonunu ekledik
import cv2
from djitellopy import Tello # tello modülünden Tello sınıfını ekledik


me=tello.Tello() # tello modülünden Tello sınıfını me olarak tanımladık
me.connect()    # Tello ile bağlantı kurduk
print(me.get_battery()) # Drone'un pil seviyesini yazdırdık
me.takeoff()  # Drone'u havalandırdık
sleep(5)  # 5 saniye bekledik
me.land()  # Drone'u indirdik
me.streamon()  # Video akışını başlattık
while True:
    frame = me.get_frame_read().frame
    cv2.imshow("Drone", frame)

    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'): #'q ' tuşuna basılırsa drone'un video akışını durdurur ve döngüden çıkar
        sleep(2)  # 2 saniye bekledik
        me.streamoff()
        break

cv2.destroyAllWindows() # Video akışını durdurduk ve tüm pencereleri kapattık
