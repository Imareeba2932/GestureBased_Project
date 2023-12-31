import cv2
#to detect landmark
import mediapipe as mp
#to control the keyboard
import pyautogui
#to calculate the time
import time 
#to calculate the distance between the landmarks
def count_fingers(lst):
    cnt=0
    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt+=1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt+=1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt+=1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt+=1
    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 5:
        cnt+=1

    return cnt 

#to capture the video
cap=cv2.VideoCapture(1)

#for drawing the keypoints of the hands on the frame
drawing= mp.solutions.drawing_utils
#hands reference
hands = mp.solutions.hands
#no. of hands to be detected
hands_obj = hands.Hands(max_num_hands=1)
#to check if the gesture is performed or not
start_init = False
#to calculate the time
prev = -1

while True:
    end_time = time.time()
    _, frm = cap.read()

    frm = cv2.flip(frm,1)

    #converting the frame to RGB
    res = hands_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]

        cnt = count_fingers(hand_keyPoints)
        if prev != cnt:
            if not(start_init):
                start_time=time.time()
                start_init = True
            elif (end_time - start_time) > 0.2:
                if (cnt ==1):
                    pyautogui.press('right')
                elif (cnt ==2):
                    pyautogui.press('left')
                elif (cnt ==3):
                    pyautogui.press('up')
                elif (cnt ==4):
                    pyautogui.press('down')
                elif (cnt ==5):
                    pyautogui.press('space')

                prev = cnt
                start_init = False

        drawing.draw_landmarks(frm, res.multi_hand_landmarks[0], hands.HAND_CONNECTIONS)

    
    cv2.imshow("window",frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
