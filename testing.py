import requests


def send_to_ifttt(event):
    url = 'https://maker.ifttt.com/trigger/' + event + '/with/key/jfRaKs196E7wf4oJWHIa2GA1RoEG4HwBTQJ6b19tvVl'
    requests.get(url)


send_to_ifttt('switched_off')
