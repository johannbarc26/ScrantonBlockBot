from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from gpiozero import LED
from time import sleep
from picamera2 import Picamera2

#RASPBERRY PI PINS
led1 = LED(17)   ## WIRED TO MICROBIT PIN 0 -> RMF
led2 = LED(27)   ## WIRED TO MICROBIT PIN 1 -> RMR
led3 = LED(23)   ## WIRED TO MICROBIT PIN 14 -> LMF
led4 = LED(24)   ## WIRED TO MICROBIT PIN 15 -> LMR

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
picam2.start()
time.sleep(2)
picam2.capture_file("moving.jpg")
image_array = picam2.capture_array()
picam2.stop()

Filename = "moving.jpg" # this part is for detecting a red block
img = Image.open(Filename)
img=img.rotate(180)
img_array=np.array(img)
for j in range(5):
    Aplot,Bplot,Cplot,Dplot,Eplot = [],[],[],[],[]
    H = 1070 - j*100
    for i in range(1920): # this loop can be changed to detect other colors
        Aplot.append(img_array[H,i,0])
        Bplot.append(255-img_array[H,i,1])
        Cplot.append(255-img_array[H,i,2])
        Dplot.append(Aplot[i]*Bplot[i]*Cplot[i])
    for i in range(2,1915):
        N = (Dplot[i] + Dplot[i+1])/2
        NN = (Dplot[i+3] + Dplot[i+4])/2
        Eplot.append(NN-N)
    #plt.plot(Aplot)
    #plt.plot(Bplot)
    #plt.plot(Cplot)
    #plt.plot(Dplot)
    #x1 = plt.plot(Eplot)
    #plt.show(x1)
    print(max(Eplot))
    print(min(Eplot))
    if max(Eplot) > 1200000 and min(Eplot) < -1200000:
        Emax = Eplot.index(max(Eplot))
        Emin = Eplot.index(min(Eplot))
        Eavg = math.floor((Emax+Emin)/2)
        print(Eavg)

Aplot,Bplot,Cplot,Dplot,Eplot = [],[],[],[],[] # second raster line to get the distance to the object
for i in range(1080):
    j = 1079-i
    Aplot.append(img_array[j,Eavg,0])
    Bplot.append(255-img_array[j,Eavg,1])
    Cplot.append(255-img_array[j,Eavg,2])
    Dplot.append(Aplot[i]*Bplot[i]*Cplot[i])
for i in range(2,1075):
    N = (Dplot[i] + Dplot[i+1])/2
    NN = (Dplot[i+3] + Dplot[i+4])/2
    Eplot.append(NN-N)
#x2 = plt.plot(Eplot)
#plt.show(x2)

Distance = Eplot.index(max(Eplot))
End = Eplot.index(min(Eplot))
Size = End-Distance
print(Distance)
print(Size)
if Distance < 210:
    print("move 20 cm")
    led1.on()
    led3.on()
    sleep(1.38)
    led1.off()
    led3.off()
    sleep(20)
if 211 < Distance < 315:
    print("move 30 cm")
    led1.on()
    led3.on()
    sleep(1.76)
    led1.off()
    led3.off()
    sleep(20)
if 316 < Distance < 370:
    print("move 40 cm")
    led1.on()
    led3.on()
    sleep(2.22)
    led1.off()
    led3.off()
    sleep(20)
if 371 < Distance < 400:
    print("move 50 cm")
    led1.on()
    led3.on()
    sleep(2.99)
    led1.off()
    led3.off()
    sleep(20)
if 401 < Distance:
    print("move >50 cm")
    led1.on()
    led3.on()
    sleep(1)
    led1.off()
    led3.off()
    sleep(20)
