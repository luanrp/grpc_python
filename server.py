from time import sleep
import grpc
from concurrent import futures

import threading

from push_mode import SubmitReply, MessageReply, MessageSyncServicer, add_MessageSyncServicer_to_server, LogInReply, HistoryReply


class MessageSync(MessageSyncServicer, threading.Thread):
    def __init__(self, cond):
        super(MessageSync, self).__init__()
        self.amount_users = 0
        self.users = []
        self.message_stack_map = {}
        self.history = ""

    def SubmitMessage(self, request, context):
        if request.name not in self.users:
            self.amount_users += 1
            self.users.append(request.name)

        if request.channel not in self.message_stack_map:
            self.message_stack_map[request.channel] = list()

        text = f"{request.time}. {request.name} написал: {request.header}.\n{request.message}"
        self.message_stack_map[request.channel].append(text)
        self.history += text+'\n'

        return SubmitReply(reply='received')

    def PushMessageStream(self, request, context):
        print(request.channel)

        while True:
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

    def GetHistory(self, request, context):
        return HistoryReply(message="Ранее опубликованные объявления:\n"+self.history)

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