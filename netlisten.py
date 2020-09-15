import subprocess
import responses


PhoneIP = '192.168.0.171'


def execute_when_return_home(command):
    proc = subprocess.Popen(["ping", PhoneIP], stdout=subprocess.PIPE)
    print("Waiting to execute '" + command + "' when the user gets home")

    responses.say("When you get home, I'll execute '" + command + "'")

    while True:
        line = proc.stdout.readline()
        if not line:
            break

        response = line.decode('utf-8')

        if "ttl" in response:
            responses.react_to(command)
            break
