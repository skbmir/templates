import tornado.ioloop
import tornado.gen
import time
from nats.io.client import Client as NATS
import msgpack

@tornado.gen.coroutine
def main():
    nc = NATS()

    options = {
        "servers": ["nats://192.168.0.114:4222"],
        "user": "stdbreaks",
        "password": "std#32",
        "tcp_nodelay": True
    }

    # Establish connection to the server.
    yield nc.connect(**options)

    @tornado.gen.coroutine
    def message_handler(msg):
        subject = msg.subject
        data = msg.data
        cmd = msgpack.unpackb(data)
        print("[Received on '{}'] : {}".format(subject, cmd))

    # Simple async subscriber
    sid = yield nc.subscribe("cmd", cb=message_handler)

    yield nc.publish("cmd", "test")

if __name__ == '__main__':
    main()
    tornado.ioloop.IOLoop().current().start()