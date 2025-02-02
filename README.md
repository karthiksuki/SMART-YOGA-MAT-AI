# Smart Yoga Mat with AI Capabilities
## Objective:
Develop an AI-powered yoga mat that offers real-time feedback on a user's posture during yoga practice, helping individuals correct their form and avoid injuries.

## Process:

### Data Collection:
I sourced a comprehensive dataset from Kaggle, web scraping, and data collection from various yoga practitioners to build a diverse and robust dataset. This data included key features such as angles of the body parts (hands, hips, legs, ankles) that are critical for assessing posture.

### Feature Engineering:
Using the collected data, I extracted key joint angles from various poses, including critical body parts like the hands, hips, legs, and ankles. These angles were calculated and organized into a CSV format for model training.

### Model Training:
I applied Random Forest Regressor, a machine learning algorithm, to the dataset to predict posture accuracy. This model was trained to recognize the proper angles for poses, with particular emphasis on the Warrior-2 Pose. The model achieved an accuracy of approximately 95% for this specific yoga pose.

### Real-Time Implementation:
Leveraging computer vision techniques, the system was integrated with a webcam to monitor the user’s posture in real-time. As users perform the Warrior-2 Pose (or similar poses), the system continuously compares the current angles with the trained model to identify deviations.

### Posture Correction:
The AI system acts as a virtual yoga tutor by analyzing the user's body angles in real-time. If any posture deviations are detected, the system provides corrective feedback to help the user improve their alignment. This feedback is shown visually via the camera feed, guiding the user toward proper form.

## Outcome:

The Smart Yoga Mat, with its real-time posture correction feature, significantly enhanced the user experience by offering instant feedback during yoga practice.
The 95% accuracy in detecting the Warrior-2 Pose ensured that the system could provide highly reliable posture correction, creating a user-friendly experience for practitioners of all levels.
