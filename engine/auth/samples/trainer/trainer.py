import cv2
import numpy as np
from PIL import Image  # pillow package
import os

# Path for samples already taken
path = 'engine\\auth\\samples'

# Create LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load Haar cascade classifier
detector = cv2.CascadeClassifier("engine\\auth\\samples\\trainer\\haarcascade_frontalface_default.xml")

def Images_And_Labels(path):  # function to fetch the images and labels
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        # Skip if it's not a file
        if not os.path.isfile(imagePath):
            continue
        # Skip if not an image file
        if not imagePath.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            gray_img = Image.open(imagePath).convert('L')  # convert to grayscale
            img_arr = np.array(gray_img, 'uint8')  # creating an array

            # Extract ID from file name e.g. User.1.jpg → 1
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            # Detect face in the image
            faces = detector.detectMultiScale(img_arr)

            for (x, y, w, h) in faces:
                faceSamples.append(img_arr[y:y + h, x:x + w])
                ids.append(id)

        except Exception as e:
            print(f"Error processing {imagePath}: {e}")

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait ...")

faces, ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

# Ensure the trainer folder exists
os.makedirs('engine\\auth\\trainer', exist_ok=True)

# Save the trained model
recognizer.write('engine\\auth\\trainer\\trainer.yml')

print("Model trained, Now we can recognize your face.")
