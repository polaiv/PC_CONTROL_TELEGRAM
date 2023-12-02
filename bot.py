import for_keyboard
import keyboard
import telebot
import config
from sound import Sound
import pyautogui
from telebot import types
import os
import time
import ctypes
import pyaudio
import wave
import tkinter
import customtkinter
import math
import cv2
import _thread
import threading
import wmi
import pythoncom
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import subprocess
import win10toast
import sys
import openai
import winsound
import json
import webbrowser
from urllib.parse import urlparse
import random
import pharases
import win32api
import win32gui
import json 
from googletrans import Translator
from base64 import b64decode
import mouse
import pyttsx3
import shutil
import tempfile
import pyscreeze

openai.api_key = 'API ключ от OPEN AI'



url = 'https://yandex.ru/pogoda/название города' # скопируйте ссылку из интернета
response = requests.get(url)
bs = BeautifulSoup(response.text, 'lxml')
weather = bs.find('span', class_='temp__value temp__value_with-unit')


the_time = time.asctime()
the_time = the_time[11:-8]



MONITOR_BRIGHTNESS_API = 0x10
BRIGHTNESS_GET = 0x1
BRIGHTNESS_SET = 0x2

# Функция для получения дескриптора монитора
def get_monitor_handle():
    return ctypes.windll.user32.MonitorFromWindow(None, MONITOR_BRIGHTNESS_API)

# Функция для получения текущей яркости монитора
def get_current_brightness():
    handle = get_monitor_handle()
    current_brightness = ctypes.c_ulong()
    ctypes.windll.dxva2.GetMonitorBrightness(handle, ctypes.byref(current_brightness))
    return current_brightness.value

# Функция для установки яркости монитора (brightness_percent - значение от 0 до 100)
def set_brightness(brightness_percent):
    handle = get_monitor_handle()
    new_brightness = int(0xFFFF * brightness_percent / 100)
    ctypes.windll.dxva2.SetMonitorBrightness(handle, new_brightness)

# Функция для повышения яркости монитора на 2
def increase_brightness():
    current_brightness = get_current_brightness()
    new_brightness = min(current_brightness + 2, 100)
    set_brightness(new_brightness)

# Функция для понижения яркости монитора на 2
def decrease_brightness():
    current_brightness = get_current_brightness()
    new_brightness = max(current_brightness - 2, 0)
    set_brightness(new_brightness)


def press(message):
    try:
        keyboard.send(f'{message.text.lower()}')
        bot.send_message(message.chat.id, f"Кнопка {message.text} была успешно нажата✅")
    except:
        bot.send_message(message.chat.id, "Операция завершилась с ошибкой❌")


def set_brightness(brightness_level):
    # Получаем хендлер монитора
    monitor_handle = ctypes.windll.user32.MonitorFromWindow(None, 1)

    # Получаем текущие настройки яркости монитора
    monitor_info = ctypes.Structure(ctypes.c_ulong, ctypes.c_ulong, ctypes.wintypes.RECT)
    ctypes.windll.user32.GetMonitorInfoW(monitor_handle, ctypes.byref(monitor_info))

    # Устанавливаем новую яркость
    ctypes.windll.dxva2.SetMonitorBrightness(monitor_handle, brightness_level)

def hand_write_fn(message):
    keyboard.write(f"{message.text}")


def change_password(message):
    try:
        os.system(f'net user Ivan {message.text}')
        bot.send_message(message.chat.id, f"Пароль успешно сменин на {message.text}")
    except:
        bot.send_message(message.chat.id, "Не удалось сменить пароль")


def passwd_check(message):
    password = 'ваш_пароль'
    if message.text == password:
        markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1_admin = types.KeyboardButton("🔐Сменить пароль")
        btn2_admin = types.KeyboardButton("🧹Очистить папку temp")
        btn3_admin = types.KeyboardButton("🧩Меню")
        markup_admin.add(btn1_admin, btn2_admin, btn3_admin)
        bot.send_message(message.chat.id, "⚠️Админ", reply_markup=markup_admin)
    else:
        bot.send_message(message.chat.id, "Неправильный пароль, доступ запрещен")



def change_bright(message):
    try:
        set_brightness(int(message.text))
    except Exception as e:
        # print(e)
        pass

def play_sound(message):
    try:
        engine = pyttsx3.init()
        ru_voice_id = "HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Speech/Voices/Tokens/TTS_MS_RU-RU_IRINA_11.0"
        engine.setProperty('voice', ru_voice_id)
        engine.say(str(message.text))
        engine.runAndWait()
        
        bot.send_message(message.chat.id, f"Сообщение {message.text} удачно воспроизвилось✅")
    except Exception as e:
        bot.send_message(message.chat.id, f"{e}")


def open_silka(message):
    try:
        webbrowser.open(f'{message.text}')
    except:
        bot.send_message(message.chat.id, 'Неверная ссылка')

def set_vol_func(message):
    Sound.volume_set(int(message.text))

def toast(message):
    toast = win10toast.ToastNotifier()
    toast.show_toast('PC CONTROL', f'{str(message.text)}', icon_path='main_ico.ico')

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.3'
]



user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}


def parse_yandex_search(message):
    url = f"https://www.yandex.ru/search/?text={str(message.text)}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    search_results = soup.find_all('a', class_='organic__url')
    descriptions = soup.find_all('div', class_='organic__text')


    for i in range(min(3, len(search_results))):
        link = search_results[i]['href']
        link = urlparse(link).netloc + urlparse(link).path  # Преобразование в полный URL-адрес
        description = descriptions[i].text.strip()
        bot.send_message(message.chat.id, f"Ссылка: {link}")
        # bot.send_message(message.chat.id, f"Описание: {description}")


