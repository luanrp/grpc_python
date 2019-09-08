#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep
import grpc
from concurrent import futures

import threading

from push_mode import SubmitReply, MessageReply, MessageSyncServicer, add_MessageSyncServicer_to_server


class MessageSync(MessageSyncServicer, threading.Thread):
    def __init__(self, cond):
        super(MessageSync, self).__init__()
        self.cond = cond
        self.count = 1
        self.cond_map = {}
        self.message_stack_map = {}

    def SubmitMessage(self, request, context):
        if request.channel not in self.cond_map:
            self.cond_map[request.channel] = threading.Condition()

        if request.channel not in self.message_stack_map:
            self.message_stack_map[request.channel] = list()
        self.message_stack_map[request.channel].append(request.message)

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
                yield MessageReply(message=str(self.message_stack_map[request.channel].pop()))

            with self.cond_map[request.channel]:
                self.cond_map[request.channel].wait()


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
