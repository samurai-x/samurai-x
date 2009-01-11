from .codegen import CodegenBase, INDENT, DEDENT
from .template import template

class PyFunction(CodegenBase):
    def __init__(self, name):
        CodegenBase.__init__(self)
        self.name = name
        self.arguments = []
        self.decorators = []
        self.code = []

    def generate_code(self):
        code = []
        # decorators
        for decorator in self.decorators:
            code.append('@' + decorator)
        # function head
        joined_args = ', '.join(self.arguments)
        code.append(template('def $name($joined_args):',
            name=self.name,
            joined_args=joined_args)
            )
        # function body
        code.append(INDENT)
        if self.code:
            code += self.code
        else:
            code.append('pass')
        code.append(DEDENT)
        code.append('')
        return code

class PyMethod(PyFunction):
    """
        an instance method
    """
    def __init__(self, name):
        PyFunction.__init__(self, name)
        self.arguments = ['self']

class PyClassMethod(PyFunction):
    """
        the class method
    """
    def __init__(self, name):
        PyFunction.__init__(self, name)
        self.arguments = ['cls']
        self.decorators = ['classmethod']

class PyAttribute(CodegenBase):
    def __init__(self, name, value):
        CodegenBase.__init__(self)
        self.name = name
        self.value = value

    def generate_code(self):
        return [' = '.join([self.name, self.value])]
