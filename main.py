import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import random
import subprocess
import pyautogui
import time
from playsound import playsound
import ctypes
import pyperclip

# Инициализация распознавания речи
r = sr.Recognizer()

# Инициализация синтезатора речи
engine = pyttsx3.init()

# Пути к аудиофайлам (замените на реальные пути)
audio_responses = {
    "greeting": ["sound\dobroe-utro.wav"],
    "confirmation": ["sound\daser.wav", "sound\ok1.wav"],
    "error": ["sound\error.wav"]
}

# Заготовленные фразы
prepared_phrases = {
    "ответ на сообщение": "Thank you for your message. I will be sure to reply to you soon.",
    "приветствие": "Здравствуйте! Чем могу помочь?",
    "прощание": "До свидания! Был рад помочь."
}

# Пути к приложениям (замените на реальные пути)
app_paths = {
    "telegram": "AyuGram.exe",
    "steam": "C:\\Program Files (x86)\\Steam\\Steam.exe",
    "discord": "C:\\Users\\everist\\AppData\\Local\\Discord\\"
}

def get_keyboard_layout():
    user32 = ctypes.windll.user32
    return user32.GetKeyboardLayout(0) & 0xFFFF

def switch_to_russian_layout():
    layouts = {
        0x0409: "en-US",
        0x0419: "ru-RU"
    }
    current_layout = get_keyboard_layout()
    if current_layout != 0x0419:  # If not Russian
        pyautogui.hotkey('alt', 'shift')  # Switch layout
        time.sleep(0.5)  # Wait for the switch to take effect

def listen_command():
    with sr.Microphone() as source:
        print("Слушаю...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Извините, я не понял")
        return None
    except sr.RequestError:
        print("Ошибка сервиса распознавания речи")
        return None

def execute_command(command):
    if "открой браузер" in command:
        webbrowser.open("https://www.google.com")
    elif "открой youtube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "открой вк" in command:
        webbrowser.open("https://vk.com")
    elif "открой телегу" in command:
        open_application("telegram")
    elif "открой стим" in command:
        open_application("steam")
    elif "открой discord" in command:
        open_application("discord")
    elif "ответь на сообщение" in command:
        type_text(prepared_phrases["ответ на сообщение"])
    elif "напиши" in command:
        # Извлекаем текст после слова "напиши"
        text_to_type = command.split("напиши", 1)[1].strip()
        if text_to_type:
            type_text(text_to_type)
        else:
            print("Не указан текст для ввода")
            return False
    elif "выключи ноут" in command:
        os.system("shutdown /s /t 1")
    elif "ребутни ноут" in command:
        os.system("shutdown /r /t 1")
    else:
        print("Команда не распознана")
        return False
    return True

def open_application(app_name):
    if app_name in app_paths:
        subprocess.Popen(app_paths[app_name])
    else:
        print(f"Путь к приложению {app_name} не найден")

def type_text(text):
    print(f"Пытаюсь вставить текст: {text}")  # Отладочный вывод
    switch_to_russian_layout()
    time.sleep(1)  # Даем время для переключения на нужное окно
    
    # Используем буфер обмена для вставки текста
    pyperclip.copy(text)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.press('enter')

def play_response(response_type):
    response = random.choice(audio_responses[response_type])
    playsound(response)

def main():
    print("Джарвис готов к работе. Скажите 'Джарвис', чтобы начать.")
    while True:
        command = listen_command()
        if command and "джарвис" in command:
            play_response("greeting")
            print("Джарвис слушает. Назовите команду.")
            command = listen_command()
            if command:
                success = execute_command(command)
                if success:
                    play_response("confirmation")
                else:
                    play_response("error")
            else:
                play_response("error")
        elif command and "выход" in command:
            print("Выключение...")
            break

if __name__ == "__main__":
    main()