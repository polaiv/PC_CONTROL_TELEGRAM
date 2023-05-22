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
from tkinter import *
import wmi
import math




    

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
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    



print("The bot was launched")

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):

    user_id = message.from_user.id
    """You have to print(user_id) this, and get your user id, after you must to paste it below, read more detailed in README.md"""

    if user_id == "your user_id (int)":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item_media = types.KeyboardButton("Media 🔉")
        item_pc = types.KeyboardButton("PC 💻")
        parameters_pc = types.KeyboardButton("PC Features 🖥️")
        
        markup.add(parameters_pc, item_pc, item_media)
        bot.send_message(message.chat.id, "Access is allowed", reply_markup=markup)


    else:
        bot.send_message(message.chat.id, 'You do not have access to this bot')
        incorrect_user = message.from_user.username
        window = Tk()
        window.title("Notification!")
        lbl = Label(window, text=f'@{incorrect_user}, tried to access your bot!')
        lbl.place(x=105, y=130)
        window.geometry('500x300')
        window.mainloop()




@bot.message_handler(content_types=['text'])
def greeting(message):
    if message.chat.type == 'private':

        if message.text == 'Media 🔉':
            markup_media = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1_media = types.KeyboardButton("🔇Mute")
            item2_media = types.KeyboardButton("- 🔉")
            item3_media = types.KeyboardButton("+ 🔉")
            item4_media = types.KeyboardButton("⏮️")
            item5_media = types.KeyboardButton("⏸️")
            item6_media = types.KeyboardButton("⏭️")
            item8_media = types.KeyboardButton("🎙️Microphone")
            item10_media = types.KeyboardButton("🧩Menu")
            markup_media.add(item1_media, item2_media, item3_media, item4_media, item5_media, item6_media, item8_media, item10_media)
            bot.send_message(message.chat.id, 'Select an item', reply_markup=markup_media)



        elif message.text == 'PC 💻':
            markup_PC = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1_PC = types.KeyboardButton("🖼️Screen")
            item2_PC = types.KeyboardButton("↻Restart")
            item3_PC = types.KeyboardButton("⭕Shutdown")
            item4_PC = types.KeyboardButton("ALT+TAB")
            item5_PC = types.KeyboardButton("ALT+F4")
            item6_PC = types.KeyboardButton("💻LOGOUT")
            item7_PC = types.KeyboardButton("🪟Hide all windows")
            item8_PC = types.KeyboardButton('🧩Menu')

            markup_PC.add(item1_PC, item2_PC, item3_PC, item4_PC, item5_PC, item6_PC, item7_PC, item8_PC)
            bot.send_message(message.chat.id, 'Select an item', reply_markup=markup_PC)


        elif message.text == '🔇Mute':
            bot.send_message(message.chat.id, "Done")

            Sound.mute()


        elif message.text == '🖼️Screen':
            screenshot = pyautogui.screenshot()
            screenshot.save('screen.png')
            with open('screen.png', 'rb') as file:
                bot.send_photo(message.chat.id, file)
            time.sleep(.25)
            os.remove('screen.png')
        elif message.text == '⏮️':
            keyboard.send("previous track")
        elif message.text == '⏭️':
            keyboard.send("next track")
        elif message.text == '⏸️':
            pyautogui.press('playpause')
        elif message.text == '↻Restart':

            markup_3 = types.InlineKeyboardMarkup(row_width=2)
            item1_mark3 = types.InlineKeyboardButton("Yes", callback_data='yes_restart')
            item2_mark3 = types.InlineKeyboardButton("No", callback_data='no_restart')

            markup_3.add(item1_mark3, item2_mark3)
            bot.send_message(message.chat.id, 'Are you sure you want to restart your computer?', reply_markup=markup_3)

        elif message.text == '⭕Shutdown':

            markup_2 = types.InlineKeyboardMarkup(row_width=2)
            item1_mark2 = types.InlineKeyboardButton("Yes", callback_data='yes_shut')
            item2_mark2 = types.InlineKeyboardButton("No", callback_data='no_shut')
            markup_2.add(item1_mark2, item2_mark2)
            bot.send_message(message.chat.id, "Are you sure you want to turn off your computer?", reply_markup=markup_2)


        elif message.text == '- 🔉':
            Sound.volume_down()
            # bot.send_message(message.chat.id, "Done")

        elif message.text == '+ 🔉':
            Sound.volume_up()
            # bot.send_message(message.chat.id, "Done")

        elif message.text == 'ALT+TAB':
            pyautogui.keyDown("alt")
            time.sleep(.2)
            pyautogui.press("tab")
            time.sleep(.2)
            pyautogui.keyUp("alt")


        elif message.text == 'ALT+F4':
            keyboard.send("alt+F4, space")
            bot.send_message(message.chat.id, "The current application has been closed")

        elif message.text == '💻LOGOUT':
            ctypes.windll.user32.LockWorkStation()

        elif message.text == '🪟Hide all windows':
            keyboard.send("win+d, space")

        elif message.text == '🎙️Microphone':
            main_func()
            bot.send_audio(message.chat.id, open('output.ogg', 'rb'))
            os.remove('output.ogg')

        elif message.text == '🧩Menu':
            markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item_media = types.KeyboardButton("Media 🔉")
            item_pc = types.KeyboardButton("PC 💻")
            parameters_pc = types.KeyboardButton("PC Features 🖥️")
            markup_2.add(parameters_pc, item_pc, item_media)
            bot.send_message(message.chat.id, 'Select an item', reply_markup=markup_2)


        elif message.text == 'PC Features 🖥️':
            computer = wmi.WMI()
            computer_info = computer.Win32_ComputerSystem()[0]
            os_info = computer.Win32_OperatingSystem()[0]
            proc_info = computer.Win32_Processor()[0]
            gpu_info = computer.Win32_VideoController()[0]

            os_name = os_info.Name.encode('utf-8').split(b'|')[0]
            os_version = ' '.join([os_info.Version, os_info.BuildNumber])
            system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
            dict_system = {
                'OS': 'OS Name: {0}'.format(os_name),
                'OS VERS': 'OS Version: {0}'.format(os_version),
                'CPUSH': 'CPU: {0}'.format(proc_info.Name),
                'RAMSH': 'RAM: {0} GB'.format(math.ceil(system_ram)),
                'GRAPHIC': 'Graphics Card: {0}'.format(gpu_info.Name)
            }

            dict_system_items = dict_system.items()

            for key, value in dict_system_items:
                bot.send_message(message.chat.id, value)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes_shut':
                os.system('shutdown -s')

                markup_4 = types.InlineKeyboardMarkup(row_width=1)
                item_1_mark4 = types.InlineKeyboardButton("Cancel shutdown", callback_data='are_you_sure')
                markup_4.add(item_1_mark4)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.chat.id, text="shutdown",
                                      reply_markup=markup_4)

                if call.data == 'are_you_sure':
                    os.system('shutdown -a')
                    bot.send_message(call.message.chat.id, "Shutdown canceled", reply_markup=None)

            elif call.data == 'no_shut':
                bot.send_message(call.message.chat.id, "Shutdown canceled")




    except Exception as e:
        print(repr(e))


    try:
        if call.message:
            if call.data == 'yes_restart':
                os.system("shutdown /r /t 00")
            elif call.data == 'no_restart':
                bot.send_message(call.message.chat.id, "Reboot canceled")

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.chat.id, text="Restart",
                                  reply_markup=None)


    except Exception as e1:
        print(repr(e1))
bot.polling(none_stop=True)