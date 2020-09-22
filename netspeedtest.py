import speedtest
import responses


def perform_test():
    servers = []

    test = speedtest.Speedtest()
    test.get_servers(servers)
    test.get_best_server()
    test.download()
    test.upload(pre_allocate=False)
    test.results.share()

    results_dict = test.results.dict()

    downSpeed = round(results_dict['download'] / 1000000, 2)
    upSpeed = round(results_dict['upload'] / 1000000, 2)
    ping = round(results_dict['ping'])

    message = "Speedtest Results:\nPing: " + str(ping) + "\nDownload: " + str(downSpeed) + "\nUpload: " + str(upSpeed)

    responses.say(message)
