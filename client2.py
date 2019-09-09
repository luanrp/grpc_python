import datetime
import grpc
import threading

from time import sleep
from push_mode import SubmitRequest, MessageSyncStub, ConnRequest, LogInRequest, HistoryRequest


def listen(client):
    while True:
        response = client.PushMessageStream(ConnRequest())
        for r in response:
            print(r.message)


def run():
    conn = grpc.insecure_channel("localhost:8080")
    client = MessageSyncStub(channel=conn)

    thread = threading.Thread(target=listen, args=(client,))
    thread.start()

    name = input("Введите ваше имя: ")
    response = client.LogIn(LogInRequest(name=name))
    print(response.reply)
    print(client.GetHistory(HistoryRequest(name=name)).message)

    while True:
        header = input("Bведите заголовок: ")
        msg = input("Введите сообщение: ")
        curr_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        client.SubmitMessage(SubmitRequest(name=name, header=header, message=msg, time=curr_time))
        sleep(0.1)


if __name__ == '__main__':
    run()