def delete_files_in_temp_folder(message):
    temp_folder = "C:\\Temp"  # Замените на реальный путь к папке temp

    deleted_count = 0
    not_deleted_count = 0

    try:
        # Получаем список файлов в папке temp
        files = os.listdir(temp_folder)

        for file in files:
            file_path = os.path.join(temp_folder, file)
            try:
                # Удаление файла
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                # Обработка ошибок при удалении
                bot.send_message(message.chat.id, f"Не удалось удалить файл {file}: {e}")
                not_deleted_count += 1
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении списка файлов: {e}")
        return

    bot.send_message(message.chat.id, f"Удалено {deleted_count} файлов, не удалено из-за ошибки {not_deleted_count} файлов.")



def console_command(message):
    try:
        subprocess.run(message.text)
        bot.delete_message(message.chat.id, message.message_id+1)
    except:
        bot.send_message(message.chat.id, 'Неверная команда')

def func_timer_shut(message):
    os.system(f'shutdown -s -f -t {int(message.text)}')

def main_func():
    
    p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     print(i, p.get_device_info_by_index(i)['name'])


    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "output.ogg"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    # print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    


# preview_text = Figlet(font='slant')
# print(preview_text.renderText('PC CONTROL'))
# print("Бот начал свою работу")
winsound.PlaySound('Доброе утро.wav', winsound.SND_FILENAME)

bot = telebot.TeleBot(config.TOKEN)



def msg_create_image_def(message):
    if message.text == '🔙Вернуться назад':
        bot.delete_message(message.chat.id, message.message_id)
        markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_media = types.KeyboardButton("🖼️Медиа")
        item_pc = types.KeyboardButton("⚙️ПК")
        close_bot = types.KeyboardButton("❌Закрыть бота")
        letter = types.KeyboardButton('✉️Сообщение')
        chatGPT = types.KeyboardButton('🧠chatGPT')
        internet = types.KeyboardButton('🌐Интернет')
        motivation = types.KeyboardButton('💪Мотивация')
        item_admin = types.KeyboardButton('⚠️Админ')
        item_programms = types.KeyboardButton('📦Программы')
        markup_2.add(item_media, item_pc, motivation, item_programms, chatGPT, internet, item_admin)
        bot.send_message(message.chat.id, '🧩Меню', reply_markup=markup_2)
    else:
        # def translate_text(text, target_language='en'):
        #     translator = Translator()
        #     translated_text = translator.translate(text, dest=target_language)
        #     return translated_text.text
        
        # translated_text = translate_text(str(message))
        bot.send_message(message.chat.id, "Генерирую картинку")
        response1 = openai.Image.create(
        prompt=message.text,
        n=1,
        size='256x256',
        response_format='b64_json'
        )

        with open('data.json', 'w') as file:
            json.dump(response1, file, indent=4, ensure_ascii=False)

        image_data = b64decode(response1['data'][0]['b64_json'])


        with open(f'generated_picture.png', 'wb') as file:
            file.write(image_data)

        bot.send_photo(message.chat.id, open('generated_picture.png', 'rb'))
        os.remove('generated_picture.png')

    


def chatGPT_fn(message):
    if message.text == '🔙Вернуться назад':
        bot.delete_message(message.chat.id, message.message_id)
        markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_media = types.KeyboardButton("🖼️Медиа")
        item_pc = types.KeyboardButton("⚙️ПК")
        close_bot = types.KeyboardButton("❌Закрыть бота")
        letter = types.KeyboardButton('✉️Сообщение')
        chatGPT = types.KeyboardButton('🧠chatGPT')
        internet = types.KeyboardButton('🌐Интернет')
        motivation = types.KeyboardButton('💪Мотивация')
        markup_2.add(item_media, item_pc, letter).add(internet).add(chatGPT).add(motivation).add(close_bot)
        bot.send_message(message.chat.id, '🧩Меню', reply_markup=markup_2)

    elif message.text == '🧠Сгенирировать фото chatGPT':
        bot.delete_message(message.chat.id, message.message_id)
        msg_create_image = bot.send_message(message.chat.id, 'Введите запрос на генерацию картинки')
        bot.register_next_step_handler(msg_create_image, msg_create_image_def)

    elif message.text == '🧠Задать вопрос chatGPT':
        bot.delete_message(message.chat.id, message.message_id)
        msg1 = bot.send_message(message.chat.id, "Введите запрос")
        bot.register_next_step_handler(msg1, chatGPT_fn)



    else:
        bot.send_message(message.chat.id, 'Запрос обрабатывается')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{message.text}",
            temperature=1,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        bot.send_message(message.chat.id, response['choices'][0]['text'])
        msg2 = bot.send_message(message.chat.id, 'Введите ваш запрос к chatGPT')
        bot.register_next_step_handler(msg2, chatGPT_fn)


