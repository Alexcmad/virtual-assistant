import openai
from dotenv import load_dotenv
import os

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


def interpret_command(command):
    message_history.append({"role": "user", "content": command})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        temperature=0
    )
    comp = completion['choices'][0]['message']['content']
    message_history.append({"role": "assistant", "content": comp})
    return comp


def answer_question(question):
    msg = {"role": "user", "content": f"{question} (50 words or less)"}
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                       messages=[msg],
                                              max_tokens=50)
    answer = completion['choices'][0]['message']['content']
    return answer
