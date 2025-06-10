import os
import eel
import subprocess
import json
from engine.features import *
from engine.commands import *
from engine.auth.samples.trainer import recoganize

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        subprocess.call([r'device.bat'])  
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can I Help You?")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)

@eel.expose
def openSettings():
    print("Settings panel opened")
    speak("Here are your settings")

@eel.expose
def saveSettings(voice_id, speech_rate):
    settings = {
        "voice_id": voice_id,
        "speech_rate": speech_rate
    }

    with open("settings.json", "w") as f:
        json.dump(settings, f)

    speak("Settings saved successfully.")
