
# IMAGE CAPTURE & FPS DISPLAY #hem görüntü yakalama hem de FPS gösterimi
from tello.py import tello  # Kendi tello dosyanız
from djitellopy import Tello 
import cv2 
import time 

# Tello bağlantısı
me = tello.Tello()
me.connect()
print(f"Batarya Durumu: {me.get_battery()}%")

me.streamon() 

# FPS ölçümü için başlangıç zamanı
prev_time = 0

while True:
    # Görüntü al
    img = me.get_frame_read().frame
    img = cv2.resize(img, (368, 248))
    img = cv2.flip(img, 1)

    # FPS hesapla
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # FPS yazısı
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Görüntüyü göster
    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF

    # 's' tuşu: Görüntü kaydet
    if key == ord('s'):
        filename = f"tello_capture_{int(time.time())}.jpg"
        cv2.imwrite(filename, img)
        print(f"Görüntü kaydedildi: {filename}")

    # 'q' tuşu: Çıkış
    elif key == ord('q'):
        print("Çıkış yapılıyor...")
        break

# Pencereyi kapat
cv2.destroyAllWindows()
# Burada fps hesaplaması ve görüntü yakalama işlemi yapıldı. ayrıca 's' tuşuna basılınca görüntü kaydedilir.