@bot.message_handler(commands=['start'])
def welcome(message):

    user_id = message.from_user.id
    if user_id == "your id telegram":
    # message1 = bot.send_message(message.chat.id, message.id)
    # bot.delete_message(message.chat.id, message1)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_media = types.KeyboardButton("🖼️Медиа")
        item_pc = types.KeyboardButton("⚙️ПК")
        close_bot = types.KeyboardButton("❌Закрыть бота")
        letter = types.KeyboardButton('✉️Сообщение')
        chatGPT = types.KeyboardButton('🧠chatGPT')
        internet = types.KeyboardButton('🌐Интернет')
        item_admin = types.KeyboardButton('⚠️Админ')
        item_programms = types.KeyboardButton('📦Программы')
        # item1 = types.KeyboardButton("🔇Mute")
        # item3 = types.KeyboardButton("🖼️Скрин")
        # item4 = types.KeyboardButton("⏮️")
        # item5 = types.KeyboardButton("⏸️")
        # item6 = types.KeyboardButton("⏭️")
        # item7 = types.KeyboardButton("- 🔉")
        # item8 = types.KeyboardButton("+ 🔉")
        # item9 = types.KeyboardButton("↻Restart")
        # item10 = types.KeyboardButton("⭕Shutdown")
        # item11 = types.KeyboardButton("ALT+TAB")
        # item12 = types.KeyboardButton("ALT+F4")
        # item2 = types.KeyboardButton("🔒Заблокировать")
        # item13 = types.KeyboardButton("Discord Mute🔇")
        # item14 = types.KeyboardButton("🪟Hide all windows")
        # item15 = types.KeyboardButton("🎙️Microphone")

        markup.add(item_media, item_pc, item_programms, chatGPT, internet, item_admin)
        try:
            bot.send_photo(message.chat.id, open('название фото которое вы хотите чтобы бот отправлял', 'rb'), caption=f'👋Приветсвую вас сэр! \n\n\n🕒Время: {the_time}, \n\n\n🌤️Текущая Погода: {weather.text}', reply_markup=markup)
        except:
            bot.send_photo(message.chat.id, open('название фото которое вы хотите чтобы бот отправлял', 'rb'), caption=f'👋Приветсвую вас сэр! \n\n\n🕒Время: {the_time}, \n\n\n🌤️Текущая Погода: пока не известна', reply_markup=markup)
        bot.delete_message(message.chat.id, message.message_id)



    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к этому боту')
        incorrect_user = message.from_user.username 
        incorrect_user_id = message.from_user.id
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        app = customtkinter.CTk()
        app.geometry('400x300')
        lbl = customtkinter.CTkLabel(master=app, text=f"@{incorrect_user} Пытался получить доступ к вашему боту!")
        lbl2 = customtkinter.CTkLabel(master=app, text=f"ID: {incorrect_user_id}")
        lbl.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        lbl2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        app.mainloop()   

# @bot.message_handler(content_types=['clear'])
# def clear(message):
#     bot.send_message(message.chat.id, message.id)
    # bot.send_message(chat_id=message.chat.id, message_thread_id=message1)





