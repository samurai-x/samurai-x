def annotate(**kwargs):
    if 'return_' in kwargs:
        kwargs['return'] = kwargs.pop('return_')
    def deco(f):
        f.func_annotations = kwargs
        return f
    return deco

