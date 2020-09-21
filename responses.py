import telegram
from datetime import time, datetime, timedelta
import time as delay
import threading
import ifttt
import random
import re
import subprocess

homeStatementComparison = re.compile('home by.+')
remindMeToComparison = re.compile('remind me in.+ minutes to.+')
lightComparison = re.compile('turn my light.+')
homeFuncComparison = re.compile('when I get home.+')
executeAfterTimeComparison = re.compile('in.+minutes.+')


def react_to(msg):
    functions = [
        "Say Hi ('hi')",
        "Say Thanks ('thanks')",
        "Ask me to remind you to go home ('home by hour:minute')",
        "Ask me to remind you to do something ('remind me in {x} minutes to {something}')",
        "Ask me to turn your light on or off ('turn my light on/off')",
        "Get me to do something when you get home ('when I get home {function}')",
        "Get me to do something after some time ('in {x} minutes {function}')",
        "Tuck me into bed/Shut down ('go to sleep')",
        "Bring up this menu ('help/what can you do?')"
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

    if msg == "help" or msg == "what can you do?":
        functionString = "Well, I can do all of this:\n"
        for function in functions:
            functionString += " - " + function + "\n"
        say(functionString)

    elif msg == "hi" or msg == "hi jason" or msg == "hey" or msg == "hey jason":
        say(random.choice(greetings))

    elif bool(re.match(homeStatementComparison, msg)):
        splitMessage = msg.split()
        timeArray = splitMessage[len(splitMessage) - 1].split(':')
        hour = int(timeArray[0])
        minute = int(timeArray[1]) if len(timeArray) > 1 else 0
        go_home_reminder(hour, minute)

    elif msg == "thanks jason" or msg == "thanks":
        say(random.choice(thanks))

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
        thread = threading.Thread(target=remind_in, args=(minutes, message.strip()))
        thread.start()

    elif bool(re.match(lightComparison, msg)):
        splitString = msg.split()
        operation = splitString[len(splitString) - 1]
        if operation == 'on':
            turn_light_on()
        elif operation == 'off':
            turn_light_off()

    elif bool(re.match(homeFuncComparison, msg)):
        splitString = msg.split()
        spoofMessage = ""
        for i in range(len(splitString)-4):
            spoofMessage += splitString[i+4] + " "
        spoofMessage = spoofMessage.strip()
        minutes = 1
        thread = threading.Thread(target=execute_when_return_home, args=(spoofMessage, minutes))
        thread.start()

    elif bool(re.match(executeAfterTimeComparison, msg)):
        splitString = msg.split()
        minutes = int(splitString[1])
        command = ""
        for i in range(len(splitString)-3):
            command += splitString[i+3] + " "
        say("I'll execute '" + command.strip() + "' after " + str(minutes) + " minutes")
        thread = threading.Thread(target=do_after, args=(command.strip(), minutes))
        thread.start()

    elif msg == "test error":
        number = 10
        say("the number is " + number)

    else:
        confusedResponse = random.choice(confusions) + "\n\nI didn't understand '" + msg + "', You can say 'help' for a list of what I'll respond to"
        say(confusedResponse)


def say(message):
    telegram.send_text(message)


def go_home_reminder(hour, minute):
    suffix = 'am'
    remindHour = hour

    if datetime.now().time() > time(12, 00):
        remindHour += 12
        suffix = 'pm'

    reminder_time = time(remindHour-1, minute)

    say("Okay, I will remind you to go home at " + str(hour-1) + ":" + str(minute) + suffix)

    thread = threading.Thread(target=send_reminder_at, args=(reminder_time, "You've got an hour to get home!! You might have to text mum too", True))
    thread.start()


def remind_in(minutes, message):
    say("I'll remind you to '" + message + "' in " + str(minutes) + " minutes")
    delay.sleep(minutes * 60)
    say("Hey! You need to " + message)


def send_reminder_at(given_time, message, home_remind=False):
    while True:
        if datetime.now().time() > given_time:
            say(message)
            if home_remind:
                remind_in(30, "get your ass home")
            break


def turn_light_on():
    ifttt.send_to_ifttt('switched_on')
    say("I've turned your light on for you")


def turn_light_off():
    ifttt.send_to_ifttt('switched_off')
    say("Lights off then")


def do_after(command, minutes):
    delay.sleep(minutes * 60)
    react_to(command)


def execute_when_return_home(command, minutes):
    PhoneIP = '192.168.0.171'

    proc = subprocess.Popen(["ping", PhoneIP], stdout=subprocess.PIPE)
    print("Waiting to execute '" + command + "' when the user gets home")

    say("When you get home, I'll execute '" + command + "'")

    delay.sleep(minutes)

    while True:
        line = proc.stdout.readline()
        if not line:
            break

        response = line.decode('utf-8')

        if "ttl" in response:
            say("Welcome home!")
            react_to(command)
            break


def go_to_sleep():
    if threading.active_count() <= 2:
        say("Good night, I'll see you later!")
        print("\nAssistant shut down by user")
        return True
    else:
        say("There are still some things you've asked me to do that I haven't done yet, so I'll stay up tyvm")
        return False
