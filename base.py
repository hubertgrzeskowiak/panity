"""this is a global share module, sorta.
only thing it does is holding an instance of ShowBase, that gets instanced
as soon as this module is imported.
"""

from showbase import ShowBase
base = ShowBase()
