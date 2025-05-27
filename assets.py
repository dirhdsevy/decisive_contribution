import tkinter as tk
from tkinter import font
import os
import logging
import subprocess
import threading

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

        # Абсолютний шлях до файлу музики
        self.music_file = os.path.join(os.path.dirname(__file__), "background.wav")
        self._is_playing = False
        self._music_process = None
        self._music_thread = None

        # Налаштування логування
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def play_music(self):
        if not os.path.exists(self.music_file):
            self.logger.error(f"Файл музики {self.music_file} не знайдений")
            return

        if self._is_playing:
            self.logger.info("Музика вже відтворюється")
            return

        try:
            self.logger.info("Запуск відтворення музики через afplay")
            self._is_playing = True
            self._music_thread = threading.Thread(
                target=self._play_music_loop,
                daemon=True
            )
            self._music_thread.start()
        except Exception as e:
            self._is_playing = False
            self.logger.error(f"Помилка запуску відтворення музики: {e}")

    def _play_music_loop(self):
        while self._is_playing:
            try:
                self._music_process = subprocess.Popen(
                    ["afplay", self.music_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self._music_process.wait()  # Чекаємо завершення відтворення
            except Exception as e:
                self.logger.error(f"Помилка в циклі відтворення: {e}")
                self._is_playing = False
                break

    def stop_music(self):
        if self._is_playing:
            self._is_playing = False
            if self._music_process:
                self._music_process.terminate()  # Завершуємо процес
                self._music_process = None
            self._music_thread = None
            self.logger.info("Музика зупинена")