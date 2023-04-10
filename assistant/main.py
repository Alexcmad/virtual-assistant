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
        command = input(f"{count+1}/{msg_limit}: Command -> ").lower()

        if command in ["reset","thank you","thanks"]:
            count = msg_limit

        elif commands.execute_command(command):

            gpt_parsing: str = GPT_Engine.interpret_command(command).lower()
            gpt_parsed_command = gpt_parsing.split('->')[0].strip().strip(".")
            command = gpt_parsed_command
            if commands.execute_command(command):
                print(command)
                print("[The Previous Response was not a valid command therefore no action was taken]")

    except Exception as e:
        print("Assistant ran into an Error")
        print(e)
    count += 1
