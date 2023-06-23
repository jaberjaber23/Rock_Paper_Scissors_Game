import cv2
import cvzone
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import time 
import random       

screen_width, screen_height = pyautogui.size()


cap =  cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0,0] # [AI, Player]


while True:
    imgBG = cv2.imread("Resources/BG.png")
    imgBG = cv2.resize(imgBG, (screen_width, screen_height))
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgScaled = cv2.resize(img, (0,0), None, 0.848, 0.848)
    imgScaled = imgScaled[:,70:460]
    playerMove = None

    hands, img = detector.findHands(imgScaled, flipType=False)#,, flipType=False  

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (915,629), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

        if timer > 3:
            stateResult = True
            timer = 0

            
            if hands:
                
                hand = hands[0]
                fingers = detector.fingersUp(hand)

                if fingers == [0,0,0,0,0]: # rock
                    playerMove = 1
                if fingers == [1,0,0,0,0]: # rock
                    playerMove = 1
                if fingers == [0,0,0,0,1]: # rock
                    playerMove = 1
                if fingers == [1,1,1,1,1]: #paperss
                    playerMove = 2
                if fingers == [1,1,1,1,0]: #paperss
                    playerMove = 2
                if fingers == [0,1,1,1,1]: #paperss
                    playerMove = 2
                if fingers == [0,1,1,0,0]: # scissor
                    playerMove = 3
                if fingers == [1,1,1,0,0]: # scissor
                    playerMove = 3
                if fingers == [0,0,1,1,1]: # scissor
                    playerMove = 3
                if fingers == [0,0,0,1,1]: # scissor
                    playerMove = 3


                randomNumber = random.randint(1,3)


                imgAI = cv2.imread(f"Resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (520,480))


                #player wins
                if (playerMove == 1 and randomNumber == 3) or \
                   (playerMove == 2 and randomNumber == 1) or \
                   (playerMove == 3 and randomNumber == 2):
                    scores[1] +=1

                # AI wins
                if (playerMove == 3 and randomNumber == 1) or \
                   (playerMove == 1 and randomNumber == 2) or \
                   (playerMove == 2 and randomNumber == 3):
                    scores[0] +=1
                

                print(playerMove)



    imgBG[380: 787,1075: 1465] = imgScaled
    #380: 787,1075: 1465

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (520,480))

    cv2.putText(imgBG, str(scores[0]), (510,243), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 6)
    cv2.putText(imgBG, str(scores[1]), (1312,243), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 6)


    #cv2.imshow('Image', img)
    cv2.imshow('BG', imgBG)
    #cv2.imshow('Scaled', imgScaled)


    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime  = time.time()
        stateResult = False
