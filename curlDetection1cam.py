import cv2
import mediapipe as mp
import numpy as np
import time
from playSound import play_sound

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def main(repetions, sets):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    mp_drawing_styles = mp.solutions.drawing_styles

    leftcounter = 0
    leftstage = None

    rightcounter = 0
    rightstage = None

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    begin = True
    if begin:
        play_sound("three")
        cv2.waitKey(1000)
        play_sound("two")
        cv2.waitKey(1000)
        play_sound("one")
        cv2.waitKey(1000)
        play_sound("start")
        begin = False
    pTime = 0
    cTime = 0

    desired_fps = 10
    frame_time = 1.0 / desired_fps

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            start_time = time.time()

            ret, frame = cap.read()

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results_pose = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results_pose.pose_landmarks.landmark
                leftshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                leftwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                rightshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightelbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                righthip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                lefthip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                leftangle = calculate_angle(leftshoulder, leftelbow, leftwrist)
                rightangle = calculate_angle(rightshoulder, rightelbow, rightwrist)

                backangle = calculate_angle(leftshoulder, lefthip, righthip)

                if leftangle > 160:
                    leftstage = 'Down'
                elif leftangle < 45 and leftstage == 'Down':
                    leftcounter += 1
                    leftstage = 'Up'

                if rightangle > 160:
                    rightstage = 'Down'
                elif rightangle < 45 and rightstage == 'Down':
                    rightcounter += 1
                    rightstage = 'Up'

                if 170 < backangle < 190:
                    # The back is straight
                    pass
                else:
                    # play_sound("straighten your back")
                    pass

                # Draw rectangles on both sides of the image
                cv2.rectangle(image, (0, 0), (215, 80), (102, 206, 183), -1)
                cv2.rectangle(image, (image.shape[1] - 215, 0), (image.shape[1], 80), (102, 206, 183), -1)

                # Put text for the left hand side
                cv2.putText(image, 'Left Hand', (65, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, 'Curls', (15, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, 'Stage', (160, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                # Put text for the right hand side
                cv2.putText(image, 'Right Hand', (image.shape[1] - 150, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, 'Curls', (image.shape[1] - 200, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, 'Stage', (image.shape[1] - 65, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                # Put counters and stages for both sides
                cv2.putText(image, str(leftcounter), (20, 67), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, leftstage, (130, 67), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(rightcounter), (image.shape[1] - 205, 67), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, rightstage, (image.shape[1] - 85, 67), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            except:
                pass
        
            if rightcounter & leftcounter >= repetions:
                play_sound("success")
                rightcounter = 0
                leftcounter = 0
                sets -= 1

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(image, str(int(fps)), (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            cv2.imshow("Raw webcam feed", image)

            k = cv2.waitKey(1)
            if k & 0xFF == 27: break  # 27 is ESC key.

            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < frame_time:
                time.sleep(frame_time - elapsed_time)

            if sets == 0:
                break

    cap.release()
    cv2.destroyAllWindows()
