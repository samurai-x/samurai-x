from struct import pack
from .protobj import Protobj

def build_list(stream, list_, type):
    for item in list_:
        if isinstance(item, Protobj):
            item.build(stream)
        else:
            stream.write(pack(type, item))
