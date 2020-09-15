import telegram
import responses
import time as delay
from threading import Thread
import random
import subprocess

print("\nJason V2\nBooting Up...\n")


def listen():
    wakings = [
        "Hey, I'm awake :)",
        "I'm up and ready to go!",
        "Just sat down with my coffee, ready to work!",
        "Just sat down with my coffee, ready to work!",
        "I'm here! Let me know if you need anything :)",
        "What's up mate, how can I help?",
        "Hey! Long time no see"
    ]

    responses.say(random.choice(wakings))
    print("Waiting for your messages...\n")
    last_message = telegram.get_most_recent_message()

    while True:
        delay.sleep(10)
        msg = telegram.get_most_recent_message()

        if msg == last_message or msg is None:
            continue

        last_message = msg
        print("User said: " + msg)

        if msg == "go to sleep":
            if responses.go_to_sleep():
                break
        if msg == "restart":
            responses.say("Let me check for updates, then I'll start back up again...")
            subprocess.Popen(["./runassistant.sh"])
            break
        else:
            responses.react_to(msg)


main_thread = Thread(target=listen)
main_thread.start()