@bot.message_handler(content_types=['text'])
def greeting(message):

    user_id = message.from_user.id

    if message.chat.type == 'private':
        if user_id == "your id telegram":
            if message.text == '🖼️Медиа':

                markup_media = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

                # item1_media = types.KeyboardButton("🔇")
                # item2_media = types.KeyboardButton("- 🔉")
                # item3_media = types.KeyboardButton("+ 🔉")
                # item4_media = types.KeyboardButton("⏮️")
                # item5_media = types.KeyboardButton("⏸️")
                # item6_media = types.KeyboardButton("⏭️")
                # item7_media = types.KeyboardButton("🔇Дискорд")
                # item8_media = types.KeyboardButton("🎙️Mикрофон")
                # item9_media = types.KeyboardButton("🔉Свое значение")
                # item10_media = types.KeyboardButton("🧩Меню")
                item_video = types.KeyboardButton('🎥Видео')
                item_music = types.KeyboardButton('🎧Музыка')
                item_menu = types.KeyboardButton('🧩Меню')
                markup_media.add(item_video, item_music, item_menu)
                bot.send_message(message.chat.id, '🖼️Медиа', reply_markup=markup_media)
                bot.delete_message(message.chat.id, message.message_id)


            elif message.text == '⚙️ПК':
                markup_PC = types.ReplyKeyboardMarkup(resize_keyboard=True)

                # item1_PC = types.KeyboardButton("🖼️Скрин")
                # item2_PC = types.KeyboardButton("🔄Перезагрузка")
                # item3_PC = types.KeyboardButton("🚫Выключение")
                # item4_PC = types.KeyboardButton("ALT+TAB") 
                # item5_PC = types.KeyboardButton("❌Закрыть")
                # item6_PC = types.KeyboardButton("🔒Заблокировать")
                # item7_PC = types.KeyboardButton("🪟Скрыть все окна")
                # item8_PC = types.KeyboardButton("📷Камера")
                # item9_PC = types.KeyboardButton("⏳Таймер на выключение ПК")
                # item10_PC = types.KeyboardButton('✉️Смс на экран')
                # item11_PC = types.KeyboardButton("🖥️Консольная команда")
                # item12_PC = types.KeyboardButton("❌Отмена таймера")
                # item13_PC = types.KeyboardButton("😴Спящий режим")
                # item14_PC = types.KeyboardButton('🧩Меню')

                item1_PC = types.KeyboardButton('🖥️Характеристики ПК')
                item2_PC = types.KeyboardButton("🔒Заблокировать")
                item3_PC = types.KeyboardButton("☀️Яркость")
                item4_PC = types.KeyboardButton("❌Закрыть")
                # item5_PC = types.KeyboardButton('🎙️Запись Микрофона')
                # item6_PC = types.KeyboardButton('🎙️Воспроизвести')
                # item18_PC = types.KeyboardButton('🎙️Отключить микрофон')
                item19_PC = types.KeyboardButton("🎙️Управление микрофоном")
                item7_PC = types.KeyboardButton('🖼️Сменить обои')
                item8_PC = types.KeyboardButton('✉️Смс на экран')
                item9_PC = types.KeyboardButton('📷Камера')
                item10_PC = types.KeyboardButton('🗑️Очистить корзину')
                item11_PC = types.KeyboardButton('🖼️Скрин')
                item12_PC = types.KeyboardButton("🔋Управление питанием ПК")
                item13_PC = types.KeyboardButton('📝Диспетчер задач')
                item14_PC = types.KeyboardButton('🧩Меню')
                item15_PC = types.KeyboardButton("🪟Скрыть все окна")
                item16_PC = types.KeyboardButton("ALT+TAB")
                item17_PC = types.KeyboardButton("⌨️Управление девайсами ПК")




                markup_PC.add(item1_PC).add(item2_PC, item3_PC, item4_PC).add(item19_PC).add(item7_PC, item8_PC).add(item9_PC, item10_PC, item11_PC).add(item17_PC).add(item12_PC, item13_PC).add(item15_PC, item16_PC).add(item14_PC)
                bot.send_message(message.chat.id, '⚙️Управление ПК', reply_markup=markup_PC)
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🔇':
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "Сделанно")
                    # print("Copyright (c) 2014 - %d | Paradoxis" % date.today().year)
                Sound.mute()

                # elif message.text == '🔉Unmute':
                #     bot.send_message(message.chat.id, "Сделанно")
                #     Sound.mute()l

            elif message.text == '🖼️Скрин':
                x = 1
                screenshot = pyscreeze.screenshot()
                screenshot.save('screen.png')
                with open('screen.png', 'rb') as file:
                    bot.send_photo(message.chat.id, file)
                time.sleep(.25)
                os.remove('screen.png')
                bot.delete_message(message.chat.id, message.message_id)
            elif message.text == '⏮️':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send("previous track")
            elif message.text == '⏭️':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send("next track")
            elif message.text == '⏸️':
                bot.delete_message(message.chat.id, message.message_id)
                pyautogui.press('playpause')

            elif message.text == '🎙️Воспроизвести':
                bot.delete_message(message.chat.id, message.message_id)
                msg_play = bot.send_message(message.chat.id, "Введите текст который хотите воспроизвести")
                bot.register_next_step_handler(msg_play, play_sound)

            elif message.text == '🔄Перезагрузка':

                markup_3 = types.InlineKeyboardMarkup(row_width=2)
                item1_mark3 = types.InlineKeyboardButton("Да", callback_data='yes_restart')
                item2_mark3 = types.InlineKeyboardButton("Нет", callback_data='no_restart')

                markup_3.add(item1_mark3, item2_mark3)
                bot.send_message(message.chat.id, 'Вы точно хотите перезагрузить компьютер?', reply_markup=markup_3)
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🚫Выключение ПК':
                bot.delete_message(message.chat.id, message.message_id)
                markup_2 = types.InlineKeyboardMarkup(row_width=2)
                item1_mark2 = types.InlineKeyboardButton("Да", callback_data='yes_shut')
                item2_mark2 = types.InlineKeyboardButton("Нет", callback_data='no_shut')
                markup_2.add(item1_mark2, item2_mark2)
                bot.send_message(message.chat.id, "Вы точно хотите выключить компьютер?", reply_markup=markup_2)

            elif message.text == '🎙️Управление микрофоном':
                bot.delete_message(message.chat.id, message.message_id)
                markup_micro = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1_micro = types.KeyboardButton("🎙️Запись Микрофона")
                btn2_micro = types.KeyboardButton("🎙️Воспроизвести")
                btn3_micro = types.KeyboardButton("🎙️Отключить микрофон")
                btn4_micro = types.KeyboardButton("🧩Меню")
                btn5_micro = types.KeyboardButton("⚙️ПК")
                markup_micro.add(btn1_micro).add(btn2_micro).add(btn4_micro, btn5_micro)
                bot.send_message(message.chat.id, '🎙️Управление микрофоном', reply_markup=markup_micro)


            elif message.text == '⌨️Управление девайсами ПК':
                bot.delete_message(message.chat.id, message.message_id)
                markup_devices = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1_mouse = types.KeyboardButton("🖱️Управление мышью")
                btn2_keyboard = types.KeyboardButton("⌨️Клавиатура")
                btn3_monitor = types.KeyboardButton("🖥️Отключить монитор")
                btn4_menu = types.KeyboardButton('🧩Меню')
                btn5_pc = types.KeyboardButton('⚙️ПК')
                markup_devices.add(btn1_mouse).add(btn2_keyboard).add(btn3_monitor).add(btn4_menu, btn5_pc)
                bot.send_message(message.chat.id, '⌨️Управление девайсами ПК', reply_markup=markup_devices)

            elif message.text == '📦Программы':
                bot.delete_message(message.chat.id, message.message_id)
                def get_random_smiley_from_file(file_path):
                    with open(file_path, "r") as file:
                        smileys = file.read().splitlines()
                    return random.choice(smileys)

                # Путь к файлу hearts.txt
                file_path = "hearts.txt"

                # Получение случайного смайлика из файла
                random_smiley = get_random_smiley_from_file(file_path)

                markup_programms = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1_prog = types.KeyboardButton(f"❤️Chrome")
                item2_prog = types.KeyboardButton(f"💙Telegram")
                item3_prog = types.KeyboardButton(f"🖤VS Code")
                item4_prog = types.KeyboardButton(f"💛Discord")
                item5_prog = types.KeyboardButton(f"🤍Notion")
                item6_prog = types.KeyboardButton(f"💜Epic Games")
                item7_prog = types.KeyboardButton(f"💚Steam")
                item8_prog = types.KeyboardButton("🧩Меню")
                markup_programms.add(item1_prog, item2_prog, item3_prog, item4_prog, item5_prog, item6_prog, item7_prog).add(item8_prog)
                bot.send_message(message.chat.id, "📦Программы", reply_markup=markup_programms)

            # elif message.text == '❤️Chrome':
            #     subprocess.Popen("C:\Program Files\Google\Chrome\Application\chrome.exe")
            #     bot.send_message(message.chat.id, "❤️Chrome был запущен")
            elif message.text == '💙Telegram':
                subprocess.Popen("C:\\Users\\Ivan\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
                bot.send_message(message.chat.id, "💙Telegram был запущен")
            elif message.text == '🖤VS Code':
                subprocess.Popen("C:\\Users\\Ivan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
                bot.send_message(message.chat.id, "🖤VS Code был запущен")
            elif message.text == '💛Discord':
                subprocess.Popen("C:\\Users\\Ivan\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe")
                bot.send_message(message.chat.id, "💛Discord был запущен")
            elif message.text == '🤍Notion':
                subprocess.Popen("C:\\Users\\Ivan\\AppData\\Local\\Programs\\Notion\\Notion.exe")
                bot.send_message(message.chat.id, "🤍Notion был запущен")
            elif message.text == '💜Epic Games':
                subprocess.Popen("C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe")
                bot.send_message(message.chat.id, "💜Epic Games был запущен")
            elif message.text == '💚Steam':
                subprocess.Popen("C:\\Program Files (x86)\\Steam\\steam.exe")
                bot.send_message(message.chat.id, "💚Steam был запущен")

            elif message.text == '⚠️Админ':
                markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
                passwd = bot.send_message(message.chat.id, "Для начала ввидите пароль")
                bot.register_next_step_handler(passwd, passwd_check)
                # btn1_admin = types.KeyboardButton("🔐Сменить пароль")
                # btn1_admin = types.KeyboardButton("")
                # btn1_admin = types.KeyboardButton("")
                # btn1_admin = types.KeyboardButton("")
                


            elif message.text == '🖱️Управление мышью':
                bot.delete_message(message.chat.id, message.message_id)
                markup_mouse = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1_right = types.KeyboardButton("ЛКМ")
                btn2_left = types.KeyboardButton("ПКМ")
                btn3_up = types.KeyboardButton("🔼")
                btn4_left = types.KeyboardButton("◀️")
                btn5_down = types.KeyboardButton("🔽")
                btn6_right = types.KeyboardButton("▶️")
                btn7_menu = types.KeyboardButton("🧩Меню")
                btn8_devices = types.KeyboardButton("⌨️Управление девайсами ПК")
                markup_mouse.add(btn1_right, btn2_left).add(btn3_up).add(btn4_left, btn5_down, btn6_right).add(btn7_menu, btn8_devices)
                bot.send_message(message.chat.id, '🖱️Управление мышью', reply_markup=markup_mouse)

            elif message.text == '⌨️Клавиатура':
                bot.delete_message(message.chat.id, message.message_id)
                markup_keyboardong = types.ReplyKeyboardMarkup(resize_keyboard=True)
                betn1 = types.KeyboardButton("✍️Ввод текста")
                betn2 = types.KeyboardButton("🔠Нажатие кнопки")
                betn3 = types.KeyboardButton("🧩Меню")
                betn4 = types.KeyboardButton("⌨️Управление девайсами ПК")
                markup_keyboardong.add(betn1).add(betn2).add(betn3, betn4)
                bot.send_message(message.chat.id, "⌨️Клавиатура", reply_markup=markup_keyboardong)

            elif message.text == "✍️Ввод текста":
                bot.delete_message(message.chat.id, message.message_id)
                hand_write = bot.send_message(message.chat.id, "Отправьте сообщение")
                bot.register_next_step_handler(hand_write, hand_write_fn)

            elif message.text == '🔠Нажатие кнопки':
                bot.delete_message(message.chat.id, message.message_id)
                msg_press = bot.send_message(message.chat.id, "Напишите клавишу, на английском")
                bot.register_next_step_handler(msg_press, press)

            elif message.text == '🖥️Отключить монитор':
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "Монитор был выключен")
                def is_monitor_on():
                    power_status = ctypes.c_ulong()
                    if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.pointer(power_status)):
                        monitor_on = bool(power_status.value & 0x00000001)
                        return monitor_on

                    return True
                def toggle_monitor():
                    monitor_on = is_monitor_on()

                    if monitor_on:
                        ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)
                    else:
                        ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, -1)

                toggle_monitor()


            elif message.text == 'вкл':
                bot.delete_message(message.chat.id, message.message_id)
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, -1)
                bot.send_message(message.chat.id, "Монитор был включен")


            elif message.text == 'ЛКМ':
                bot.delete_message(message.chat.id, message.message_id)
                mouse.click('left')

            elif message.text == 'ПКМ':
                bot.delete_message(message.chat.id, message.message_id)
                mouse.click('right')

            elif message.text == '🔼':
                bot.delete_message(message.chat.id, message.message_id)
                current_x, current_y = pyautogui.position()
                pyautogui.move(0, -50, duration=0.1)

            elif message.text == '🔽':
                bot.delete_message(message.chat.id, message.message_id)
                current_x, current_y = pyautogui.position()
                pyautogui.move(0, 50, duration=0.1)

            elif message.text == '▶️':
                bot.delete_message(message.chat.id, message.message_id)
                current_x, current_y = pyautogui.position()
                pyautogui.move(50, 0, duration=0.1)

            elif message.text == '◀️':
                bot.delete_message(message.chat.id, message.message_id)
                current_x, current_y = pyautogui.position()
                pyautogui.move(-50, 0, duration=0.1)


            elif message.text == '- 🔉':
                bot.delete_message(message.chat.id, message.message_id)
                Sound.volume_down()
                    # bot.send_message(message.chat.id, "Сделлано")

            elif message.text == '+ 🔉':
                bot.delete_message(message.chat.id, message.message_id)
                Sound.volume_up()
                    # bot.send_message(message.chat.id, "Сделлано")

            elif message.text == 'ALT+TAB':
                pyautogui.keyDown("alt")
                time.sleep(.2)
                pyautogui.press("tab")
                time.sleep(.2)
                pyautogui.keyUp("alt")
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '❌Закрыть':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send("alt+F4, space")
                bot.send_message(message.chat.id, "Текущее приложение было закрыто")

            elif message.text == '🔒Заблокировать':
                bot.delete_message(message.chat.id, message.message_id)
                ctypes.windll.user32.LockWorkStation()

            elif message.text == '🔇Дискорд':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send("F8")

            elif message.text == '🪟Скрыть все окна':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send("win+d")

            elif message.text == '🎙️Запись Микрофона':
                bot.delete_message(message.chat.id, message.message_id)
                main_func()
                bot.send_audio(message.chat.id, open('output.ogg', 'rb'))
                os.remove('output.ogg')

            elif message.text == '🧩Меню':
                bot.delete_message(message.chat.id, message.message_id)
                markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_media = types.KeyboardButton("🖼️Медиа")
                item_pc = types.KeyboardButton("⚙️ПК")
                close_bot = types.KeyboardButton("❌Закрыть бота")
                letter = types.KeyboardButton('✉️Сообщение')
                chatGPT = types.KeyboardButton('🧠chatGPT')
                internet = types.KeyboardButton('🌐Интернет')
                item_admin = types.KeyboardButton('⚠️Админ')
                item_programms = types.KeyboardButton('📦Программы')
                markup_2.add(item_media, item_pc, item_programms, chatGPT, internet, item_admin)
                bot.send_message(message.chat.id, '🧩Меню', reply_markup=markup_2)


            elif message.text == '🖥️Характеристики ПК':
                bot.delete_message(message.chat.id, message.message_id)
                pythoncom.CoInitialize()
                computer = wmi.WMI()
                computer_info = computer.Win32_ComputerSystem()[0]
                os_info = computer.Win32_OperatingSystem()[0]
                proc_info = computer.Win32_Processor()[0]
                gpu_info = computer.Win32_VideoController()[0]

                os_name = os_info.Name.encode('utf-8').split(b'|')[0]
                os_version = ' '.join([os_info.Version, os_info.BuildNumber])
                system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
                dict_system = {
                    'OS': 'OS Name: {0}'.format(os_name.decode('utf-8')),
                    'OS VERS': 'OS Version: {0}'.format(os_version),
                    'CPUSH': 'CPU: {0}'.format(proc_info.Name),
                    'RAMSH': 'RAM: {0} GB'.format(math.ceil(system_ram)),
                    'GRAPHIC': 'Graphics Card: {0}'.format(gpu_info.Name)
                }
                    # bot.send_message(message.chat.id, f'{dict_system.items()} + \n')
                dict_system_items = dict_system.items()

                for key, value in dict_system_items:
                    bot.send_message(message.chat.id, value)

            elif message.text == "📷Камера":
                try:
                    cap = cv2.VideoCapture(0)
                    for i in range(1, 2):
                        ret, img = cap.read()
                        cv2.imwrite('camrec.png', img)
                        # if cv2.waitKey(10) == 27:
                        #     break

                    cap.release()
                    cv2.destroyAllWindows()
                    bot.send_video(message.chat.id, open('camrec.png', 'rb'))
                    os.remove('camrec.png')
                    bot.delete_message(message.chat.id, message.message_id)

                except cv2.error:
                    bot.delete_message(message.chat.id, message.message_id)
                    bot.send_message(message.chat.id, 'Камера не найдена')

            elif message.text == '⏳Таймер на выключение ПК':
                bot.delete_message(message.chat.id, message.message_id)
                timer_shut = bot.send_message(message.chat.id, 'Введите время в секундах')
                bot.register_next_step_handler(timer_shut, func_timer_shut)

            elif message.text == '❌Отмена таймера':
                bot.delete_message(message.chat.id, message.message_id)
                os.system('shutdown -a')

            elif message.text == '🖥️Консольная команда':
                bot.delete_message(message.chat.id, message.message_id)
                msg = bot.send_message(message.chat.id, 'Введите команду')
                bot.register_next_step_handler(msg, console_command)

            elif message.text == '✉️Смс на экран':
                bot.delete_message(message.chat.id, message.message_id)
                send_toast = bot.send_message(message.chat.id, 'Введите что вы хотите вывести')
                bot.register_next_step_handler(send_toast, toast)

            elif message.text == '🔉Свое значение':
                bot.delete_message(message.chat.id, message.message_id)
                my_set_volume = bot.send_message(message.chat.id, 'Введите свое значение')
                bot.register_next_step_handler(my_set_volume, set_vol_func)

            elif message.text == '❌Закрыть бота':
                bot.delete_message(message.chat.id, message.message_id)
                bot.stop_polling()
                sys.exit(1)
                winsound.PlaySound('Отключаю питание.wav', winsound.SND_FILENAME)

            elif message.text == '😴Спящий режим':
                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'])
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '✉️Сообщение':
                try:
                    bot.send_photo(message.chat.id, open('hi-pic.jpg', 'rb'), caption=f'👋Приветсвую вас сэр! \n\n\n🕒Время: {the_time}, \n\n\n🌤️Текущая Погода: {weather.text}')
                except:
                                bot.send_photo(message.chat.id, open('hi-pic.jpg', 'rb'), caption=f'👋Приветсвую вас сэр! \n\n\n🕒Время: {the_time}, \n\n\n🌤️Текущая Погода: пока не известна')
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🧠chatGPT':
                bot.delete_message(message.chat.id, message.message_id)
                markup_4 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                btn_1_openai = types.KeyboardButton("🧠Задать вопрос chatGPT")
                btn_2_openai = types.KeyboardButton("🧠Сгенирировать фото chatGPT")
                btn_3_openai = types.KeyboardButton("🔙Вернуться назад")
                markup_4.add(btn_1_openai, btn_2_openai, btn_3_openai)
                bot.send_message(message.chat.id, '🧠chatGPT', reply_markup=markup_4)
                # bot.register_next_step_handler(chatGPT_msg, chatGPT_fn)

            elif message.text == '🧠Задать вопрос chatGPT':
                bot.delete_message(message.chat.id, message.message_id)
                markup_10 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1_chat = types.KeyboardButton("🔙Вернуться назад")
                markup_10.add(btn1_chat)
                msg1 = bot.send_message(message.chat.id, "Введите запрос", reply_markup=markup_10)
                bot.register_next_step_handler(msg1, chatGPT_fn)

            elif message.text == '🧠Сгенирировать фото chatGPT':
                bot.delete_message(message.chat.id, message.message_id)
                markup_11 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn11_chat = types.KeyboardButton("🔙Вернуться назад")
                markup_11.add(btn11_chat)
                msg2 = bot.send_message(message.chat.id, "Введите запрос на генерацию картинки", reply_markup=markup_11)
                bot.register_next_step_handler(msg2, msg_create_image_def)  

            elif message.text == '🎧Музыка':
                markup_media_keyboard = types.ReplyKeyboardMarkup()
                item0_media = types.KeyboardButton("🔉Звук")
                item1_media = types.KeyboardButton("🔇")
                item2_media = types.KeyboardButton("- 🔉")
                item3_media = types.KeyboardButton("+ 🔉")
                item4_media = types.KeyboardButton("⏮️")
                item5_media = types.KeyboardButton("⏸️")
                item6_media = types.KeyboardButton("⏭️")
                item7_media = types.KeyboardButton("🔇Дискорд")
                item10_media = types.KeyboardButton('🧩Меню')
                markup_media_keyboard.add(item0_media).add(item2_media, item1_media, item3_media, item4_media, item5_media, item6_media, item7_media).add(item10_media)
                bot.send_message(message.chat.id, '🎧Музыка', reply_markup=markup_media_keyboard)

            elif message.text == '🎥Видео':
                markup_video = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1_video = types.KeyboardButton("🔉Звук")
                item2_video = types.KeyboardButton('🔈')
                item3_video = types.KeyboardButton('🔇')
                item4_video = types.KeyboardButton('🔊')
                item5_video = types.KeyboardButton('⬅️')
                item6_video = types.KeyboardButton('⏸️')
                item7_video = types.KeyboardButton('➡️')
                item8_video = types.KeyboardButton('◀️Видео')
                item9_video = types.KeyboardButton('Видео▶️')
                item10_video = types.KeyboardButton('🖥️Во весь экран')
                item11_video = types.KeyboardButton('📎Открыть ссылку')
                item12_video = types.KeyboardButton('🧩Меню')
                item13_video = types.KeyboardButton('🖼️Медиа')
                markup_video.add(item1_video).add(item2_video, item3_video, item4_video, item5_video, item6_video, item7_video).add(item8_video, item9_video).add(item10_video).add(item11_video).add(item12_video, item13_video)
                bot.send_message(message.chat.id, '🎥Видео', reply_markup=markup_video)


            elif message.text == '◀️Видео':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send('shift+p')

            elif message.text == 'Видео▶️':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send('shift+n')

            elif message.text == '🖥️Во весь экран':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send('f')

            elif message.text == '⬅️':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send('left')

            elif message.text == '➡️':
                bot.delete_message(message.chat.id, message.message_id)
                keyboard.send('right')

            elif message.text == '📎Открыть ссылку':
                bot.delete_message(message.chat.id, message.message_id)
                msg_silka = bot.send_message(message.chat.id, "Введите ссылку")
                bot.register_next_step_handler(msg_silka, open_silka)

            elif message.text == '🔈':
                bot.delete_message(message.chat.id, message.message_id)
                Sound.volume_down()

            elif message.text == '🔊':
                bot.delete_message(message.chat.id, message.message_id)
                Sound.volume_up()

            elif message.text == '🔉Звук':
                bot.delete_message(message.chat.id, message.message_id)
                my_set_volume = bot.send_message(message.chat.id, 'Введите свое значение')
                bot.register_next_step_handler(my_set_volume, set_vol_func)

            elif message.text == '☀️Яркость':
                bot.delete_message(message.chat.id, message.message_id)
                markup_bright = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1_bright = types.KeyboardButton("⬇️Меньше")
                item2_bright = types.KeyboardButton("☀️100%")
                item3_bright = types.KeyboardButton("⬆️Больше")
                item4_bright = types.KeyboardButton("☀️0%")
                item5_bright = types.KeyboardButton("☀️25%")
                item6_bright = types.KeyboardButton("☀️50%")
                item7_bright = types.KeyboardButton("☀️75%")
                item8_bright = types.KeyboardButton("🧩Меню")
                item9_bright = types.KeyboardButton("⚙️ПК")
                #markup_bright.add(item1_bright, item2_bright, item3_bright).add(item4_bright, item5_bright, item6_bright, item7_bright).add(item8_bright, item9_bright)
                markup_bright.row(item1_bright, item2_bright, item3_bright)
                markup_bright.row(item4_bright, item5_bright, item6_bright, item7_bright)
                markup_bright.row(item8_bright, item9_bright)
                bot.send_message(message.chat.id, "☀️Яркость", reply_markup=markup_bright)

            elif message.text == '☀️100%':
                bot.delete_message(message.chat.id, message.message_id)
                bright_100 = 100
                set_brightness(bright_100)

            elif message.text == '⬇️Меньше':
                bot.delete_message(message.chat.id, message.message_id)
                decrease_brightness()

            elif message.text == '⬆️Больше':
                bot.delete_message(message.chat.id, message.message_id)
                increase_brightness()

            elif message.text == "☀️0%":
                bot.delete_message(message.chat.id, message.message_id)
                bright_0 = 0
                set_brightness(bright_0)

            elif message.text == "☀️25%":
                bot.delete_message(message.chat.id, message.message_id)
                bright_25 = 25
                set_brightness(bright_25)

            elif message.text == "☀️50%":
                bot.delete_message(message.chat.id, message.message_id)
                bright_50 = 50
                set_brightness(bright_50)
            elif message.text == '☀️75%':
                bot.delete_message(message.chat.id, message.message_id)
                bright_75 = 75
                set_brightness(bright_75)

            elif message.text == '🧹Очистить папку temp':
                bot.delete_message(message.chat.id, message.message_id)


            elif message.text == '🖼️Сменить обои':
                bot.send_message(message.chat.id, 'Отправьте картину')


            elif message.text == '🔋Управление питанием ПК':
                markup_pitanie = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1_pit = types.KeyboardButton('😴Спящий режим')
                btn2_pit = types.KeyboardButton('💤Гибернация')
                btn3_pit = types.KeyboardButton('🔄Перезагрузка')
                btn4_pit = types.KeyboardButton('🚫Выключение ПК')
                btn5_pit = types.KeyboardButton('⏳Таймер на выключение ПК')
                btn6_pit = types.KeyboardButton('❌Отмена таймера')
                btn7_pit = types.KeyboardButton('🧩Меню')
                btn8_pit = types.KeyboardButton('⚙️ПК')
                markup_pitanie.add(btn1_pit, btn2_pit, btn3_pit).add(btn4_pit).add(btn5_pit).add(btn6_pit).add(btn7_pit, btn8_pit)
                bot.send_message(message.chat.id, '🔋Управление питанием ПК', reply_markup=markup_pitanie)
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🔙Вернуться назад':
                bot.delete_message(message.chat.id, message.message_id)
                markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_media = types.KeyboardButton("🖼️Медиа")
                item_pc = types.KeyboardButton("⚙️ПК")
                close_bot = types.KeyboardButton("❌Закрыть бота")
                letter = types.KeyboardButton('✉️Сообщение')
                chatGPT = types.KeyboardButton('🧠chatGPT')
                internet = types.KeyboardButton('🌐Интернет')
                item_admin = types.KeyboardButton('⚠️Админ')
                item_programms = types.KeyboardButton('📦Программы')
                markup_2.add(item_media, item_pc, item_programms, chatGPT, internet, item_admin)
                bot.send_message(message.chat.id, '🧩Меню', reply_markup=markup_2)

            elif message.text == '💤Гибернация':
                subprocess.run(['shutdown', '/h'])
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🔐Сменить пароль':
                bot.delete_message(message.chat.id, message.message_id)
                change_pswd = bot.send_message(message.chat.id, 'Напишите новый пароль')
                bot.register_next_step_handler(change_pswd, change_password)


            elif message.text == '📝Диспетчер задач':
                keyboard.send('ctrl+shift+esc')
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🗑️Очистить корзину':
                SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
                SHEmptyRecycleBin(None, None, 1)
                bot.send_message(message.chat.id, 'Корзина очищена')
                bot.delete_message(message.chat.id, message.message_id)

            elif message.text == '🌐Интернет':
                msg_internet = bot.send_message(message.chat.id, 'Отправьте свой запрос')
                bot.register_next_step_handler(msg_internet, parse_yandex_search)



        else:
            bot.send_message(message.chat.id, 'У вас нету доступа к этому боту')




