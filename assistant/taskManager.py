from tinydb import TinyDB, Query
from assistant.schemas import Task
from pprint import pprint
from assistant.basic import match_substring
import speech_recognition as sr
from datetime import datetime
import re

db = TinyDB('../tasks.json')
Tasks = Query()
r = sr.Recognizer()
mic = sr.Microphone()


def add_task(task):
    new_task = Task(**{"content": task})
    task_data = new_task.dict()
    db.insert(task_data)


def view_tasks():
    for item in db:
        i = {"content": item['content'],
             "completed":item['completed']}
        pprint(i)


def clear():
    db.truncate()


def get_tasks_by_keyword(keyword: str):
    task = db.search(Tasks.content.search(keyword, flags=re.IGNORECASE))

    while len(task) > 2:
        print("There are more than 2 results for this keyword. Please specify another keyword to "
              "refine the search: ")
        task = refine_search(listen(),task)

    if len(task) == 2:
        print(f"There are 2 matching results. Do you mean '{task[0]['content']}' or '{task[1]['content']}' ?")
        choice = listen()
        if match_substring(choice,task[0]['content']):
            return task[0]
        elif match_substring(choice,task[1]['content']):
            return task[1]
        else:
            print("Keyword not found")
    if task:
        return task[0]
    else:
        return []


def refine_search(keyword: str, initial_search: list):
    result = []
    for i in initial_search:
        if re.search(keyword, i['content'], flags=re.IGNORECASE):
            result.append(i)
    return result


def complete_task(keyword):
    task = get_tasks_by_keyword(keyword)
    if task:
        if not task['completed']:
            db.update({'completed': True, 'completed_at': datetime.now().isoformat()}, Tasks.content == task['content'])
            print("Task Completed")
        else:
            print("Task Already Completed")
    else:
        print(f"Could not find task containing keyword '{keyword}'")


def count_complete_tasks():
    return db.count(Tasks.completed == True)


def count_incomplete_tasks():
    return db.count(Tasks.completed == False)


def count_total_tasks():
    return len(db)


def listen():
    """with mic as source:
        print("Listening: ")
        try:
            audio = r.listen(source)
            keyword = r.recognize_google(audio)
            return keyword
        except:
            return"""
    return input("Keyword: ")
