import mediapipe
import cv2

medhands=mediapipe.solutions.hands
draw=mediapipe.solutions.drawing_utils

hand=medhands.Hands(max_num_hands=1)

cap=cv2.VideoCapture(0)
while True:
    sucess,img=cap.read()
    img=cv2.flip(img,1)
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=hand.process(imgrgb)

    cv2.rectangle(img,(20,350),(90,440),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(20,350),(90,440),(0,0,255),thickness=8)


    tipids=[4,8,12,16,20]
    lmlist=[]
    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                #print(id,lm)
                cx=lm.x
                cy=lm.y
                lmlist.append([id,cx,cy])
                #print(lmlist)

                if len(lmlist)!=0 and len(lmlist)==21:

                    fingerlist=[]

                    #thumb

                    if lmlist[12][1]>lmlist[20][1]:
                        if lmlist[tipids[0]][1]>lmlist[tipids[0]-1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    else:
                        if lmlist[tipids[0]][1]<lmlist[tipids[0]-1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)       

                    #other fingers

        
                    for i in range(1,5):                                 
                        if lmlist[tipids[i]][2]<lmlist[tipids[i]-2][2]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                    print(fingerlist)


                    if len(fingerlist)!=0:
                        fingercount=fingerlist.count(1)  

                    cv2.putText(img,str(fingercount),(25,430),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),5)          


            draw.draw_landmarks(img,handlms,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(230,123,12),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2))
    cv2.imshow('Hand',img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
