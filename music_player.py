import pygame
import os
import random

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, 'music')

pygame.mixer.init()
_current_emotion = None
_paused = False

def play_for_emotion(emotion):
    """
    Plays music based on the given emotion.

    Args:
        emotion (str): The emotion to play music for.
    """
    global _current_emotion
    if emotion == _current_emotion and pygame.mixer.music.get_busy() and not _paused:
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

def pause():
    """
    Pauses or unpauses the current music.
    """
    global _paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        _paused = True
    else:
        pygame.mixer.music.unpause()
        _paused = False

def stop():
    """
    Stops the current music and resets the emotion.
    """
    pygame.mixer.music.stop()
    global _current_emotion
    _current_emotion = None
    global _paused
    _paused = False

def get_current_emotion():
    """
    Returns the current emotion being played, or None if no music is playing.

    Returns:
        str or None: The current emotion or None.
    """
    return _current_emotion if pygame.mixer.music.get_busy() else None