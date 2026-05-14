import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'emotion_model.h5')

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

model = load_model(MODEL_PATH)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def detect_emotion(frame):
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))

    emotion, confidence = None, 0.0

    for (x, y, w, h) in faces:
        roi  = cv2.resize(gray[y:y+h, x:x+w], (48, 48))
        roi  = np.expand_dims(roi.astype('float32') / 255.0, axis=(0, -1))
        pred = model.predict(roi, verbose=0)[0]
        idx  = np.argmax(pred)
        emotion    = EMOTIONS[idx]
        confidence = float(pred[idx])

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{emotion} {confidence*100:.1f}%",
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return frame, emotion, confidence