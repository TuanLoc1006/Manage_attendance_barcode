file_open = open('fileQRcode.txt','a')

import cv2 
from pyzbar.pyzbar import decode
import numpy as np 

cam = cv2.VideoCapture(0)
while True:
    ok, frame = cam.read()
    
    for code in decode(frame):
       
        pts = np.array([code.polygon], np.int32)
        pts = pts.reshape(((-1,1,2)))
        cv2.polylines(frame, [pts], True, (0,0,255), 3)

    cv2.imshow('my frame QR',frame)
    key_pressed = cv2.waitKey((1))
    if key_pressed == 13:
        data = code.data.decode('utf-8')
        print(data)
        file_open.write(data + "\n")	
    # q ma assci la 113
    if  key_pressed == 113:
        break


file_open.close()
# giai phong bo nho camera
cam.release()
# dong het tat ca window
cv2.destroyAllWindows()

