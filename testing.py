string = "remind me in 30 minutes to go home"

splitString = string.split()
minutes = int(splitString[3])
message = ""
for x in range(len(splitString)-6):
    message += splitString[x+6] + " "

print(message)
