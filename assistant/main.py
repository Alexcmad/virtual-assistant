import speech_recognition.exceptions
import speech_recognition as sr
from assistant import basic, spotifyControls, taskManager, GPT_Engine
from pprint import pprint
import pyautogui as pg

r = sr.Recognizer()
mic = sr.Microphone()

while True:
    try:
        command = input("Command: ")

        gpt_parsing: str = GPT_Engine.interpret_command(command).lower()

        gpt_parsed_command = gpt_parsing.split('->')[0].strip()

        if gpt_parsed_command.startswith('play'):
            name = gpt_parsed_command.lstrip('play ')
            spotifyControls.play_playlist(name)

        elif gpt_parsed_command.startswith('open'):
            name = gpt_parsed_command.split('open')[1].strip()
            basic.open(name)

        elif gpt_parsed_command.startswith('close'):
            name = gpt_parsed_command.split('close')[1].strip()
            basic.close(name)

        elif 'pause' == gpt_parsed_command:
            spotifyControls.pause()

        elif 'next' == gpt_parsed_command:
            spotifyControls.next_track()

        elif 'previous' == gpt_parsed_command:
            spotifyControls.previous_track()

        elif 'resume' == gpt_parsed_command:
            spotifyControls.resume()

        elif gpt_parsed_command.startswith('add task'):
            task = gpt_parsed_command.split('add task')[1].strip()
            print(task)
            taskManager.add_task(task)

        elif gpt_parsed_command == 'view tasks':
            taskManager.view_tasks()

        elif gpt_parsed_command.startswith('complete task'):
            keyword = gpt_parsed_command.split('complete task')[1].strip()
            taskManager.complete_task(keyword)

        elif gpt_parsed_command.startswith('view task'):
            keyword = gpt_parsed_command.split('view task')[1].strip()
            pprint(taskManager.get_tasks_by_keyword(keyword))

        elif 'shuffle' == gpt_parsed_command:
            spotifyControls.shuffle()

        elif gpt_parsed_command.startswith("volume up"):
            try:
                amount = gpt_parsed_command.split("volume up")[1]
                if amount:
                    spotifyControls.volume_up(int(amount))
                else:
                    spotifyControls.volume_up()
            except:
                print("Error Turning Volume Up")

        elif gpt_parsed_command.startswith("volume down"):
            try:
                amount = gpt_parsed_command.split("volume down")[1]
                if amount:
                    spotifyControls.volume_down(int(amount))
                else:
                    spotifyControls.volume_down()
            except:
                print("Error Turning Volume Down")

        elif gpt_parsed_command.startswith("volume set"):
            try:
                amount = int(gpt_parsed_command.split("volume set")[1].strip())
                spotifyControls.volume_set(amount)
            except:
                print("Error Setting Volume")

        elif gpt_parsed_command == "restart":
            try:
                spotifyControls.restart()
            except:
                print("Error pulling up this chune")

        elif gpt_parsed_command.startswith("count completed task"):
            print(f"{taskManager.count_complete_tasks()} Tasks Completed")

        elif gpt_parsed_command.startswith("count incomplete task"):
            print(f"{taskManager.count_incomplete_tasks()} Tasks Incomplete")

        elif gpt_parsed_command.startswith("count total task"):
            print(f"{taskManager.count_total_tasks()} Tasks in Total")

        elif gpt_parsed_command == "clear tasks":
            taskManager.clear()

        elif gpt_parsed_command.startswith("type"):
            content = gpt_parsed_command.strip("type")
            pg.write(content)

        elif gpt_parsed_command == 'enter':
            pg.press('enter')

        elif gpt_parsed_command == 'scroll up':
            pg.scroll(clicks=1000)
        elif gpt_parsed_command == 'scroll down':
            pg.scroll(clicks=-1000)
        else:
            print(gpt_parsed_command)
            print("[The Previous Response was not a valid command therefore no action was taken]")


    except:
        print("Assistant ran into an Error")
