"""
This module offers a few classes for IPC through unnamed pipes.
We're using this to communicate between the wxPython instance and
Panda3D instances.

Basically every P3D app has a wx.Panel that serves as a host for the P3D
window. The P3D app gets a pipe which it should wrap with a MessageClient,
add a listener and call the "process" method of the MessageClient a few times
a second. Same applies to the wx.Panel side. The difference is that the host
wx panel and the messageserver run in the same process, thus using real pipes
would be slow. We use a fake pipe for that channel. The server's "process"
function is called from wx, too.

All pipes are connected to MessageServer and the server reads the "recievers"
attribute of each message and forwards it according to that.
Recievers can either be one client, multiple or a group like ALL (including
the sender) or OTHERS.

Communication partners in the regular case:

+-------------------------------------------------------+
|[editor gui]   [game gui]   <- both are wx Panels      |
|     \            /                                    |
|      \          /                                     |   <- WX Process
|    [MessageServer]                                    |
|      /          \                                     |
+---- / -----+---- \ -----------------------------------+
|     |      |     |                                    |
|     |      |     |                                    |  <- Subprocesses
|  [editor]  |    [game]     <- corresponding P3D apps  | (1 for each p3d app)
+------------+------------------------------------------+

The naming convention (panels with appended " gui") is important so that
P3D apps can send messages to their 'containers' in the GUI.

All wiring of pipes with the server is done from wx, since wx spawns P3D apps.
Panda3d only gets a pipe and wraps it into a MessageClient.
"""

import collections

# reciever types
ALL, OTHERS = RECIEVER_TYPES = range(2)

# request types
LOG, UI, COMMAND = REQ_TYPES = range(3)

# request specialisations
ADD_GAME_OBJECT, REMOVE_GAME_OBJECT,\
OPEN_WINDOW, CLOSE_WINDOW, RESIZE_WINDOW, FOCUS_WINDOW = REQ_SPECS = range(6)

class LogRequest(object):
    """Request for logging/printing something."""
    req_type = LOG

class UIRequest(object):
    """UI Requests are not saved in a history. They're only used for
    the user interface.
    """
    req_type = UI

class CommandRequest(object):
    """Commands are all saved in a global history and should be undo-able."""
    req_type = COMMAND


class AddGameObjectRequest(CommandRequest):
    """Create a game object with the default name and save the submitted
    id as reference. It can be renamed in a second step with a
    ComponentAttributeChangeRequest.
    """
    req_spec = ADD_GAME_OBJECT
    def __init__(self, go_id):
        """The id can be any random but unique number.
        You must not use an id of an object that has been created previously.
        """
        self.go_id = go_id

class RemoveGameObjectRequest(CommandRequest):
    req_spec = REMOVE_GAME_OBJECT
    def __init__(self, go_id):
        self.go_id = go_id

class OpenWindowRequest(UIRequest):
    req_spec = OPEN_WINDOW
    def __init__(self, window_id, handle=None, width=500, height=500):
        self.window_id = window_id
        self.handle = handle
        self.width = width
        self.height = height

class CloseWindowRequest(UIRequest):
    req_spec = CLOSE_WINDOW
    def __init__(self, window_id):
        self.window_id = window_id

class ResizeWindowRequest(UIRequest):
    req_spec = RESIZE_WINDOW
    def __init__(self, window_id, width, height):
        self.window_id = window_id
        self.width = width
        self.height = height

class FocusWindowRequest(UIRequest):
    req_spec = FOCUS_WINDOW
    def __init__(self, window_id):
        self.window_id = window_id


# The following code is deprecated since multiprocessing.dummy.connection.Pipe
# offers more or less the same functionality.

# class FakeConnection(object):
#     """Used by FakePipe only. Not really usable otherwise."""
#     def __init__(self):
#         self.query1 = []
#         self.query2 = []

#     def send(self, payload):
#         self.query2.append(payload)

#     def recv(self):
#         return self.query1.pop()

#     def poll(self):
#         return self.query1 != []

# def FakePipe():
#     """Simulated pipe for communicating inside one process, where
#     race conditions can't occur. Tries to copy multiprocessing.Pipe.
#     """
#     con1 = FakeConnection()
#     con2 = FakeConnection()
#     con1.query2 = con2.query1
#     con2.query2 = con1.query1
#     return con1, con2




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

        payload should be one of the Request classes.
        """
        self.recievers = recievers
        self.payload = payload

# TODO: Move this to another module, so that subprocesses don't import yet
# another global messageserver.
class MessageClient(object):
    """One end of a pipe. This is the preferred way of using a pipe."""
    def __init__(self, pipe):
        """Pipe should be a multiprocessing.Pipe or
        multiprocessing.dummy.connection.Pipe (fake pipe).
        """
        self.pipe = pipe
        self.listeners = []
        self.type_listeners = {}

    def addListener(self, listener, req_type=None):
        """Add a listener (function) that is invoked every time a message
        arrives. If req_type is not None, that listener will be activated only
        if a message payload has that request type.
        Every listener can only be used once for a target. So you can't assign
        the same function twice to a specific req_type. You also can't assign
        a listener to all types (req_type=None) more than once. The second try
        will be ignored silently.

        Arguments:
        listener -- a function
        req_type -- one of the request types specified in this module
                    (E.g. UI, COMMAND, LOG). Leave at None for all types.
        """
        if req_type is None:
            if listener not in self.listeners:
                self.listeners.append(listener)
        else:
            if not self.type_listeners.has_key(req_type):
                self.type_listeners[req_type] = []
            if listener not in self.type_listeners[req_type]:
                self.type_listeners[req_type].append(listener)

    def removeListener(self, listener, req_type=None):
        """Remove a listener. If req_type is None, only listeners listening
        to all types will be removed. To remove a listener that listens for
        e.g. req_type=UI you need to specify that.
        This function throws a ValueError if no such listener can be found.
        """
        if req_type is None:
                self.listeners.remove(listener)
        else:
            try:
                self.type_listeners[req_type].remove(listener)
            except KeyError:
                raise ValueError("No such listener")

    def sendMessage(self, message):
        """Send a message through the pipe. Message should be an instance of
        Message. Otherwise there might be problems on the reading side.
        """
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
        assert not isinstance(recievers, basestring)
        assert isinstance(recievers, collections.Iterable)
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
            rt = message.payload.req_type
            if self.type_listeners.has_key(rt):
                for listener in self.type_listeners[rt]:
                    listener(message)


class MessageServer(object):
    """Connection of all pipes which processes forwarding.
    There should be only one server.
    """
    def __init__(self):
        self.pipes = {}

    def connectPipe(self, name, pipe):
        """Neither the name nor the pipe connection must be used already.
        AssertionError is thrown if one of both is the case.
        """
        assert name not in self.pipes.keys()
        assert pipe not in self.pipes.values()
        self.pipes[name] = pipe

    def detachPipe(self, pipe):
        """Detach the pipe from the server, but keep the object alive and
        return it.
        Arguments:
        pipe -- can either be a name or a Connection object
        """
        if isinstance(pipe, basestring):
            con = self.pipes[name]
            del self.pipes[name]
            return con
        for name in self.pipes.keys():
            if self.pipes[name] == pipe:
                con = self.pipes[name]
                del self.pipes[name]
                return con

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
