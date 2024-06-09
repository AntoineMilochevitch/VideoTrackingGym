### README

# Sport Video Tracking System

## Description

This project is a video tracking system for sports, utilizing stereo cameras to track athletes' movements in real-time. Camera calibration is an essential step to ensure optimal tracking accuracy.

## Features

- **Real-Time Tracking**: Precise tracking of athletes during sports sessions.
- **Camera Calibration**: Uses a chessboard pattern to calibrate stereo cameras.
- **User-Friendly Interface**: Instructions and visual feedback to facilitate usage.
- **Movement Analysis**: Tools to analyze athletes' movements.

## Prerequisites

- Python 3.x
- OpenCV
- Numpy
- Mediapipe
- Pygame

## Installation

1. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Camera Calibration
You have the possibility, if you use 2 cameras, to calbirate them.

1. **Prerequisites**
    - chessboard 
    - settings of your camera :you need to change the **ID** of your cameras, the **size** of your chessboard, the **image resolution** and the **size** of each side of the squares of the chessboard.
    ```py
    calibration_settings = {
    'camera0': 2,
    'camera1': 1,
    'frame_width': 1280,
    'frame_height': 720,
    'mono_calibration_frames': 10,
    'stereo_calibration_frames': 10,
    'view_resize': 1,
    'checkerboard_box_size_scale' : 2.2,
    'checkerboard_rows': 7,
    'checkerboard_columns': 7,
    'cooldown': 100
    }
    ```

2. **Calibration of each cameras**
    - For both cameras, you must first take turns presenting the board (camera 1 then 2). For each camera, 10 frames will be captured every 100ms. To start capturing, press the space bar.
    ![Starting the frame collection](D:\TUL\VideoTrackingGym\image\Calib1.png)
    - After capturing the frames, you must validate or not the images (by pressing space to validate or S to skip).
    ![Validation of the frames](D:\TUL\VideoTrackingGym\image\Calib2.png)
    - Then, you need to calibrate both cameras at the same time. Make sure they are in their final positions and that the board is clearly visible to both of them. Press the space key to begin.
    ![Calibration both camera](D:\TUL\VideoTrackingGym\image\Calib3.png)
    - Finally, as before, validate or not the images by pressing space or S (note that this validates the image pair)
    ![Calibration both camera](D:\TUL\VideoTrackingGym\image\Calib3.png)

### Video Tracking

1. **Run the Tracking Script:**
   ```sh
   python main.py
   ```

2. **Start Tracking:**
    You will have several choices : 
        - The number of camera (1 or 2).
        - The type of sports (1 = curl, 2 = squats).
        - The possibility to calibrate the cameras.
        - Indicate the number of sets and repetitions.

