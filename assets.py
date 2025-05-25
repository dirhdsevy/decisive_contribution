import tkinter as tk
from tkinter import font
import winsound
import os


class Assets:
    def __init__(self):
        self.font_large = ("Verdana", 24, "bold")
        self.font_medium = ("Verdana", 14)
        self.font_small = ("Verdana", 10)

        self.bg_color = "#2c3e50"
        self.button_color = "#3498db"
        self.button_hover = "#2980b9"
        self.text_color = "#ecf0f1"
        self.accent_color = "#e74c3c"

        self.music_file = "background.wav"

    def play_music(self):
        if os.path.exists(self.music_file):
            try:
                winsound.PlaySound(self.music_file, winsound.SND_ASYNC | winsound.SND_LOOP)
            except Exception as e:
                print(f"Помлка музики: {e}")
        else:
            print(f"Файл музики {self.music_file} не знайдений")