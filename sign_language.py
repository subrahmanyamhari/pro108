import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips =[8, 12, 16, 20]
thumb_tip= 4
status=""
tone=(0,0,0)

while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    results = hands.process(img)
    cv2.putText(img, status, (20, 300), cv2.FONT_HERSHEY_COMPLEX, 2, tone)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            #accessing the landmarks by their position
            lm_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

            #Code goes here
            for tip in finger_tips:
                x ,y= int(lm_list[tip].x*w),int(lm_list[tip].y*h)
                cv2.circle(img, (x,y), 15, (255.0,0), cv2.FILLED)
                if int(lm_list[tip].x*w)>int(lm_list[tip-2].x*w):
                    if int(lm_list[4].y * h) > int(lm_list[17].x * w):
                        status="dislike"
                        tone=(0,0,255)
                    if int(lm_list[4].y * h) < int(lm_list[17].x * w):
                        status="like"
                        tone = (255, 255, 0)
                else:
                    tone=(0,0,0)
                    status=""
            mp_draw.draw_landmarks(img, hand_landmark,
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),
            mp_draw.DrawingSpec((0,255,0),4,2))
    

    cv2.imshow("hand tracking", img)
    cv2.waitKey(1)