@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получаем информацию о файле
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path

    # Скачиваем файл
    downloaded_file = bot.download_file(file_path)

    # Указываем путь и имя файла, в котором мы хотим сохранить картинку
    save_path = 'image_from_user.jpg'

    # Сохраняем картинку
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)


    image_path = 'C:/Ivan/programming/PC_CONTOL_исходник/image_from_user.jpg'
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes_shut':
                os.system('shutdown -s -f -t 0')

                markup_4 = types.InlineKeyboardMarkup(row_width=1)
                item_1_mark4 = types.InlineKeyboardButton("Отменить выключение", callback_data='are_you_sure')
                markup_4.add(item_1_mark4)
                bot.delete_message(call.message.chat.id, call.message.message_id-1)

                if call.data == 'are_you_sure':
                    os.system('shutdown -a')
                    bot.send_message(call.message.chat.id, "Выключение отменено", reply_markup=None)
                    bot.delete_message(call.message.chat.id, call.message.message_id-1)

            elif call.data == 'no_shut':
                bot.send_message(call.message.chat.id, "Выключение отменнено")
                bot.delete_message(call.message.chat.id, call.message.message_id-1)




    except Exception as e:
        # print(repr(e))
        pass


    try:
        if call.message:
            if call.data == 'yes_restart':
                bot.delete_message(call.message.chat.id, call.message.message_id-1)
                os.system("shutdown /r /t 00")  
            elif call.data == 'no_restart':
                bot.send_message(call.message.chat.id, "Перезагрузка отменена")
                bot.delete_message(call.message.chat.id, call.message.message_id-1)

            



    except Exception as e1:
        # print(repr(e1))
        pass
bot.polling(none_stop=True)