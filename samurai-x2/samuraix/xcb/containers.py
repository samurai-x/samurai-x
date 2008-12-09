class SizeHints(object):
    properties = ('x', 'y', 'width', 'height', 'min_width', \
              'min_height', 'max_width', 'max_height', 'width_inc',
              'height_inc', 'min_aspect_num', 'min_aspect_den',
              'max_aspect_num', 'max_aspect_den', 'base_width', 'base_height')
 
    def __init__(self, **kwargs):
        for prop_name in self.properties:
            setattr(self, prop_name, kwargs.get(prop_name, 0)) # TODO: not so nice

        # TODO: implement aspect ratios (using `fractions`?)

    def __repr__(self):
        return '<SizeHints perfect size = %s>' % (self.perfect_size,)

    @property
    def perfect_size(self):
        return (self.perfect_width, self.perfect_height)

    @property
    def perfect_width(self):
        if self.width:
            return self.width # User-specified size
        i = 2
        return (self.base_width or self.min_width) + i * self.width_inc # TODO: let the user choose `i` 

    @property
    def perfect_height(self):
        print vars(self)
        if self.height:
            return self.height # User-specified size
        j = 2
        return (self.base_height or self.min_height) + j * self.height_inc # TODO: let the user choose `j` 
