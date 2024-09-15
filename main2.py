import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import random
import subprocess
import pyautogui
import time
import pyperclip
from playsound import playsound
import pygame

class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        pygame.mixer.init()
        self.audio_responses = {
            "greeting": [r"C:\Users\everist\Desktop\new\jarvis\sound\daser.wav"],
            "confirmation": [r"C:\Users\everist\Desktop\new\jarvis\sound\okk.wav"],
            "error": [r"C:\Users\everist\Desktop\new\jarvis\sound\error.wav"],
            "good_morning": [r"C:\Users\everist\Desktop\new\jarvis\sound\dobroe-utro.wav"]
        }
        self.app_paths = {
            "telegram": "C:\\Users\\everist\\Downloads\\AyuGram.exe",
            "steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
            "discord": "C:\\Users\\everist\\AppData\\Local\\Discord\\app-1.0.9162\\Discord.exe"
        }
        self.websites = {
            "browser": "https://ya.ru/",
            "youtube": "https://www.youtube.com",
            "vk": "https://vk.com",
            "pogoda":  "https://yandex.by/pogoda/tselina?ysclid=m0vu86tmr0587639688&lat=46.536032&lon=41.031736"
        }

    def listen(self):
        with sr.Microphone() as source:
            print("Слушаю...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            print("Извините, я не понял")
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания речи")
            return None

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def play_audio(self, response_type):
        responses = self.audio_responses.get(response_type, [])
        for response in responses:
            if os.path.exists(response):
                try:
                    pygame.mixer.music.load(response)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    break
                except Exception as e:
                    print(f"Не удалось воспроизвести {response}: {e}")
            else:
                print(f"Файл не найден: {response}")
        else:
            print(f"Не удалось найти или воспроизвести аудио для {response_type}")
            self.speak(f"Аудио для {response_type} недоступно")

    def type_text(self, text):
        print(f"Пытаюсь вставить текст: {text}")
        pyperclip.copy(text)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

    def open_application(self, app_name):
        if app_name in self.app_paths:
            subprocess.Popen(self.app_paths[app_name])
        else:
            print(f"Путь к приложению {app_name} не найден")

    def open_website(self, website_name):
        if website_name in self.websites:
            webbrowser.open(self.websites[website_name])
        else:
            print(f"URL для {website_name} не найден")

    def good_morning_routine(self):
        self.play_audio("good_morning")
        
        # Открываем все приложения
        for app in self.app_paths:
            self.open_application(app)
            time.sleep(1)  # Небольшая пауза между запуском приложений
        
        # Открываем все сайты
        for site in self.websites:
            self.open_website(site)
            time.sleep(1)  # Небольшая пауза между открытием сайтов

    def execute_command(self, command):
        if "открой браузер" in command:
            self.open_website("browser")
        elif "открой youtube" in command:
            self.open_website("youtube")
        elif "открой вк" in command:
            self.open_website("vk")
        elif "открой погоду" in command:
            self.open_website("pogoda")
        elif "открой телегу" in command:
            self.open_application("telegram")
        elif "открой steam" in command:
            self.open_application("steam")
        elif "открой discord" in command:
            self.open_application("discord")
        elif "напиши" in command:
            text_to_type = command.split("напиши", 1)[1].strip()
            if text_to_type:
                self.type_text(text_to_type)
            else:
                print("Не указан текст для ввода")
                return False
        elif "выключи компьютер" in command:
            os.system("shutdown /s /t 1")
        elif "перезагрузи компьютер" in command:
            os.system("shutdown /r /t 1")
        elif "доброе утро" in command:
            self.good_morning_routine()
        else:
            print("Команда не распознана")
            return False
        return True

    def run(self):
        print("Джарвис готов к работе. Скажите 'Джарвис', чтобы начать.")
        while True:
            command = self.listen()
            if command and "джарвис" in command:
                self.play_audio("greeting")
                if "доброе утро" in command:
                    self.good_morning_routine()
                else:
                    print("Джарвис слушает. Назовите команду.")
                    command = self.listen()
                    if command:
                        success = self.execute_command(command)
                        if success:
                            self.play_audio("confirmation")
                        else:
                            self.play_audio("error")
                    else:
                        self.play_audio("error")
            elif command and "выход" in command:
                print("Выключение...")
                break

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()