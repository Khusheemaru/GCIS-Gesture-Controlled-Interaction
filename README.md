# Gesture-Controlled Interaction System (GCIS)

The Gesture-Controlled Interaction System (GCIS) is an advanced solution designed to enable seamless human-computer interaction using hand gestures. Leveraging MediaPipe for real-time hand tracking and gesture recognition, GCIS allows users to control the cursor and perform mouse actions, making it ideal for gaming, accessibility, and interactive presentations.




## Features

- Real-Time Hand Tracking: Uses MediaPipe to detect and track hand landmarks with high accuracy.
- Gesture-Based Cursor Control: Maps hand movements to control the cursor position on the screen.
- Click and Drag Actions: Implements gestures for mouse click and drag operations.
- Customizable Sensitivity: Allows adjustment of detection and tracking sensitivity.



## Applications

- Gaming: Play online games using hand gestures for a more immersive experience.
- Accessibility: Provides an alternative input method for users with limited mobility.
- Interactive Presentations: Control presentation slides and annotations with hand movements.
## Installation

Clone the repository:

```bash
git clone https://github.com/Khusheemaru/GCIS-Gesture-Controlled-Interaction.git
cd GCIS

```
Additional Requirements:

OpenCV: For capturing video from the webcam.
MediaPipe: For hand tracking and gesture recognition.
pyautogui: For simulating mouse actions.
pywin32: For controlling the cursor position on Windows.
You can install these packages using:

```bash
pip install opencv-python mediapipe pyautogui pywin32
```


## Usage/Examples


Control the cursor:

- Move your index finger to move the cursor.
- Touch the thumb tip with the index finger tip to click.
- Touch the thumb tip with the middle finger tip to drag.
Exit:

Press 'q' to exit the program.
