"""This module describes attributes components can have.
These are used to
1. validate xml files that try to set components' values and
2. choose the right GUI widgets in the editor
"""

class SerializedProperty(object):
    def __init__(self):
        self.value = None
    def __get__(self, obj, cls=None):
        return self.value
    def __set__(self, obj, value):
        # first check
        try:
            self.check(value)
            self.value = value
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
        """you should override this function.
        
        check a potential value for its correctness and type.
        assertionerror is thrown if you're unlucky.
        """
        pass
    
    def convert(self, value):
        """Try to convert a value so that it passes the check.
        This is in particular useful when working with numbers.
        A converted value is returned that can be assigned to this property or
        None.
        """
        pass


class Component(SerializedProperty):
    def __init__(self, typ=None):
        SerializedProperty.__init__(self)
        self.typ = typ

    def check(self, value):
        assert hasattr(value, "game_object")


class FloatProperty(SerializedProperty):
    def __init__(self, minimum=None, maximum=None, default=None):
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        assert minimum <= maximum
        if default is not None:
            self.check(default)
            self.value = default
        else:
            if minimum is not None:
                self.check(minimum)
                self.value = minimum
            elif maximum is not None:
                self.check(maximum)
                self.value = maximum
            else:
                self.value = 0.0
    
    def __copy__(self):
        f = Float()
        f.minimum = self.minimum
        f.maximum = self.maximum
        f.default = self.default
        f.value = self.value
        return f

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
