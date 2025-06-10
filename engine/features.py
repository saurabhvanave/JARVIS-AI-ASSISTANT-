import os
from playsound import playsound
from engine.commands import speak
import eel
from pipes import quote
import subprocess
import pyautogui
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import re
import webbrowser
import sqlite3
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio
import struct
import time
from engine.helper import remove_words
from hugchat import hugchat

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
# JArvis sound fn

@eel.expose
def playAssistantSound():
   music_dir = "www/assets/audio/jarvis audio.mp3"
   playsound(music_dir)
   
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")
      
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:  # ✅ Check if it's not None
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak(query)


    
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
            
            
            
# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 36
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)
    
    
# chat
import sqlite3

def chatBot(query):
    user_input = query.lower()

    # Immediately show the new question on the front-end
    eel.DisplayMessage(user_input)  # 🧠 Show the question immediately on screen

    # Connect to the SQLite database
    conn = sqlite3.connect('jarvis.db')
    cursor = conn.cursor()

    # Check if the query exists in the database
    cursor.execute("SELECT answer FROM general_responses WHERE question LIKE ?", ('%' + user_input + '%',))
    result = cursor.fetchone()

    # If a response is found in the database, use it
    if result:
        response = result[0]
    else:
        # If no database answer is found, use the chatbot
        chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)

    print(response)

    # Show the new answer on the screen once it is ready
    eel.receiverText(response)        # 📡 Send to front-end (SiriWave etc.)
    eel.DisplayMessage(response)      # 🧠 Show message on screen
    speak(response)                   # 🎤 Speak it out loud

    # Commit any necessary changes (optional)
    conn.commit()
    conn.close()

    return response


# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)
  
  
  
# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(270,1504)
    #start chat
    tapEvents(569,1515)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(172,305)
    # tap on input
    tapEvents(168,1521)
    #message
    adbInput(message)
    #send
    tapEvents(660,928)
    speak("message send successfully to "+name)
    
    
    



       