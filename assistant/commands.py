from assistant import spotifyControls, basic, taskManager, GPT_Engine
from pprint import pprint
import pyautogui as pg
import gtts
from  playsound import playsound


def execute_command(command: str):
    command.removesuffix('.')

    if command.startswith('play'):
        name = command.split('play')[1].strip()
        spotifyControls.play(name)

    elif command.startswith('open'):
        name = command.split('open')[1].strip()
        basic.open(name)

    elif command.startswith('close'):
        name = command.split('close')[1].strip()
        basic.close(name)

    elif 'pause' == command:
        spotifyControls.pause()

    elif 'next' == command:
        spotifyControls.next_track()

    elif 'previous' == command:
        spotifyControls.previous_track()

    elif 'resume' == command:
        spotifyControls.resume()

    elif command.startswith('add task'):
        task = command.split('add task')[1].strip()
        print(f"Added task: {task}")
        taskManager.add_task(task)

    elif command == 'view tasks':
        taskManager.view_tasks()

    elif command.startswith('complete task'):
        keyword = command.split('complete task')[1].strip()
        taskManager.complete_task(keyword)

    elif command.startswith('view task'):
        keyword = command.split('view task')[1].strip()
        pprint(taskManager.get_tasks_by_keyword(keyword))

    elif 'shuffle' == command:
        spotifyControls.shuffle()

    elif command.startswith("volume up"):
        try:
            amount = command.split("volume up")[1]
            if amount:
                spotifyControls.volume_up(int(amount))
            else:
                spotifyControls.volume_up()
        except:
            print("Error Turning Volume Up")

    elif command.startswith("volume down"):
        try:
            amount = command.split("volume down")[1]
            if amount:
                spotifyControls.volume_down(int(amount))
            else:
                spotifyControls.volume_down()
        except:
            print("Error Turning Volume Down")

    elif command.startswith("volume set"):
        try:
            amount = int(command.split("volume set")[1].strip())
            spotifyControls.volume_set(amount)
        except:
            print("Error Setting Volume")

    elif command == "restart":
        try:
            spotifyControls.restart()
        except:
            print("Error pulling up this chune")

    elif command.startswith("count completed task"):
        print(f"{taskManager.count_complete_tasks()} Tasks Completed")

    elif command.startswith("count incomplete task"):
        print(f"{taskManager.count_incomplete_tasks()} Tasks Incomplete")

    elif command.startswith("count total task"):
        print(f"{taskManager.count_total_tasks()} Tasks in Total")

    elif command == "clear tasks":
        taskManager.clear()

    elif command.startswith("type"):
        content = command.strip("type")
        pg.write(content)

    elif command == 'enter':
        pg.press('enter')

    elif command == 'scroll up':
        pg.scroll(clicks=1000)
    elif command == 'scroll down':
        pg.scroll(clicks=-1000)

    elif command == 'now playing':
        song = spotifyControls.now_playing()
        ans = (GPT_Engine.answer_question(f"{song} what song is this?"))
        print(ans)

    elif command.startswith("ask question"):
        question = command.split("ask question")[1].strip()
        ans = GPT_Engine.answer_question(question)
        print(ans)


    else:
        return True
