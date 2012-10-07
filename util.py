import re

_underscorer1 = re.compile('(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')

def camelToSnake(text):
    """Convert HelloWorld to hello_world."""
    subbed = _underscorer1.sub(r'\1_\2', text)
    return _underscorer2.sub(r'\1_\2', subbed).lower()

def snakeToCamel(text):
    """Convert hello_world to HelloWorld. Note that first letter is
    capital, too.
    """
    return text.title().replace("_", "")

def isNumber(num):
    try:
        float(num)
        return True
    except ValueError:
        return False