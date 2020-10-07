# Jason Assistant

This is an assistant (named Jason after the .json data it receives from Telegram) I wrote to help me in my day-to-day life.
It uses Telegrams Bot API to send and receive messages, which is how I interact with the assistant.
It is written entirely in python and runs at all times on a Raspberry Pi on my desk.
It uses a few different API's to get info for me (see features section), and in integrated with IFTTT and WebHooks to control the lights in my room.

## Features

- Responds to variations of 'hi' and 'thanks'
- See this list of functions
> help

>what can you do?
- Can remind you when to leave to get home by a certain time
> home by {hour}:{minute}
- Can remind you to do something after a defined amount of minutes
> remind me in {x} minutes to do {string of any length}
- Can turn my bedroom light on or off
> turn my light on/off
- Execute one of these commands when I get home
> when I get home {function}
- Execute one of these commands after a certain amount of time
> in {x} minutes {function}
- Execute an array of commands at a certain time, intuitively decides which am/pm the user means
> at {hour}:{minute} {comma separated list of functions}
- Get the top headlines in Australia from today
> what's new
- Get the newest headlines about a given topic
> what's new with {topic}
- Do a speedtest for the home WiFi
> do a speedtest
- Shut down the assistant (only if no other tasks are pending)
> go to sleep
- Update the assistant, pulls files from github and then restarts the program
> restart