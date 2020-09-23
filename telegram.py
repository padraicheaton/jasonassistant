import requests

bot_token = '1250953983:AAHZcezaGT8mqHBSZ1doWb5m3Y4Apa2YgbY'
bot_chatID = '1304413590'

offset = 0

try:
    checkResponse = requests.get('https://api.telegram.org/bot' + bot_token + '/getUpdates')
    checkJson = checkResponse.json()
    messageArr = checkJson["result"]
    lastUpdateId = messageArr[len(messageArr) - 1]['update_id']
    offset = int(lastUpdateId)
except requests.exceptions.ConnectionError:
    print("Can't connect to the internet")


def send_text(message):
    print("Sending \"" + message + "\"\n")

    if len(message) >= 4096:
        send_text("Requested message was too long...")
        return

    http_message = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    try:
        response = requests.get(http_message)
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Can't connect to the internet")


def get_most_recent_message():
    http_message = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=' + str(offset)

    try:
        response = requests.get(http_message)
        jsonMessage = response.json()

        messageArray = jsonMessage["result"]

        message = messageArray[len(messageArray) - 1]['message']['text']

        if len(messageArray) >= 98:
            send_text("I'm getting a little tired, might need to have a nap soon...\n\nMessage Bank is too full, "
                      "restart to reset offset")

        return message
    except requests.exceptions.ConnectionError:
        print("Can't connect to the internet")
