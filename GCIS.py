import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
import win32api
import pyautogui

#used to draw lines and dots on hand
mp_drawing = mp.solutions.drawing_utils

#used to get all info about hand co-ordinates
mp_hands = mp.solutions.hands

#take input from webcam using opencv
video = cv2.VideoCapture(0)

#sensitivity of detection and tracking
with mp_hands.Hands(min_detection_confidence = 0.8,min_tracking_confidence = 0.5) as hands:
    is_dragging = False
    
    while video.isOpened():
        _,frame = video.read() #read method to read data first is signal and second is frame

        #opencv takes input in bgr format, mediapipe in rgb
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image = cv2.flip(image,1)

        image_height,image_width,_ = image.shape

        #get hand co-ordinates
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

            for hand_landmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalized_landmark = hand_landmarks.landmark[point]
                    pixel_coordinates_landmark = mp_drawing._normalized_to_pixel_coordinates(
                        normalized_landmark.x, normalized_landmark.y, image_width, image_height
                    )

                    if point == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                        try:
                            cv2.circle(image, (pixel_coordinates_landmark[0], pixel_coordinates_landmark[1]), 25, (0, 200, 0), 5)
                            index_finger_tip_x = pixel_coordinates_landmark[0]
                            index_finger_tip_y = pixel_coordinates_landmark[1]

                            # Scale cursor position to screen size
                            screen_width, screen_height = pyautogui.size()
                            cursor_x = int(index_finger_tip_x * screen_width / image_width)
                            cursor_y = int(index_finger_tip_y * screen_height / image_height)

                            win32api.SetCursorPos((cursor_x, cursor_y))

                            # Detect proximity to thumb tip for click
                            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                            thumb_tip_x, thumb_tip_y = int(thumb_tip.x * image_width), int(thumb_tip.y * image_height)
                            click_distance = np.sqrt((index_finger_tip_x - thumb_tip_x) ** 2 + (index_finger_tip_y - thumb_tip_y) ** 2)

                            # Detect proximity to middle finger tip for slide
                            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                            middle_finger_tip_x, middle_finger_tip_y = int(middle_finger_tip.x * image_width), int(middle_finger_tip.y * image_height)
                            slide_distance = np.sqrt((thumb_tip_x - middle_finger_tip_x) ** 2 + (thumb_tip_y - middle_finger_tip_y) ** 2)

                            # Click if the distance is below the threshold
                            if click_distance < 30:  # Threshold value for click
                                pyautogui.click(button='left')

                            # Start drag if thumb and middle finger tips are close
                            if slide_distance < 30 and not is_dragging:  # Threshold value for slide
                                pyautogui.mouseDown(button='left')
                                is_dragging = True

                            # End drag if thumb and middle finger tips are not close
                            if slide_distance >= 30 and is_dragging:
                                pyautogui.mouseUp(button='left')
                                is_dragging = False

                        except Exception as e:
                            print(f"Error: {e}")

        cv2.imshow('game', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()