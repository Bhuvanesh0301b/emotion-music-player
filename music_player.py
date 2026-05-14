import pygame
import os
import random

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, 'music')

pygame.mixer.init()
_current_emotion = None

def play_for_emotion(emotion):
    global _current_emotion
    if emotion == _current_emotion and pygame.mixer.music.get_busy():
        return

    folder = os.path.join(MUSIC_DIR, emotion)
    songs  = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(('.mp3', '.wav', '.ogg'))
    ]

    if not songs:
        print(f"No songs found in music/{emotion}/ folder")
        return

    song = random.choice(songs)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    _current_emotion = emotion
    print(f"Now playing [{emotion}]: {os.path.basename(song)}")

def stop():
    pygame.mixer.music.stop()
    global _current_emotion
    _current_emotion = None

def get_current_emotion():
    return _current_emotion if pygame.mixer.music.get_busy() else None