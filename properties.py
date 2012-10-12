"""This module describes attributes components can have.
These are used to
1. marshal and unmarshal to and from xml
2. validate assignment of component attributes
3. choose the right GUI widgets in the editor
"""

class SerializedProperty(object):
    """The SerializedProperty is meant to be initiated as a class attribute,
    where it serves as both class- and instance attribute.
    From the point of view of the object it behaves like a usual int, float,
    string or other value, but under the hood it offers validation,
    converting and callbacks on change.

    It behaves a bit like the python-own property class, but in contrast
    it doesn't allow explicit assignment of getter and setter etc.

    This is the base class which doesn't offer any checks or validation.
    Better use the specialized subclasses instead.

    See the test files, especially serializingtest.py for usage examples.
    """
    def __init__(self, default=None):
        """default value is used as initial value."""
        self.default = default
        self.listeners = {}

    def __get__(self, obj, cls=None):
        """Return a value when called on object or SerializedProperty instance
        when called on class.
        """
        if obj is None:
            # property called on class level. return a nice object
            return self

        if hasattr(obj, "_properties") and obj._properties.has_key(self):
            return obj._properties[self]
        else:
            return self.default

    def getValue(self, obj):
        return self.__get__(obj)

    def __set__(self, obj, value):
        """Set a property on an object.
        If the new value is same as current, no checks are run and the value
        is returned. Otherwise self.check() is run and on failure
        self.convert(), followed by a second check. If one of the checks is
        successful, the new value is returned and set, otherwise only False
        is returned.
        """
        # create a properties dict on the object
        if not hasattr(obj, "_properties"):
            obj._properties = {}
            if value == self.default:
                return value
        elif obj._properties.has_key(self) and value == obj._properties[self]:
                # new value is same as old one
                return value
        # check the given value
        try:
            self.check(value)
            obj._properties[self] = value
            self.__invokeListeners(obj, value)
            return value
        except AssertionError:
            pass
        # then try to convert and check again
        try:
            value = self.convert(value)
            self.check(value)
            obj._properties[self] = value
            self.__invokeListeners(obj, value)
            return value
        except (AssertionError, ValueError) as e:
            print "warning, setting value "+str(value)+" on obj "+str(obj)+" not possible!"
            return False

    def __invokeListeners(self, obj, value):
        if hasattr(obj, "_listeners") and self in obj._listeners:
            for f in obj._listeners[self]:
                f(value)

    def addListener(self, obj, function):
        """Add a callback function that is called every time the value is
        effectively changed. The new value is passed as argument.
        obj is the object this property should be watched on.
        """
        if not hasattr(obj, "_listeners"):
            obj._listeners = {}
            obj._listeners[self] = []
        elif not obj._listeners.has_key(self):
            obj._listeners[self] = []
        obj._listeners[self].append(function)

    def removeListener(self, obj, function):
        """Reverse of addListener."""
        obj._listeners[self].remove(function)

    def removeAllListeners(self, obj):
        obj._listeners.pop(self, None)

    def check(self, value):
        """Check a potential value for its correctness and optionally type.
        AssertionError is thrown if you're unlucky.

        Override this method in derived classes.
        """
        pass
    
    def convert(self, value):
        """Try to convert a value so that it passes the check.
        This is in particular useful when working with numbers.
        A converted value is returned that can be assigned to this property or
        None.

        Override this method in derived classes.
        """
        pass


class FloatProperty(SerializedProperty):
    def __init__(self, minimum=None, maximum=None, default=0.0):
        """When setting values to this, minimum and maximum are checked and the
        given value might get clipped eventually. The default value is not
        checked. This means setting minimum=0, maximum=1 and default=2 sets
        the value to 2 which, once changed, can't get out of the range 0..1
        """
        SerializedProperty.__init__(self, default)
        self.minimum = minimum
        self.maximum = maximum

    def check(self, value):
        assert isinstance(value, float)
        if self.minimum is not None:
            assert value >= self.minimum
        if self.maximum is not None:
            assert value <= self.maximum
    
    def convert(self, value):
        value = float(value)
        if value < self.minimum:
            return self.minimum
        elif self.maximum is not None and value > self.maximum:
            return self.maximum
        return value


class IntegerProperty(SerializedProperty):
    def __init__(self, minimum=None, maximum=None, default=0):
        """When setting values to this, minimum and maximum are checked and the
        given value might get clipped eventually. The default value is not
        checked. This means setting minimum=0, maximum=1 and default=2 sets
        the value to 2 which, once changed, can't get out of the range 0..1
        """
        SerializedProperty.__init__(self, default)
        self.minimum = minimum
        self.maximum = maximum

    def check(self, value):
        assert isinstance(value, int)
        if self.minimum is not None:
            assert value >= self.minimum
        if self.maximum is not None:
            assert value <= self.maximum
    
    def convert(self, value):
        value = int(value)
        if value < self.minimum:
            return self.minimum
        elif self.maximum is not None and value > self.maximum:
            return self.maximum
        return value


class UnsignedIntegerProperty(IntegerProperty):
    """Positive integer, zero included.
    Note that this is not really an unsigned int as in C, it still lacks the
    last bit.
    """
    def check(self, value):
        assert isinstance(value, int)
        assert value >= 0
        if self.minimum is not None:
            assert value >= self.minimum
        if self.maximum is not None:
            assert value <= self.maximum


class StringProperty(SerializedProperty):
    def __init__(self, default=""):
        SerializedProperty.__init__(self, default)

    def check(self, value):
        assert isinstance(value, str)

    def convert(self, value):
        return str(value)


class PathProperty(StringProperty):
    pass


class SerializedPropertyDecorator(property):
    """Use this SerializedProperty if you need your own getter and setter.
    This class tries to behave same as SerializedProperty except for checks
    and convertion.
    This class is mainly used by the transform component, as it stores
    its property values on a nodepath.
    """
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):

        def decorated(obj, value):
            self.__invokeListeners(obj, value);
            fset(obj, value)

        super(SerializedPropertyDecorator, self).__init__(
            fget,
            decorated,
            fdel,
            doc)

    def getValue(self, obj):
        return self.__get__(obj)

    def __invokeListeners(self, obj, value):
        if hasattr(obj, "_listeners") and self in obj._listeners:
            for f in obj._listeners[self]:
                f(value)

    def addListener(self, obj, function):
        """Add a callback function that is called every time the value is
        effectively changed. The new value is passed as argument.
        obj is the object this property should be watched on.
        """
        if not hasattr(obj, "_listeners"):
            obj._listeners = {}
            obj._listeners[self] = []
        elif not obj._listeners.has_key(self):
            obj._listeners[self] = []
        obj._listeners[self].append(function)

    def removeListener(self, obj, function):
        """Reverse of addListener."""
        obj._listeners[self].remove(function)

    def removeAllListeners(self, obj):
        obj._listeners.pop(self, None)