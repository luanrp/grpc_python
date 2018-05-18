#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, time

import grpc

from push_mode.push_pb2 import SubmitRequest
from push_mode.push_pb2_grpc import MessageSyncStub


def run():
    conn = grpc.insecure_channel("localhost:8081")
    client = MessageSyncStub(channel=conn)
    for i in range(1, 10000000):
        client.SubmitMessage(SubmitRequest(channel="aaaa", message=str(time())))
        sleep(0.1)


if __name__ == '__main__':
    run()
