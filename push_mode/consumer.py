#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grpc
from grpc._channel import _Rendezvous

import push_mode
from push_mode.push_pb2 import ConnRequest
from push_mode.push_pb2_grpc import MessageSyncStub


def run():
    conn = grpc.insecure_channel("localhost:8081")
    client = push_mode.push_pb2_grpc.MessageSyncStub(channel=conn)

    try:
        response = client.PushMessageStream(ConnRequest(channel="aaaa"))

        for r in response:
            print(r.message)
    except _Rendezvous as e:
        # here we can setup some retry mechanism.
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            print("StatusCode.UNAVAILABLE")

        if e.code() == grpc.StatusCode.INTERNAL:
            print("StatusCode.INTERNAL")

    except Exception as e:
        print("exception")


if __name__ == '__main__':
    run()
