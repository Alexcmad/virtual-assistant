import openai
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv("GPT_SECRET")
openai.api_key = api_key


def refresh_history():
    with open("../test_context", 'r') as file:
        ctx = file.read()
    task_list = open("../tasks.json", "r").read()
    new_history = [{"role": "user", "content": ctx},
                   {"role": "assistant", "content": "now playing"},
                   {"role": "user", "content": f"these are all my tasks {task_list}."}]
    return new_history


message_history = refresh_history()


def interpret_command_gpt_TURBO(command):
    message_history.append({"role": "user", "content": command})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        temperature=0
    )
    comp = completion['choices'][0]['message']['content']
    message_history.append({"role": "assistant", "content": comp})
    return comp


def interpret_command_davinci(command):
    completion = openai.Completion.create(
        model="davinci:ft-personal-2023-04-11-08-33-03",
        prompt=command,
        temperature=0
    )
    comp = completion['choices'][0]['text'].split("\n")[0].strip()
    return comp



def answer_question(question):
    msg = {"role": "user", "content": f"{question} in 50 words or less"}
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[msg],
                                              max_tokens=50)
    answer = completion['choices'][0]['message']['content']
    return answer


# pprint(interpret_command_davinci("Who was in paris? ->"))