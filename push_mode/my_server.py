#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep
import grpc
from concurrent import futures

import threading

from push_mode.push_pb2 import SubmitReply, MessageReply
from push_mode.push_pb2_grpc import MessageSyncServicer, add_MessageSyncServicer_to_server


class MessageSync(MessageSyncServicer, threading.Thread):
    def __init__(self, cond):
        super(MessageSync, self).__init__()
        self.cond = cond
        self.count = 1
        self.cond_map = {}
        self.message_stack_map = {}

    def SubmitMessage(self, request, context):
        if not self.cond_map.has_key(request.channel):
            self.cond_map[request.channel] = threading.Condition()

        if not self.message_stack_map.has_key(request.channel):
            self.message_stack_map[request.channel] = list()
        self.message_stack_map[request.channel].append(request.message)

        with self.cond_map[request.channel]:
            self.cond_map[request.channel].notifyAll()
        return SubmitReply(reply='received')

    def PushMessageStream(self, request, context):
        print(request.channel)
        if not self.cond_map.has_key(request.channel):
            self.cond_map[request.channel] = threading.Condition()

        while True:
            self.count += 1
            if self.message_stack_map.has_key(request.channel) and self.message_stack_map[request.channel].__len__():
                yield MessageReply(message=str(self.message_stack_map[request.channel].pop()))

            with self.cond_map[request.channel]:
                self.cond_map[request.channel].wait()


def serve():
    grpcserver = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    cond = threading.Condition()
    m = MessageSync(cond)

    add_MessageSyncServicer_to_server(m, grpcserver)
    grpcserver.add_insecure_port('0.0.0.0:8081')
    grpcserver.start()

    sleep(1000000)


if __name__ == '__main__':
    serve()
