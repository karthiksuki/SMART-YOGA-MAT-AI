import cv2
import os
import time

output_folder = 'captured_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

num_images = 100
capture_delay = 0.5
name = input("Name: ")

for img_count in range(num_images):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Failed to grab frame.")
        break



    # Save the captured image to the folder
    img_name = os.path.join(output_folder, f'image_{name}_{img_count}.png')
    cv2.imwrite(img_name, frame)
    print(f"Captured {img_name}")

    cv2.imshow('Webcam', frame)

    # Wait for a short delay between captures
    time.sleep(capture_delay)

    # Press 'q' to quit the capturing process manually (optional)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
