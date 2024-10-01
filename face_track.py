import cv2
import numpy as np

import time


def analyze_face_and_eyes(frame):
  """
  Analyzes face and eye direction in a given image.

  Args:
      frame (numpy.ndarray): The image frame.

  Returns:
      tuple: A tuple containing two dictionaries, 'face_direction' and 'eye_directions'.
          - face_direction (dict): Contains keys 'up', 'down', 'left', and 'right'
            with values set to True if the face is oriented in that direction
            and False otherwise.
          - eye_directions (list of dicts): Contains a list of dictionaries,
            one for each detected eye. Each dictionary has the same keys as
            'face_direction' with values indicating the direction of that eye.
  """

  # Load face and eye cascade classifiers (assuming they are in the same directory)
  face_cascade = cv2.CascadeClassifier('face_detect_dataset/haarcascade_frontalface_default.xml')
  eye_cascade = cv2.CascadeClassifier('face_detect_dataset/haarcascade_eye.xml')

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Detect faces
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  # Initialize face and eye direction variables
  face_direction = {'up': False, 'down': False, 'left': False, 'right': False}
  eye_directions = []

  # Iterate over detected faces
  for (x, y, w, h) in faces:
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]

    # Detect eyes within the face ROI
    eyes = eye_cascade.detectMultiScale(roi_gray)

    # Analyze face direction
    face_center = (x + w // 2, y + h // 2)
    image_center = (frame.shape[1] // 2, frame.shape[0] // 2)

    face_direction['up'] = face_center[1] < image_center[1]
    face_direction['down'] = face_center[1] > image_center[1]
    face_direction['left'] = face_center[0] < image_center[0]
    face_direction['right'] = face_center[0] > image_center[0]

    # Analyze eye directions
    for (ex, ey, ew, eh) in eyes:
      eye_center = (ex + ew // 2, ey + eh // 2)
      eye_direction = {'up': False, 'down': False, 'left': False, 'right': False}

      eye_direction['up'] = eye_center[1] < face_center[1]
      eye_direction['down'] = eye_center[1] > face_center[1]
      eye_direction['right'] = eye_center[0] < face_center[0]
      eye_direction['left'] = eye_center[0] > face_center[0]

      eye_directions.append(eye_direction)

  return face_direction, eye_directions
import cv2
import time

def generate_video_feed():
    """
    Captures video frames from the default camera, analyzes face and eye directions,
    and prints the results to the console.

    Yields:
        None: This function doesn't yield anything as it directly prints the results.

    Returns:
        None: This function doesn't explicitly return anything.
    """

    cap = cv2.VideoCapture(0)  # Open the default camera

    while True:
        ret, frame = cap.read()

        if not ret:
            break  # Exit the loop if frame reading fails

        face_direction, eye_directions = analyze_face_and_eyes(frame)  # Assuming `analyze_face_and_eyes` exists

        # Generate text output
        output_text = "Face Direction: "
        output_text += "Up" if face_direction['up'] else ""
        output_text += "Down" if face_direction['down'] else ""
        output_text += "Left" if face_direction['left'] else ""
        output_text += "Right" if face_direction['right'] else ""

        output_text += "\nEye Directions:"
        for i, eye_direction in enumerate(eye_directions):
            output_text += f"\n  Eye {i+1}: "
            output_text += "Up" if eye_direction['up'] else ""
            output_text += "Down" if eye_direction['down'] else ""
            output_text += "Left" if eye_direction['left'] else ""
            output_text += "Right" if eye_direction['right'] else ""

        # Print the output text with a 2-second delay
        return output_text
        time.sleep(2)

    # Release the video capture resource
    cap.release()

# Call the function to start the video processing
generate_video_feed()