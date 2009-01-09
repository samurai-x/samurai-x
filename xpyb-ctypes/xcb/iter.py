from itertools import chain

def flatten(l):
    return list(chain.from_iterable(l))

class Iterator(object):
    def __init__(self, list, groupsize, name, is_list):
        self.list = list
        self.groupsize = groupsize
        self.name = name
        self.is_list = bool(is_list)
        
    def __iter__(self):
#        print 'MOO', repr(self.list)
#        for l in self.list:
#            print 'RERPRPR', repr(l)
#            if isinstance(l, list):
#                l = flatten(l)
#            yield l
        if len(self.list) == 0:
            return iter([])
        else:
            if isinstance(self.list[0], (list, tuple)):
                return iter(self.list)
            else:
                return iter([self.list])
