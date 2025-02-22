
import datetime
import speech_recognition as sr
import pyttsx3
import win32com.client
import webbrowser
import subprocess
from openai import OpenAI
from config import git_2
import os

def conversation(cont):
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=git_2,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "",
            },
            {
                "role": "user",
                "content": cont,
            }
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    print(f"Mary: {response.choices[0].message.content}")
    say(response.choices[0].message.content)



def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)
def Instructions():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try :
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Some error occurred sorry.")
def written(content):
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=git_2,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "",
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    print(response.choices[0].message.content)
    new_text = ""
    new_text += response.choices[0].message.content
    if not os.path.exists("Open ai"):
        os.mkdir("Open ai")
    with open(f"Open ai/{query_1.split("intelligence")[1:]}.txt", "w") as f:
        f.write(new_text)

if __name__ == '__main__':


    say("Hello I am your assistant Mary")
    while True:
        print("Listening...")
        query_1 = Instructions()
        #opening websites
        sites = [["Wikipedia","https://wikipedia.com"], ["You Tube", "https://youtube.com"],["Google","https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query_1.lower():
                webbrowser.open(site[1])
                say(f"Opening {site[0]}")
        #telling time
        if "the time" in query_1.lower():
            Time = datetime.datetime.now().time()
            say(f"Sir the time is {Time}")
        #opening applications
        elif "open firefox".lower() in query_1.lower():
            subprocess.call("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
            print("opening firefox")
        #Note that one can easily create a list of lists as in the case of opening sites.
        elif "Using artificial intelligence".lower() in query_1.lower():
            written(query_1)
        else:
            conversation(query_1)












# See PyCharm help at https://www.jetbrains.com/help/pycharm/
