# Emotion Music Player

A real-time facial emotion detection system that automatically plays
music based on your mood using deep learning and computer vision.

## Emotions Detected
Happy | Sad | Angry | Fear | Surprise | Disgust | Neutral

## Tech Stack
- Python 3.10
- TensorFlow / Keras
- OpenCV
- Pygame
- Tkinter

## How to Run
1. Train model on Google Colab using notebooks/train_model.ipynb
2. Download emotion_model.h5 into the model/ folder
3. Add .mp3 songs into music/<emotion>/ folders
4. Run: python app.py

## Dataset
FER-2013 from Kaggle