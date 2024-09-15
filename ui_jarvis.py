import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import random
import subprocess
import pyautogui
import time
import pygame
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Инициализация colorama

class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        pygame.mixer.init()
        self.audio_responses = {
            "greeting": [r"C:\Users\everist\Desktop\new\jarvis\sound\ok.wav"],
            "confirmation": [r"C:\Users\everist\Desktop\new\jarvis\sound\okk.wav"],
            "error": [r"C:\Users\everist\Desktop\new\jarvis\sound\error.wav"],
            "good_morning": [r"C:\Users\everist\Desktop\new\jarvis\sound\dobroe-utro.wav"]
        }

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
                    print(Fore.RED + f"Не удалось воспроизвести {response}: {e}")
            else:
                print(Fore.RED + f"Файл не найден: {response}")
        else:
            print(Fore.RED + f"Не удалось найти или воспроизвести аудио для {response_type}")
            self.speak(f"Аудио для {response_type} недоступно")

    def listen(self):
        with sr.Microphone() as source:
            print(Fore.YELLOW + "Слушаю...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
            print(Fore.GREEN + f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            print(Fore.RED + "Извините, я не понял")
            return None
        except sr.RequestError:
            print(Fore.RED + "Ошибка сервиса распознавания речи")
            return None

    def speak(self, text):
        print(Fore.BLUE + f"Джарвис говорит: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def execute_command(self, command):
        if "открой браузер" in command:
            webbrowser.open("https://www.google.com")
            return True
        elif "открой youtube" in command:
            webbrowser.open("https://www.youtube.com")
            return True
        elif "открой вк" in command:
            webbrowser.open("https://vk.com")
            return True
        # Добавьте остальные команды здесь
        else:
            print(Fore.RED + "Команда не распознана")
            return False

    def good_morning_routine(self):
        self.speak("Доброе утро! Начинаю утреннюю рутину.")
        # Здесь реализуйте утреннюю рутину
        print(Fore.CYAN + "Выполняю утреннюю рутину...")
        # Например:
        webbrowser.open("https://www.google.com")
        webbrowser.open("https://www.youtube.com")
        # Добавьте другие действия по вашему усмотрению
        self.speak("Утренняя рутина завершена.")

    def run(self):
        print(Back.WHITE + Fore.BLACK + "Джарвис готов к работе. Скажите 'Джарвис', чтобы начать.")
        while True:
            command = self.listen()
            if command and "джарвис" in command:
                self.play_audio("greeting")
                if "доброе утро" in command:
                    self.good_morning_routine()
                else:
                    print(Fore.YELLOW + "Джарвис слушает. Назовите команду.")
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
                print(Fore.MAGENTA + "Выключение...")
                break

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()