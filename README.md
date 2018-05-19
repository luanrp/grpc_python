# grpc_python

## What's This
This a demo to show how to make a message push channel based on grpc. One or several message producers can submit message to a given channel, once the message is received, it will be pushed to the consumer. 

## Background 
Based on my specific requirements, there is a cloud server hosting my SAAS platform, and there are several hosts deployed in different locations. Messages will be submitted via APP/mobile to SAAS and then routed to the hosts. 

In Java, a netty based channel works perfect on such scenario. With Python, I guess grpc will be the fastest way. Leave me message if there are better solutions.

## Design
```angular2html
service MessageSync {
  // message producer
  rpc SubmitMessage (SubmitRequest) returns (SubmitReply) {}

  // message consume, push mode
  rpc PushMessageStream(ConnRequest) returns (stream MessageReply){}
}
```

- The producer can use ```SubmitMessage``` to publish message, including the channel name(I use the channel name to identify which host to receive the message), and the message.
```angular2html
message SubmitRequest {
  string channel = 1;
  string message = 2;

```

- The consumer can use PushMessageStream to register the channel. 
```angular2html
message ConnRequest {
  string channel = 1;
}

```
Once registered, the message will be received: 
```angular2html
        response = client.PushMessageStream(ConnRequest(channel="aaaa"))

        for r in response:
            print(r.message)
```

## TODO
This is a quick demo; more work should be done if you wanna make a robust product: e.g., 
- Connection retry for server/client error. 
- One message can only be pushed to one consumer. That meets my requirement. It will be easy to introduce a pub/sub model into the current demo.


By A Python starter.