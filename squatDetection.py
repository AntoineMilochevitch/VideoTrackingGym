import numpy as np
from playSound import play_sound

def calculate_angle_3d(a, b, c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

def check_squat(angle_left, angle_right):

    if angle_left < 90 and angle_right < 90:
        return "Down"
    elif angle_left > 150 and angle_right > 150:
        return "Up"

def check_back_straight(shoulder_left, shoulder_right, hip_left, hip_right):
    shoulder_center = (shoulder_left + shoulder_right) / 2
    hip_center = (hip_left + hip_right) / 2
    spine_vector = shoulder_center - hip_center
    vertical_ref = np.array([0, 0, 1])
    cosine_angle = np.dot(spine_vector, vertical_ref) / (np.linalg.norm(spine_vector) * np.linalg.norm(vertical_ref))
    angle_with_vertical = np.arccos(cosine_angle)
    return np.degrees(angle_with_vertical)

def main(points_3d):
    landmarks_3d = np.array(points_3d)

    # Extract coordinates for left and right sides
    right_wrist = np.array(landmarks_3d[0])
    right_elbow = np.array(landmarks_3d[1])
    right_shoulder = np.array(landmarks_3d[2])
    left_shoulder = np.array(landmarks_3d[3])
    left_elbow = np.array(landmarks_3d[4])
    left_wrist = np.array(landmarks_3d[5])
    right_hip = np.array(landmarks_3d[6])
    left_hip = np.array(landmarks_3d[7])
    left_knee = np.array(landmarks_3d[8])
    right_knee = np.array(landmarks_3d[9])
    left_ankle = np.array(landmarks_3d[10])
    right_ankle = np.array(landmarks_3d[11])

    angle_left = calculate_angle_3d(left_ankle, left_knee, left_hip)
    angle_right = calculate_angle_3d(right_ankle, right_knee, right_hip)

    trunk_angle_left = calculate_angle_3d(left_hip,left_shoulder, left_wrist)
    trunk_angle_right = calculate_angle_3d(right_hip,right_shoulder, right_wrist)


    squat_detected =  check_squat(angle_left, angle_right)

    if trunk_angle_left < 90 and trunk_angle_left > 58:
        print("Trunk is straight")
    else:
        print(f"Trunk angle is {trunk_angle_left:.2f} degrees, not straight")

    if trunk_angle_right < 90 and trunk_angle_right > 58:
        print("Trunk is straight")
    else:
        print(f"Trunk angle is {trunk_angle_right:.2f} degrees, not straight")

    back_angle = check_back_straight(left_shoulder, right_shoulder, left_hip, right_hip)
    if back_angle < 10:  # Tolerance angle can be adjusted as needed
        print("Back is straight")
    else:
        print(f"Back angle is {back_angle:.2f} degrees, not straight")
        play_sound("straighten your back")


    return squat_detected

if __name__ == "__main__":
    main()
