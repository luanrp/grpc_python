import grpc

from push_mode import ConnRequest, MessageSyncStub


def run():
    conn = grpc.insecure_channel("localhost:8080")
    client = MessageSyncStub(channel=conn)

    try:
        response = client.PushMessageStream(ConnRequest(channel="aaaa"))

        for r in response:
            print(r.message)

    except Exception as e:
        print("exception")


if __name__ == '__main__':
    run()
