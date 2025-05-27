import tkinter as tk
from tkinter import font
import os
import sys

try:
    import winsound
except ImportError:
    winsound = None

try:
    import pygame
except ImportError:
    pygame = None


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
            if sys.platform == "win32" and winsound:
                try:
                    winsound.PlaySound(self.music_file, winsound.SND_ASYNC | winsound.SND_LOOP)
                except Exception as e:
                    print(f"Помилка музики (winsound): {e}")
            elif pygame:
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load(self.music_file)
                    pygame.mixer.music.play(-1)
                except Exception as e:
                    print(f"Помилка музики (pygame): {e}")
            else:
                print("Аудіо не підтримується: не встановлено winsound або pygame.")
        else:
            print(f"Файл музики {self.music_file} не знайдений")
