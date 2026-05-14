import cv2
import threading
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk

from emotion_detector import detect_emotion
from music_player import play_for_emotion, stop, get_current_emotion

EMOTION_COLORS = {
    'happy':    '#F5A623',
    'sad':      '#4A90D9',
    'angry':    '#D0021B',
    'fear':     '#7B68EE',
    'surprise': '#50C878',
    'disgust':  '#8B4513',
    'neutral':  '#888888'
}

STABILITY_FRAMES     = 15
CONFIDENCE_THRESHOLD = 0.55

class App:
    def __init__(self, root):
        self.root            = root
        self.root.title("Emotion Music Player")
        self.root.configure(bg='#1a1a2e')
        self.root.geometry('700x600')
        self.cap             = cv2.VideoCapture(0)
        self.pending_emotion = None
        self.current_emotion = None
        self.stable_count    = 0
        self.running         = True
        self._build_ui()
        self._loop()

    def _build_ui(self):
        tk.Label(
            self.root,
            text="Emotion Music Player",
            font=tkfont.Font(family='Arial', size=18, weight='bold'),
            bg='#1a1a2e', fg='white'
        ).pack(pady=8)

        self.video_lbl = tk.Label(self.root, bg='#1a1a2e')
        self.video_lbl.pack()

        self.emotion_lbl = tk.Label(
            self.root,
            text="Detecting emotion...",
            font=tkfont.Font(family='Arial', size=14),
            bg='#1a1a2e', fg='white'
        )
        self.emotion_lbl.pack(pady=6)

        self.song_lbl = tk.Label(
            self.root,
            text="No song playing",
            font=tkfont.Font(family='Arial', size=11),
            bg='#1a1a2e', fg='#aaaaaa'
        )
        self.song_lbl.pack()

        tk.Button(
            self.root,
            text="Stop Music",
            command=stop,
            bg='#c0392b', fg='white',
            relief='flat', padx=12, pady=4
        ).pack(pady=10)

    def _loop(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            frame, emotion, conf = detect_emotion(frame)

            if emotion and conf >= CONFIDENCE_THRESHOLD:
                if emotion == self.pending_emotion:
                    self.stable_count += 1
                else:
                    self.pending_emotion = emotion
                    self.stable_count    = 1

                if self.stable_count >= STABILITY_FRAMES:
                    if emotion != self.current_emotion:
                        self.current_emotion = emotion
                        threading.Thread(
                            target=play_for_emotion,
                            args=(emotion,),
                            daemon=True
                        ).start()

                color = EMOTION_COLORS.get(emotion, 'white')
                self.emotion_lbl.config(
                    text=f"Emotion: {emotion.upper()}  ({conf*100:.1f}%)",
                    fg=color
                )

            playing = get_current_emotion()
            self.song_lbl.config(
                text=f"Playing: {playing.upper()} mood" if playing else "No song playing"
            )

            img   = Image.fromarray(
                        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    ).resize((640, 460))
            imgtk = ImageTk.PhotoImage(img)
            self.video_lbl.config(image=imgtk)
            self.video_lbl.image = imgtk

        self.root.after(30, self._loop)

    def on_close(self):
        self.running = False
        stop()
        self.cap.release()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app  = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()