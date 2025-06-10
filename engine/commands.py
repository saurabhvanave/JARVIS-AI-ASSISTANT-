import pyttsx3
import speech_recognition as sr
import eel
import time
import json


import keyboard  # Add keyboard module to detect escape key

def speak(text):
    try:
        text = str(text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 174)
        
        # First display the message
        eel.DisplayMessage(text)
        eel.receiverText(text)  # Send to chat
        
        # Then speak it
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print("Error in speak function:", str(e))


 
    
@eel.expose  
    
def takecommand():
    
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print('listning....')
        eel.DisplayMessage('listning....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source,10, 6)
    
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing')
        query = r.recognize_google(audio,language='en-in',)
        print(f"usr said: {query}")
        eel.DisplayMessage(query) 
        # time.sleep(2)
        
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    
    if message ==1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    try:
        
    
        if "open" in query:
          from engine.features import openCommand
          openCommand(query)
        elif "on youtube" in query :
           from engine.features import PlayYoutube
           PlayYoutube(query)
           
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall,sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
            elif "take photo" in query or "click photo" in query or "capture image" in query or "click selfie" in query:
             from engine.features import takePhotoWithCameraChoice
            if "front" in query or "selfie" in query:
                takePhotoWithCameraChoice("front")
            else:
                takePhotoWithCameraChoice("back")
        
        else:
          from engine.features import chatBot
          chatBot(query)
    except:
        print("error")       
           
    eel.ShowHood()
        
        
        
