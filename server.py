from time import sleep
import grpc
from concurrent import futures

import threading

from push_mode import SubmitReply, MessageReply, MessageSyncServicer, add_MessageSyncServicer_to_server, LogInReply


class MessageSync(MessageSyncServicer, threading.Thread):
    def __init__(self, cond):
        super(MessageSync, self).__init__()
        self.cond = cond
        self.amount_users = 0
        self.users = []
        self.count = 1
        self.cond_map = {}
        self.message_stack_map = {}

    def SubmitMessage(self, request, context):
        if request.name not in self.users:
            self.cond_map[request.channel] = threading.Condition()
            self.amount_users += 1
            self.users.append(request.name)

        if request.channel not in self.message_stack_map:
            self.message_stack_map[request.channel] = list()

        text = f"{request.time}. {request.name} написал: {request.header}.\n{request.message}"
        self.message_stack_map[request.channel].append(text)

        with self.cond_map[request.channel]:
            self.cond_map[request.channel].notifyAll()
        return SubmitReply(reply='received')

    def PushMessageStream(self, request, context):
        print(request.channel)
        if request.channel not in self.cond_map:
            self.cond_map[request.channel] = threading.Condition()

        while True:
            self.count += 1
            if request.channel in self.message_stack_map and self.message_stack_map[request.channel].__len__():
                yield MessageReply(message=str(self.message_stack_map[request.channel][0]))
                self.amount_users -= 1
                if self.amount_users <= 0:
                    self.message_stack_map[request.channel].pop()
                    self.amount_users = len(self.users)

    def LogIn(self, request, context):
        if request.name not in self.users:
            self.users.append(request.name)
        return LogInReply(reply="Successful log in")

def serve():
    grpcserver = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    cond = threading.Condition()
    m = MessageSync(cond)

    add_MessageSyncServicer_to_server(m, grpcserver)
    grpcserver.add_insecure_port('0.0.0.0:8080')
    grpcserver.start()

    sleep(1000000)


if __name__ == '__main__':
    serve()