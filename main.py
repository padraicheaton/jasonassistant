import telegram
import responses
import time as delay
import re
from threading import Thread
import random

homeStatementComparison = re.compile('home by.+')
remindMeToComparison = re.compile('remind me in.+ minutes to.+')
setupComparison = re.compile('setup my.+')

print("Jason V1\nBooting Up...\n")


def listen():
    functions = [
        "Say Hi ('hi')",
        "Say Thanks ('thanks')",
        "Ask me to remind you to go home ('home by hour:minute')",
        "Ask me to remind you to do something ('remind me in {x} minutes to {something}')",
        "Ask me to set up a predefined environment ('setup my {env_name}')",
        "Tuck me into bed/Shut down ('go to sleep')",
        "Bring up this menu ('help/what can you do?')"
    ]

    wakings = [
        "Hey, I'm awake :)",
        "I'm up and ready to go!",
        "Just sat down with my coffee, ready to work!",
        "Just sat down with my coffee, ready to work!",
        "I'm here! Let me know if you need anything :)"
    ]

    greetings = [
        "Hi!",
        "Hello there!",
        "Hey!",
        "Hi, good to see you're still alive",
        "Hi, good to see you're still alive"
    ]

    thanks = [
        "No problem :)",
        "Happy to help!",
        "No worries mate",
        "No worries mate",
        "Anytime :)"
    ]

    confusions = [
        "...Sorry, what?",
        "I don't know what that means ;(",
        "...what?",
        "Wanna try that one again mate?"
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

        if msg == "help" or msg == "what can you do?":
            functionString = "Well, I can do all of this:\n"
            for function in functions:
                functionString += " - " + function + "\n"
            responses.say(functionString)

        elif msg == "hi" or msg == "hi jason" or msg == "hey" or msg == "hey jason":
            responses.say(random.choice(greetings))

        elif bool(re.match(homeStatementComparison, msg)):
            splitMessage = msg.split()
            timeArray = splitMessage[len(splitMessage) - 1].split(':')
            responses.go_home_reminder(int(timeArray[0]), int(timeArray[1]))

        elif msg == "thanks jason" or msg == "thanks":
            responses.say(random.choice(thanks))

        elif bool(re.match(remindMeToComparison, msg)):
            splitString = msg.split()
            minutes = int(splitString[3])
            message = ""
            for x in range(len(splitString) - 6):
                word = splitString[x + 6]
                if word == "my":
                    word = "your"
                if word == "I":
                    word = "you"
                if word == "mine":
                    word = "yours"
                if word == "am":
                    word = "are"
                message += word + " "
            responses.remind_in(minutes, message.strip())

        elif bool(re.match(setupComparison, msg)):
            splitString = msg.split()
            responses.setup(splitString[2])

        elif msg == "go to sleep":
            if responses.go_to_sleep():
                break

        else:
            confusedResponse = random.choice(confusions) + "\n\nYou can say 'help' for a list of what I'll respond to"
            responses.say(confusedResponse)


main_thread = Thread(target=listen)
main_thread.start()
