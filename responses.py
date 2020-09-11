import telegram
from datetime import time, datetime, timedelta
import threading
import envsetup


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
    reminder_time = datetime.now()
    reminder_time += timedelta(seconds=minutes*60)

    say("I'll remind you to " + message + " in " + str(minutes) + " minutes")

    thread = threading.Thread(target=send_reminder_at, args=(reminder_time.time(), "Hey! You need to " + message))
    thread.start()


def send_reminder_at(given_time, message, home_remind=False):
    while True:
        if datetime.now().time() > given_time:
            say(message)
            if home_remind:
                remind_in(30, "get your ass home")
            break


def setup(environment):
    success = True

    if environment == "uni" or environment == "university":
        envsetup.setup_uni()
    elif environment == "youtube":
        envsetup.setup_youtube()
    else:
        success = False
        say("I'm not sure I know how that one's set up...")

    if success:
        say("I've set up your " + environment + " environment, it's ready and waiting for you")


def go_to_sleep():
    if threading.active_count() <= 2:
        say("Good night, I'll see you later!")
        print("\nAssistant shut down by user")
        return True
    else:
        say("There are still some things you've asked me to do that I haven't done yet, so I'll stay up tyvm")
        return False
