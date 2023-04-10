import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GPT_SECRET")
openai.api_key=api_key


def interpret_command(command):
    ctx = ''
    with open("../context",'r') as file:
        ctx = file.read()
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": ctx},
                    {"role":"assistant","content":"Hey Lex"},
                    {"role":"user","content": command+" ->"}]
    )
    return completion['choices'][0]['message']['content']