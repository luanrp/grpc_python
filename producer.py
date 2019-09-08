#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, time

import grpc

from push_mode import SubmitRequest, MessageSyncStub


def run():
    conn = grpc.insecure_channel("localhost:8080")
    client = MessageSyncStub(channel=conn)
    for i in range(1, 10000000):
        client.SubmitMessage(SubmitRequest(channel="aaaa", message=str(time())))
        sleep(0.1)


if __name__ == '__main__':
    run()
