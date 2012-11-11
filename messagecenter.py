"""
This module offers a few classes for IPC through unnamed pipes.
We're using this to communicate between the wxPython instance and
Panda3D instances.


Basically every P3D app has a wx.Panel that serves as a host for the P3D
window. The P3D app gets a pipe which it should wrap with a MessageClient,
add a listener and call the process method of the MessageClient a few times a
second. Same applies to the wx.Panel side. The difference is that the host
wx panel and the messageserver run in the same process, thus using real pipes
would be slow. We use a FakePipe for that channel.

All pipes are connected to MessageServer and the server reads the recievers
attribute of each message and forwards it. Recievers can either be one client,
multiple or something like ALL (including the sender) or OTHERS.


Communication partners in the regular case:


[editor gui]   [game gui]   <- both are wx Panels
     \            /
      \          /
    [MessageServer]
      /          \ 
     /            \ 
  [editor]      [game]     <- corresponding P3D apps


The naming convention (containers with appended " gui") is important so that
P3D apps can send messages to their containers in the GUI.

All wiring of pipes with the server is done from wx, since wx spawns P3D apps.
"""

import collections

# reciever types
ALL, OTHERS = range(2)

# request types.
# If multiple classes of a type are needed, it might be a good idea to create
# superclasses that carry the attribute
LOG, UI, COMMAND = range(3)

class UIRequest(object):
    """UI Requests are not saved in a history. They're only used for
    the user interface.
    """
    req_type = UI

    def __init__(self, command, args=[]):
        self.command = command
        self.args = args

class CommandRequest(object):
    """Abstract class.
    Do not instantiate this class. It's only meant for subclassing.

    CommandRequest subclasses stand for a function each. The function has
    to be implemented and called by the recievers, though.
    """
    req_type = COMMAND

    def __init__(self):
        self.undo = None

class AddGameObjectRequest(CommandRequest):
    """Create a game object with the default name and save the submitted
    id as reference.
    """
    def __init__(self, idnr):
        CommandRequest.__init__(self)
        # idnr stands for id number
        CommandRequest.__init__(self)
        self.idnr = idnr

class RemoveGameObjectRequest(object):
    def __init__(self, idnr):
        CommandRequest.__init__(self)
        self.idnr = idnr


def FakePipe():
    """Simulated pipe for communicating inside one process, where
    race conditions can't occur.
    """
    con1 = FakeConnection()
    con2 = FakeConnection()
    con1.query2 = con2.query1
    con2.query2 = con1.query1
    return con1, con2

class FakeConnection(object):
    """Used by FakePipe only. Not really usable otherwise."""
    def __init__(self):
        self.query1 = []
        self.query2 = []

    def send(self, payload):
        self.query2.append(payload)

    def recv(self):
        return self.query1.pop()

    def poll(self):
        return self.query1 != []


class Message(object):
    """This is what gets sent through the pipe.
    It contains information about recievers and a payload.
    """
    def __init__(self, recievers, payload):
        """Arguments:
        if recievers is an integer, it is expected to be ALL or OTHERS
        if it is a string, it's considered a name of a client
        if it is another iterable, it should be a list of strings which are
        considered to be client names

        payload should be one of the Request ckasses.
        """
        self.recievers = recievers
        self.payload = payload

class MessageClient(object):
    """One end of a pipe. This is the preferred way of using a pipe."""
    def __init__(self, pipe):
        """Pipe should be a multiprocessing.Pipe, but can actually be anything
        that has the methods send, poll and recv - e.g. FakePipe.
        """
        self.pipe = pipe
        self.listeners = []

    def addListener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def removeListener(self, listener):
        self.listeners.remove(listener)

    def sendMessage(self, message):
        self.pipe.send(message)

    def broadcast(self, payload):
        """Convenience method.
        Send a message to everybody, including the sender with the
        specified payload. Most of the time you won't need this.
        """
        m = Message(recievers=ALL, payload=payload)
        self.pipe.send(m)

    def multicast(self, recievers, payload):
        """Convenience method.
        Send a message to multiple recievers with the specified payload.
        """
        assert not isinstance(recievers, basestring) and \
            isinstance(recievers, collections.Iterable)
        m = Message(recievers=recievers, payload=payload)
        self.pipe.send(m)

    def unicast(self, reciever, payload):
        """Convenience method.
        Send a message to one reciever.
        """
        assert isinstance(reciever, basestring)
        m = Message(recievers=reciever, payload=payload)
        self.pipe.send(m)

    def others(self, payload):
        """Convenience method.
        Send a message to all others.
        """
        m = Message(recievers=OTHERS, payload=payload)
        self.pipe.send(m)

    def process(self, *args, **kwargs):
        while self.pipe.poll():
            message = self.pipe.recv()
            for listener in self.listeners:
                listener(message)

class MessageServer(object):
    """Connection of all pipes which processes forwarding.
    There should be only one server.
    """
    def __init__(self):
        self.pipes = {}

    def connectPipe(self, name, pipe):
        self.pipes[name] = pipe

    def detachPipeByName(self, name):
        del self.pipes[name]

    def detachPipe(self, pipe):
        for name in self.pipes.keys():
            if self.pipes[name] == pipe:
                del self.pipes[name]

    def process(self, *args, **kwargs):
        """Process all messages. This method should be called often."""
        for name, pipe in self.pipes.iteritems():
            while pipe.poll():
                message = pipe.recv()

                if message.payload.req_type == LOG:
                    #print "log ",message.payload
                    pass
                elif message.payload.req_type == COMMAND:
                    #print "command ", message.payload
                    pass

                if isinstance(message.recievers, int):
                    # must be ALL or OTHERS
                    if message.recievers == ALL:
                        for p in self.pipes.items():
                            p.send(message)
                    elif message.recievers == OTHERS:
                        recievers = dict(self.pipes)
                        # remove the pipe we are reading from
                        del recievers[name]
                        message.recievers = recievers.keys()
                        for r in recievers.values():
                            r.send(message)
                    else:
                        raise StandardError("fail1")

                elif isinstance(message.recievers, basestring):
                    # must be a reciever name
                    if message.recievers == name:
                        # Someone sent a message to himself. Discard it
                        print ("Message from {} was not delivered,"
                              " because it was sent to itself.").format(name)
                        continue
                    if message.recievers in self.pipes.keys():
                        # TODO: why the fuck does this not work?! WRRRAAARRGH *trollface*
                        self.pipes[message.recievers].send(message)
                    else:
                        raise StandardError("fail2")

                elif isinstance(message.recievers, collections.Iterable):
                    # must be a list of reciever names
                    for rec in message.recievers:
                        if rec in self.pipes.keys():
                            self.pipes[rec].send(message)
                        else:
                            raise StandardError("fail3")

# set global instance
messageserver = MessageServer()


# Test
# TODO: rewrite this!
if __name__ == "__main__":
    p1 = FakePipe() # A
    p2 = FakePipe() # B

    pay = CommandRequest(lambda: True)
    m = Message()
    m.recievers = "B"
    m.payload = pay
    p1.send(m)
    p1.send(m)

    ms = MessageServer()
    ms.connectPipe("A", p1)
    ms.connectPipe("B", p2)

    ms.process()
    assert p2.recv() is not None
    print p1.query, p2.query