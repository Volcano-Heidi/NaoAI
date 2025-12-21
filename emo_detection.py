import tensorflow as tf
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

def detect_emotion(image_path):
    face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    classifier = tf.keras.models.load_model('Emotion_Detection.h5')
    class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

    # Load the image from file
    frame = cv2.imread(image_path)

    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    emotions = []

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # make a prediction on the ROI, then lookup the class
            preds = classifier.predict(roi)[0]
            label = class_labels[preds.argmax()]
            emotions.append(label)
        else:
            emotions.append('No Face Found')

    return emotions

# Example usage:
image_path = './image.jpg'
result = detect_emotion(image_path)

# Save the output to a text file
output_file_path = './output_text.txt'
with open(output_file_path, 'w') as file:
    for emotion in result:
        file.write("your emotion is "+emotion + '\n')

print("Result saved to:", output_file_path)

