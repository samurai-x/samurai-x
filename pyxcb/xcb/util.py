CACHE_KEYWORD = '_cached'

def cached(func):
    # TODO: UGLY UGLY UGLY
    def do_cache(self, *args, **kwargs):
        if CACHE_KEYWORD not in func.func_dict: # table does not exist
            func.func_dict[CACHE_KEYWORD] = {}
        if self not in func.func_dict[CACHE_KEYWORD]:
            func.func_dict[CACHE_KEYWORD][self] = func(self, *args, **kwargs)
        return func.func_dict[CACHE_KEYWORD][self]
    return do_cache

def cached_property(func):
    return property(cached(func))
