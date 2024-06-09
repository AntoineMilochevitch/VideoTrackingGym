import numpy as np

def calculate_angle_3d(a, b, c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

def check_bicep_curl(shoulder, elbow, wrist,counter):
    angle = calculate_angle_3d(shoulder, elbow, wrist)
    if counter % 50 == 0:
        print("angle: ", angle)
    if angle < 55:
        return "Up"
    elif angle > 130:
        return "Down"

def check_back_straight(shoulder_left, shoulder_right, hip_left, hip_right):
    shoulder_center = (shoulder_left + shoulder_right) / 2
    hip_center = (hip_left + hip_right) / 2
    spine_vector = shoulder_center - hip_center
    vertical_ref = np.array([0, 0, 1])
    cosine_angle = np.dot(spine_vector, vertical_ref) / (np.linalg.norm(spine_vector) * np.linalg.norm(vertical_ref))
    angle_with_vertical = np.arccos(cosine_angle)
    return np.degrees(angle_with_vertical)

def main(points_3d,counter):
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

    if counter % 50 == 0:
        print("right_wrist: ", right_wrist)
        print("right_elbow: ", right_elbow)
        print("right_shoulder: ", right_shoulder)
        print("left_shoulder: ", left_shoulder)
        print("left_elbow: ", left_elbow)
        print("left_wrist: ", left_wrist)
        print("right_hip: ", right_hip)
        print("left_hip: ", left_hip)

    # Check curl for left arm
    left_position = check_bicep_curl(left_shoulder, left_elbow, left_wrist,counter)
        
    # Check curl for right arm
    right_position = check_bicep_curl(right_shoulder, right_elbow, right_wrist,counter)

    # Check if back is straight
    back_angle = check_back_straight(left_shoulder, right_shoulder, left_hip, right_hip)
    if back_angle < 10:  # Tolerance angle can be adjusted as needed
        #print("Back is straight")
        pass
    else:
        #print(f"Back angle is {back_angle:.2f} degrees, not straight")
        pass

    return left_position, right_position
