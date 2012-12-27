from multiprocessing import Process, Pipe
from multiprocessing.dummy.connection import Pipe as FakePipe

from panda3dinstance import Panda3dInstance
from messagecenter import messageserver, MessageClient, OpenWindowRequest

# TODO: maybe we should only return single objects instead of the
# _Panda3dInstance composite object. E.g. only return a messageclient
# or number of windows depending on a p3d name.
class Panda3dManager(object):
    """There should be only one instance of this class.
    It's designed to be used from the wx process.

    The Panda3D Manager spawns Processes with Panda3D and keeps
    connections to them. It also utilizes the messageserver to keep the
    connections public/global.
    """
    
    class _Panda3dInstance(object):
        """This class contains all information required for communicating
        with Panda3d instances. In particular you probably want to use the
        messageclient to send requests to the P3d instance.
        """
        def __init__(self, name, process=None, messageclient=None):
            self.name = name
            self.process = process
            self.messageclient = messageclient
            self.windows = 0

    class P3dInstanceNotFoundException(Exception):
        """Raised when a non-existent P3d instance was requested."""
        def __init__(self, name=None):
            message = ("The Panda3d instance you requested ({}) was either "
                      "removed or never existed.")
            if name is None:
                message = message.format('""')
            else:
                message = message.format(' "'+name+'"')
            Exception.__init__(self, message)

    def __init__(self):
        self.instances = []

    def process(self, *args, **kwargs):
        """Call this function often (60 times a second) to call the process
        method on all message clients. Alternatively you can process each
        message client on your own.
        """
        for i in self.instances:
            if i.messageclient is not None:
                i.messageclient.process()

    def getPanda3dInstance(self, name):
        """Start a new Panda3D instance in a process. The instance
        shouldn't open any windows by default, only wrap the recieved pipe
        with a MessageClient and poll for new requests from time to time.

        Returned object is of type Panda3dManager._Panda3dInstance.
        If an instance with the specified name already exists, no new
        instance will be created but the existing one will be returned.
        """
        old = self.getInstance(name)
        if old:
            return old

        panda_pipe, server_pipe = Pipe()
        messageserver.connectPipe(name, server_pipe)
        panda_process = Process(target=Panda3dInstance, args=(
            panda_pipe, name))
        panda_process.start()

        server_pipe2, gui_pipe = FakePipe()

        messageserver.connectPipe(name+" gui", server_pipe2)
        messageclient = MessageClient(gui_pipe)

        p3d = Panda3dManager._Panda3dInstance(name, panda_process, messageclient)
        self.instances.append(p3d)
        return p3d

    def openWindow(self, p3d, width=500, height=500, handle=None):
        """Open a new window within the specified instance.
        p3d can be either a name or a Panda3dInstance object.
        If a handle is passed, it will be used for parenting the new window
        to a parent window.
        Raises an P3dInstanceNotFoundException if no instance with the
        specified name can be found.
        """
        if isinstance(p3d, basestring):
            p3d = self.getInstance(p3d)
        if not p3d:
            raise P3dInstanceNotFoundException(p3d)

        p3d.windows += 1
        payload = OpenWindowRequest(p3d.windows, handle, width, height)
        p3d.messageclient.unicast(p3d.name, payload)
        return p3d.windows

    def getInstance(self, name):
        """Returns an Panda3dManager._Panda3dInstance object or None
        if there is no instance with the given name.
        """
        for i in self.instances:
            if i.name == name:
                return i

    def hasInstance(self, name):
        """Returns True or False depending on the existance of a named
        instance.
        """
        return self.getInstance(name) != None

# global instance
panda3dmanager = Panda3dManager()