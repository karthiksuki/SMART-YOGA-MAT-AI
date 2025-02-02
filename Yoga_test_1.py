import os
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np

# Initialize mediapipe pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculateAngle(a, b, c):
    # Ensure the keypoints are not None
    if a is None or b is None or c is None:
        return None

    # Actual calculation logic
    a = np.array(a)  # First point
    b = np.array(b)  # Midpoint
    c = np.array(c)  # Endpoint

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def extractKeypoint(image_path, frame_num):
    joint_list_video = pd.DataFrame([])

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_h, image_w, _ = image.shape

        try:
            landmarks = results.pose_landmarks.landmark if results.pose_landmarks else None

            if landmarks is None:
                print(f"No landmarks detected in {image_path}")
                return joint_list_video  # Return empty DataFrame

            # Collecting landmarks
            keypoints = {name: [landmarks[landmark.value].x, landmarks[landmark.value].y]
                         if landmarks[landmark.value].visibility > 0.5 else None
                         for name, landmark in mp_pose.PoseLandmark.__members__.items()}

            # Calculating angles (with check for None)
            # angle_1: Right shoulder to right elbow to right wrist.
            # angle_2: Left shoulder to left elbow to left wrist.
            # angle_3: Right elbow to right shoulder to right hip.
            # angle_4: Left elbow to left shoulder to left hip.
            # angle_5: Right shoulder to right hip to right knee.
            # angle_6: Left shoulder to left hip to left knee.
            # angle_7: Right hip to right knee to right ankle.
            # angle_8: Left hip to left knee to left ankle.
            angles = []
            angles.append(calculateAngle(keypoints['RIGHT_SHOULDER'], keypoints['RIGHT_ELBOW'], keypoints['RIGHT_WRIST']))
            angles.append(calculateAngle(keypoints['LEFT_SHOULDER'], keypoints['LEFT_ELBOW'], keypoints['LEFT_WRIST']))
            angles.append(calculateAngle(keypoints['RIGHT_ELBOW'], keypoints['RIGHT_SHOULDER'], keypoints['RIGHT_HIP']))
            angles.append(calculateAngle(keypoints['LEFT_ELBOW'], keypoints['LEFT_SHOULDER'], keypoints['LEFT_HIP']))
            angles.append(calculateAngle(keypoints['RIGHT_SHOULDER'], keypoints['RIGHT_HIP'], keypoints['RIGHT_KNEE']))
            angles.append(calculateAngle(keypoints['LEFT_SHOULDER'], keypoints['LEFT_HIP'], keypoints['LEFT_KNEE']))
            angles.append(calculateAngle(keypoints['RIGHT_HIP'], keypoints['RIGHT_KNEE'], keypoints['RIGHT_ANKLE']))
            angles.append(calculateAngle(keypoints['LEFT_HIP'], keypoints['LEFT_KNEE'], keypoints['LEFT_ANKLE']))

            # Filter out None angles (if keypoints were missing), replace with NaN
            angles = [angle if angle is not None else np.nan for angle in angles]

            # Creating DataFrame from landmarks only
            joint_list_video = pd.DataFrame({
                'frame': frame_num,
                'id': range(len(landmarks)),
                'x': [p.x for p in landmarks],
                'y': [p.y for p in landmarks],
                'z': [p.z for p in landmarks],
                'vis': [p.visibility for p in landmarks],
                'angle_1': [angles[0]] * len(landmarks),  # Repeat the angle for every landmark
                'angle_2': [angles[1]] * len(landmarks),
                'angle_3': [angles[2]] * len(landmarks),
                'angle_4': [angles[3]] * len(landmarks),
                'angle_5': [angles[4]] * len(landmarks),
                'angle_6': [angles[5]] * len(landmarks),
                'angle_7': [angles[6]] * len(landmarks),
                'angle_8': [angles[7]] * len(landmarks)
            })

        except Exception as e:
            print(f"An error occurred while processing {image_path}: {e}")

    return joint_list_video  # Return DataFrame with landmarks and angles

def processImagesFromFolder(folder_path, output_csv):
    # List all image files in the folder
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    all_joint_data = pd.DataFrame()

    for idx, img_path in enumerate(image_files):
        print(f"Processing {img_path}")
        joint_data = extractKeypoint(img_path, idx)
        if not joint_data.empty:
            # Use pd.concat to combine DataFrames
            all_joint_data = pd.concat([all_joint_data, joint_data], ignore_index=True)

    # Save to CSV
    all_joint_data.to_csv(output_csv, index=False)
    print(f"Data successfully saved to {output_csv}")

# Example usage:
folder_path = 'warrior2'
output_csv = 'warrior_output_final.csv'
processImagesFromFolder(folder_path, output_csv)

