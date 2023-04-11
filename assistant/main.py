import openai.error
import speech_recognition.exceptions
import speech_recognition as sr
from assistant import GPT_Engine, commands


r = sr.Recognizer()
mic = sr.Microphone(device_index=2)

msg_limit = 5


def use_turbo():
    count = 0
    while True:
        if count > msg_limit - 1:
            GPT_Engine.message_history = GPT_Engine.refresh_history()
            print("[Command History has been Reset]")
            count = 0
        try:
            command = input(f"{count + 1}/{msg_limit}: Command -> ").lower()

            if command in ["reset", "thank you", "thanks"]:
                count = msg_limit

            elif commands.execute_command(command):

                gpt_parsing: str = GPT_Engine.interpret_command_gpt_TURBO(f"{command} ->").lower()
                gpt_parsed_command = gpt_parsing.split('->')[0].strip().strip(".")
                command = gpt_parsed_command
                if commands.execute_command(command):
                    print(command)
                    print("[The Previous Response was not a valid command therefore no action was taken]")

        except Exception as e:
            print("Assistant ran into an Error")
            print(e)
        count += 1


def use_davinci():
    while True:
        try:
            command = input("Command -> ")
            gpt_parsed_command: str = GPT_Engine.interpret_command_davinci(f"{command} ->").lower()
            if commands.execute_command(gpt_parsed_command):
                print(gpt_parsed_command)
                print("[The model tried to execute the above command and it didn't work]")
        except Exception as e:
            print("Assistant ran into an Error")
            print(e)

def choose_model():
    model = input("Choose model to use:\n"
                  "[0] - GPT-3 Davinci Fine tuned model (Cheap but dull and slightly pricey to train) <-- Default\n"
                  "[1] - GPT-3.5-Turbo (Expensive but more creative)\n"
                  "> ")
    if model == "1":
        use_turbo()
    else:
        use_davinci()
def listen():
    while True:
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                command = r.recognize_google(audio)
                if command:
                    print(command)
                    return command
                else:
                    continue

            except Exception as e:
                print(e)


choose_model()