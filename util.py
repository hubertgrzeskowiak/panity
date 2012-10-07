import re

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')

def camelToSnake(text):
    subbed = _underscorer1.sub(r'\1_\2', text)
    return _underscorer2.sub(r'\1_\2', subbed).lower()