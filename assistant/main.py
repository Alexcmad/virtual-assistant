import openai.error
import speech_recognition.exceptions
import speech_recognition as sr
from assistant import GPT_Engine, commands
from pprint import pprint
import pyautogui as pg

r = sr.Recognizer()
mic = sr.Microphone()

msg_limit = 5

count = 0
while True:
    if count > msg_limit-1:
        GPT_Engine.message_history = GPT_Engine.refresh_history()
        print("[Command History has been Reset]")
        count = 0
    try:
        command = input(f"{count+1}/{msg_limit}: Command -> ")

        gpt_parsing: str = GPT_Engine.interpret_command(command).lower()

        gpt_parsed_command = gpt_parsing.split('->')[0].strip()

        commands.execute_command(gpt_parsed_command)

    except:
        print("Assistant ran into an Error")
    count += 1
