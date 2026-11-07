from modules.speech_to_text import listen
from modules.command_handler import execute
from modules.text_to_speech import speak

speak("Kaabo. Emi ni Oluranlọwọ Yoruba.")

while True:

    text = listen()

    if text != "":

        execute(text)