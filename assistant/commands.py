from assistant import spotifyControls, basic, taskManager, GPT_Engine, contactManager, emailReader
from pprint import pprint
import pyautogui as pg
import gtts
from playsound import playsound


def execute_command(command: str):
    command.removesuffix('.')
    lower_command = command.lower()

    if lower_command.startswith('play'):
        name = command.split('play')[1].strip()
        spotifyControls.play(name)

    elif lower_command.startswith('open'):
        name = command.split('open')[1].strip()
        basic.Aopen(name)

    elif lower_command.startswith('close'):
        name = command.split('close')[1].strip()
        basic.close(name)

    elif 'pause' == lower_command:
        spotifyControls.pause()

    elif 'next' == lower_command:
        spotifyControls.next_track()

    elif 'previous' == lower_command:
        spotifyControls.previous_track()

    elif 'resume' == lower_command:
        spotifyControls.resume()

    elif lower_command.startswith('add task'):
        task = command.split('add task')[1].strip()
        print(f"Added task: {task}")
        taskManager.add_task(task)

    elif lower_command == 'view tasks':
        taskManager.view_tasks()

    elif lower_command.startswith('complete task'):
        keyword = command.split('complete task')[1].strip()
        taskManager.complete_task(keyword)

    elif lower_command.startswith('view task'):
        keyword = command.split('view task')[1].strip()
        pprint(taskManager.get_tasks_by_keyword(keyword))

    elif 'shuffle' == lower_command:
        spotifyControls.shuffle()

    elif lower_command.startswith("volume up"):
        try:
            amount = lower_command.split("volume up")[1]
            if amount:
                spotifyControls.volume_up(int(amount))
            else:
                spotifyControls.volume_up()
        except:
            print("Error Turning Volume Up")

    elif lower_command.startswith("volume down"):
        try:
            amount = lower_command.split("volume down")[1]
            if amount:
                spotifyControls.volume_down(int(amount))
            else:
                spotifyControls.volume_down()
        except:
            print("Error Turning Volume Down")

    elif lower_command.startswith("volume set"):
        try:
            amount = int(command.split("volume set")[1].strip())
            spotifyControls.volume_set(amount)
        except:
            print("Error Setting Volume")

    elif lower_command == "restart":
        try:
            spotifyControls.restart()
        except:
            print("Error pulling up this chune")

    elif lower_command.startswith("count completed task"):
        print(f"{taskManager.count_complete_tasks()} Tasks Completed")

    elif lower_command.startswith("count incomplete task"):
        print(f"{taskManager.count_incomplete_tasks()} Tasks Incomplete")

    elif lower_command.startswith("count total task"):
        print(f"{taskManager.count_total_tasks()} Tasks in Total")

    elif lower_command == "clear tasks":
        taskManager.clear()

    elif lower_command.startswith("type"):
        content = command.strip("type")
        pg.write(content)

    elif lower_command == 'enter':
        pg.press('enter')

    elif lower_command == 'scroll up':
        pg.scroll(clicks=1000)
    elif lower_command == 'scroll down':
        pg.scroll(clicks=-1000)

    elif lower_command == 'now playing':
        song = spotifyControls.now_playing()
        ans = (GPT_Engine.answer_question(f"{song} what song is this?"))
        print(ans)

    elif lower_command.startswith("ask question"):
        question = command.split("ask question")[1].strip()
        ans = GPT_Engine.answer_question(question)
        print(ans)

    elif lower_command.startswith("translate"):
        query = command.replace("translate", "").split("lang=")
        # print(query)
        string = query[0]
        lang = query[1]
        ans = basic.translate(string, lang)
        print(ans)

    elif lower_command.startswith("write email"):
        # print(command)
        first_split = command.replace("write email", "").split("SUBJECT=")
        body = first_split[0].strip()
        second_split = first_split[1].split("TO=")
        receiverName = second_split[1].strip()
        # print(receiverName)
        receiverEmail = contactManager.get_contact_email(receiverName)
        subject = second_split[0].strip()
        if receiverEmail:
            print(f"Email written Successfully\nSubject: {subject}\nRecipient: {receiverEmail}\nBody: {body}")
            contactManager.current_email = {"receiver": receiverEmail, "subject": subject, "body": body}

    elif lower_command.startswith("send email"):
        if contactManager.current_email:
            contactManager.send_email(**contactManager.current_email)
            print(f"Email {contactManager.current_email.get('subject')} Sent Successfully")
            contactManager.current_email.clear()
        else:
            print("No email ready to be sent")

    elif lower_command.startswith("search subject"):
        keyword = command.replace("search subject", '').strip()
        emailReader.search_subjects(keyword)

    elif lower_command.startswith("search sender"):
        keyword = command.replace("search sender", '').strip()
        emailReader.search_sender(keyword)

    elif lower_command.startswith("read email"):
        q = command.replace("read email","").strip()
        if q.isnumeric():
            emailReader.read_idx(int(q))
        else:
            emailReader.read_keyword(q)

    else:
        return True
