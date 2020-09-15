import subprocess


PhoneIP = '192.168.0.171'


def execute_when_return_home(func, command):
    proc = subprocess.Popen(["ping", "-t", PhoneIP], stdout=subprocess.PIPE)
    print("Waiting to execute '" + command + "' when the user gets home")

    while True:
        line = proc.stdout.readline()
        if not line:
            break

        response = line.decode('utf-8')

        if "TTL" in response:
            func(command)
            break
