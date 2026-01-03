#KEYBOARD CONTROL 
import pygame #  kontroller için pygame kütüphanesini ekledik

def init(): # pygame'i başlatmak için init fonksiyonunu tanımladık
    pygame.init()
    win=pygame.display.set_mode((400,400))# Pygame penceresini oluşturduk 

def getKey(keyName): # Tuşa basılıp basılmadığını kontrol eden fonksiyon
    ans= False 
    for eve in pygame.get():pass # Pygame olaylarını kontrol ettik
    keyInput=pygame.key.get_pressed() # Tuşlara basılıp basılmadığını kontrol ettik
    myKey=getattr(pygame,"K_{}".format(keyName)) # Tuş adını pygame modülünden aldık
    if keyInput[myKey]: 
        ans=True
    pygame.display.update() # Pygame penceresini güncelledik
    return ans 

def main(): 
    if (getKey("LEFT")): 
        print("Left key pressed")
    if (getKey("RIGHT")):
        print("Right key pressed")
        

if __name__=='__main__': 
    init()
    while True:
        main()
# Burada pygame kütüphanesini kullanarak tuşlara basılıp basılmadığını kontrol eden bir modül oluşturduk.
# Bu modül, drone'un hareket etmesini sağlayacak.

