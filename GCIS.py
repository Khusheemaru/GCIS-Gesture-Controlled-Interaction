import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import win32api

# Initialize MediaPipe hands module and drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class HandGestureControl:
    CLICK_THRESHOLD = 30
    DRAG_THRESHOLD = 30

    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
        self.is_dragging = False
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def draw_hand_landmarks(self, image, hand_landmarks):
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
        )

    def get_landmark_coordinates(self, hand_landmarks, landmark, image_width, image_height):
        normalized_landmark = hand_landmarks.landmark[landmark]
        return mp_drawing._normalized_to_pixel_coordinates(normalized_landmark.x, normalized_landmark.y, image_width, image_height)

    def handle_gestures(self, index_finger_tip, thumb_tip, middle_finger_tip, image_width, image_height):
        # Scale cursor position to screen size
        screen_width, screen_height = pyautogui.size()
        cursor_x = int(index_finger_tip[0] * screen_width / image_width)
        cursor_y = int(index_finger_tip[1] * screen_height / image_height)
        
        win32api.SetCursorPos((cursor_x, cursor_y))
        
        click_distance = np.sqrt((index_finger_tip[0] - thumb_tip[0]) ** 2 + (index_finger_tip[1] - thumb_tip[1]) ** 2)
        slide_distance = np.sqrt((thumb_tip[0] - middle_finger_tip[0]) ** 2 + (thumb_tip[1] - middle_finger_tip[1]) ** 2)
        
        if click_distance < self.CLICK_THRESHOLD:
            pyautogui.click(button='left')
        
        if slide_distance < self.DRAG_THRESHOLD and not self.is_dragging:
            pyautogui.mouseDown(button='left')
            self.is_dragging = True
        elif slide_distance >= self.DRAG_THRESHOLD and self.is_dragging:
            pyautogui.mouseUp(button='left')
            self.is_dragging = False

    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image_height, image_width, _ = image.shape
        results = self.hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image, image_width, image_height, results

    def run(self):
        while self.video.isOpened():
            success, frame = self.video.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image, image_width, image_height, results = self.process_frame(frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.draw_hand_landmarks(image, hand_landmarks)

                    try:
                        index_finger_tip = self.get_landmark_coordinates(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP, image_width, image_height)
                        thumb_tip = self.get_landmark_coordinates(hand_landmarks, mp_hands.HandLandmark.THUMB_TIP, image_width, image_height)
                        middle_finger_tip = self.get_landmark_coordinates(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, image_width, image_height)

                        if index_finger_tip and thumb_tip and middle_finger_tip:
                            self.handle_gestures(index_finger_tip, thumb_tip, middle_finger_tip, image_width, image_height)
                    
                    except Exception as e:
                        print(f"Error processing hand landmarks: {e}")

            cv2.imshow('Hand Gesture Control', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    control = HandGestureControl()
    control.run()