import pygame
import os
import random

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, 'music')

pygame.mixer.init()
_current_emotion = None

def play_for_emotion(emotion):
    """
    Plays music for the given emotion.

    If the music folder for the emotion does not exist or is empty, the function will print an error message and return without playing any music.

    Args:
        emotion (str): The emotion for which to play music.
    """
    global _current_emotion
    if emotion == _current_emotion and pygame.mixer.music.get_busy():
        return

    folder = os.path.join(MUSIC_DIR, emotion)
    if not os.path.exists(folder):
        print(f"Music folder for emotion '{emotion}' does not exist: {folder}")
        return

    if not os.listdir(folder):
        print(f"Music folder for emotion '{emotion}' is empty: {folder}")
        return

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
    """
    Stops the currently playing music.
    """
    pygame.mixer.music.stop()
    global _current_emotion
    _current_emotion = None

def get_current_emotion():
    """
    Returns the current emotion for which music is playing, or None if no music is playing.

    Returns:
        str or None: The current emotion or None.
    """
    return _current_emotion if pygame.mixer.music.get_busy() else None