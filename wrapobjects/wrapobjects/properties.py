from wraplib.pyclass import PyClass
from wraplib.pymember import PyMethod

def make_properties(wrapper, obj):
    def _make_property(name):
        args = []
        try:
            getter = obj.get_member_by_name('get_%s' % name)
        except KeyError:
            args.append('None')
        else:
            args.append(getter.name)
            if not isinstance(getter, PyMethod):
                print 'Property %s of %s: getter is %r' % (name, obj.name, getter)
                return
            if len(getter.arguments) != 1:
                print 'Property %s of %s: getter takes a strange number of arguments' % (name, obj.name)
                return
        try:
            setter = obj.get_member_by_name('set_%s' % name)
        except KeyError:
            pass
        else:
            args.append(setter.name)
            if not isinstance(setter, PyMethod):
                print 'Property %s of %s: setter is %r' % (name, obj.name, setter)
                return
            if len(setter.arguments) != 2:
                print 'Property %s of %s: setter takes a strange number of arguments' % (name, obj.name)
                return
        obj.new_attribute(name, 'property(%s)' % (', '.join(args)))

    if isinstance(obj, PyClass):
        for member in obj.members:
            if (member.name.startswith('get_') or
                    member.name.startswith('set_')):
                propname = member.name[len('get_'):]
                try:
                    obj.get_member_by_name(propname)
                except KeyError:
                    _make_property(propname)
