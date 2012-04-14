"""This module describes attributes components can have.
These are used to
1. validate xml files that try to set components' values and
2. choose the right GUI widgets in the editor
"""

class SerializedProperty(object):
    def __init__(self, default=None):
        self.default = default

    def __get__(self, obj, cls=None):
        if hasattr(obj, "_properties") and obj._properties.has_key(self):
            return obj._properties[self]
        else:
            return self.default

    def __set__(self, obj, value):
        """Set a property on an object. self.check is run and on failure
        self.convert, followed by a second check. If one of the checks is
        successful, the new value is returned, otherwise False.
        """
        # create a properties dict on the object
        if not hasattr(obj, "_properties"):
            obj._properties = {}
        # check the given value
        try:
            self.check(value)
            obj._properties[self] = value
            return value
        except AssertionError:
            pass
        # then try to convert and check again
        try:
            value = self.convert(value)
            self.check(value)
            self.value = value
            return value
        except:
            return False

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


class ComponentProperty(SerializedProperty):
    def __init__(self, typ=None):
        SerializedProperty.__init__(self)
        self.typ = typ

    def check(self, value):
        assert hasattr(value, "name")
        assert hasattr(value, "game_object")


class FloatProperty(SerializedProperty):
    def __init__(self, minimum=None, maximum=None, default=0.0):
        """When setting values to this, minimum and maximum are checked and the
        given value might get clipped eventually. The default value is not
        checked.
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
        try:
            value = float(value)
        except ValueError:
            return
        if value < self.minimum:
            return self.minimum
        elif self.maximum is not None and value > self.maximum:
            return self.maximum
        return value
 
    def __copy__(self):
        f = Float()
        f.minimum = self.minimum
        f.maximum = self.maximum
        f.default = self.default
        f.value = self.value
        return f
