import cv2
import numpy as np

i = 0
count = 0
cap = cv2.VideoCapture('video3.mp4')
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while cap.isOpened():

    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    points = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        #print(count)
        if cv2.contourArea(contour) < 8000:
            continue

        cisla = []
        cislo = -10
        while (cislo <= 100):
            cisla.append(cislo)
            cislo = cislo + 1
        bool = 1
        for point in points:
            for cislo in cisla:
               for cislo2 in cisla:
                    if (x+cislo,y+cislo2) == point:
                     bool = 0
        if bool==1:
            points.append((x+100,y+100))




    for point in points:
        cv2.circle(frame1,(point),250,(255,0,0),2)
        for point2 in points:

            if point != point2:
                if (round((abs((abs(abs(point.__getitem__(0))-abs(point2.__getitem__(0))))/abs(abs(point.__getitem__(1))+abs(point2.__getitem__(1)))))*3,2))>1:
                    cv2.putText(frame1, str('dobry'), (int((point.__getitem__(0)+point2.__getitem__(0))/2),int((point.__getitem__(1)+point2.__getitem__(1))/2)), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
                    cv2.line(frame1,(point),(point2),(0,255,0),2)
                else:
                    cv2.putText(frame1,str('spatny'), (int((point.__getitem__(0)+point2.__getitem__(0))/2),int((point.__getitem__(1)+point2.__getitem__(1))/2)), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2)
                    cv2.line(frame1,(point),(point2),(0,0,255),2)
        count = count + 1
        print((point.__getitem__(0)-point2.__getitem__(0))/(point.__getitem__(1)+point2.__getitem__(1)))


        #cv2.rectangle(frame1, (x-(w), y-30), (x+(w*2), y+(h+60)), (255, 0, 0), 2)



    cv2.drawContours(frame1, contours, -1, (0, 0, 255), 2)

    image = cv2.resize(frame1, (1280,720))
    out.write(image)
    cv2.imshow("SMAP", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    cv2.putText(frame2, 'Pocet lidi: '+str(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 0, 0), 2)
    count = 0
    points.clear()
    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()