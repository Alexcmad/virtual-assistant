import speech_recognition.exceptions
from dotenv import load_dotenv
import os
import speech_recognition as sr
from assistant import basic, spotifyControls, taskManager
from pprint import pprint
import pyautogui as pg

load_dotenv()
GPT_SECRET = os.getenv("GPT_SECRET")

r = sr.Recognizer()
mic = sr.Microphone()

while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("Listening: ")
            audio = r.listen(source)
            command: str = r.recognize_google(audio)
            print(command)
            command=command.lower()

        if command.startswith("i said "):
            command = command.lstrip("I said ")

        if command.startswith('play'):
            name = command.lstrip('play ')
            spotifyControls.play_playlist(name)

        elif command.startswith('open'):
            name = command.lstrip('open')
            basic.open(name)

        elif command.startswith('close'):
            name = command.lstrip('close')
            basic.close(name)

        elif 'pause' in command:
            spotifyControls.pause()

        elif 'next' in command:
            spotifyControls.next_track()

        elif 'previous' in command:
            spotifyControls.previous_track()

        elif 'resume' in command:
            spotifyControls.resume()

        elif command.startswith('add task'):
            task = command.lstrip('add task')
            taskManager.add_task(task)

        elif command.startswith('complete task'):
            keyword = command.lstrip('complete task ')
            taskManager.complete_task(keyword)

        elif command.startswith('view task'):
            keyword = command.lstrip('view task')
            pprint(taskManager.get_tasks_by_keyword(keyword))

        elif 'shuffle' in command:
            spotifyControls.shuffle()

        elif command.startswith("volume up"):
            try:
                amount = int(command.lstrip("volume up"))
                spotifyControls.volume_up(amount)
            except:
                print("Error Turning Volume Up")

        elif command.startswith("volume down"):
            try:
                amount = int(command.lstrip("volume down"))
                spotifyControls.volume_down(amount)
            except:
                print("Error Turning Volume Down")

        elif command.startswith("count completed task"):
            print(f"{taskManager.count_complete_tasks()} Tasks Completed")

        elif command.startswith("count incomplete task"):
            print(f"{taskManager.count_incomplete_tasks()} Tasks Incomplete")

        elif command.startswith("count total task"):
            print(f"{taskManager.count_total_tasks()} Tasks in Total")

        elif command.startswith("type"):
            content = command.strip("type")
            pg.write(content)

        elif command == 'enter':
            pg.press('enter')

        elif command=='scroll up':
            pg.scroll(clicks=100)
        elif command=='scroll down':
            pg.scroll(clicks=-100)
        else:
            print("Command not recognized")


    except speech_recognition.exceptions.UnknownValueError:
        continue
