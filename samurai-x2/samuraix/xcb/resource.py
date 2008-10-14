import samuraix.event

class ResourceMeta(type):
    def __new__(mcs, name, bases, dct):
        return type.__new__(mcs, name, bases, dct)

    def __call__(cls, connection, xid, *args, **kwargs):
        cached = connection.get_from_cache(xid)
        if cached:
            assert isinstance(cached, cls) # if that one fails, it's a bug. xids are not unique then.
            return cached
        else:
            obj = type.__call__(cls, connection, xid, *args, **kwargs)
            connection.add_to_cache(obj)
            return obj

class Resource(samuraix.event.EventDispatcher):
    __metaclass__ = ResourceMeta

    ## should we have something like this?:
    #@classmethod
    #def new(cls, connection):
    #    return cls(connection, _xcb.xcb_generate_id(connection._connection))

    def __init__(self, connection, xid):
        self.connection = connection
        self._xid = xid

    def __eq__(self, other):
        return self._xid == other._xid

    def delete(self):
        """ 
            The resource is going to be deleted. Remove it from
            the cache.
        """
        self.connection.remove_from_cache(self)
