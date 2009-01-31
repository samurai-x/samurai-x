from .codegen import CodegenBase, INDENT, DEDENT
from .template import template
from .pymember import PyMethod, PyAttribute

class PyClass(CodegenBase):
    def __init__(self, name, base='object'):
        self.name = name
        self.base = base
        self.members = []

    def add_member(self, member):
        self.members.append(member)
    
    def get_member_by_name(self, name):
        for member in self.members:
            if member.name == name:
                return member
        raise KeyError(name)

    def new_method(self, name):
        ret = PyMethod(name)
        self.members.append(ret)
        return ret

    def new_attribute(self, name, value):
        ret = PyAttribute(name, value)
        self.members.append(ret)
        return ret

    def generate_code(self):
        code = [
            template('class $name($base):', 
                name = self.name,
                base = self.base
            ), 
            INDENT]
        if not self.members:
            code.append('pass')
        else:
            for member in self.members:
                code += member.generate_code()
        if code[-1] != '': # force a newline
            code.append('')
        code.append(DEDENT)
        return code
