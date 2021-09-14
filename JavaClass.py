import javalang
import json


def get_inner_classes(declaration, package):
    return JavaClass(declaration.name, declaration.body, None, None, None, package)


def get_constructors(declaration):
    constructor_modifiers = str(declaration.modifiers)
    constructor_name = str(declaration.name)
    constructor_parameters = parse_parameter(declaration.parameters)
    constructor_throws = parse_parameter(declaration.throws)
    return constructor_modifiers, constructor_name, constructor_parameters, constructor_throws


def get_methods(declaration):
    method_modifier = str(declaration.modifiers)
    method_name = str(declaration.name)
    method_parameters = parse_parameter(declaration.parameters)
    method_return_type = parse_type(declaration.return_type)
    return method_modifier, method_name, method_parameters, method_return_type


def get_field(declaration):
    field_annotation = str(declaration.annotations)
    field_modifiers = str(declaration.modifiers)
    filed_type = parse_type(declaration.type)
    field_name = ''
    field_value = ''
    for declaration in declaration.declarators:
        field_name = field_name + str(declaration.name)
        field_value = field_value + parse_declaration_value(declaration.initializer)
    return field_annotation, field_modifiers, filed_type, field_name, field_value


def get_import(imports):
    for import_ in imports:
        return import_.path if import_.wildcard is False else import_.path + '.*'


class JavaClass:

    def __init__(self, name, body, extends, implements, imports, package):
        self.name = name
        self.extends = extends
        self.implements = implements
        self.fields = []
        self.constructors = []
        self.methods = []
        self.inner_classes = []
        self.imports = []
        self.package = None if package is None else package.name
        if imports is not None:
            self.imports.append(get_import(imports))
        for declaration in body:
            if isinstance(declaration, javalang.tree.FieldDeclaration):
                # self.fields.append(get_field(declaration))
                self.fields.append(declaration)
            elif isinstance(declaration, javalang.tree.ConstructorDeclaration):
                # self.constructors.append(get_constructors(declaration))
                self.constructors.append(declaration)
            elif isinstance(declaration, javalang.tree.MethodDeclaration):
                # self.methods.append(get_methods(declaration))
                self.methods.append(declaration)
            elif isinstance(declaration, javalang.tree.ClassDeclaration):
                # self.inner_classes.append(get_inner_classes(declaration, package))
                self.inner_classes.append(declaration)

    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return json.dumps(self, cls=change_type, indent=4)


def change_type(byte):
    if isinstance(byte, bytes):
        return str(byte, encoding='utf-8')
    return json.JSONEncoder.default(byte)


def parse_declaration_value(value):
    if isinstance(value, javalang.tree.BinaryOperation):
        return parse_declaration_value(value.operandl) + value.operator + parse_declaration_value(value.operandr)
    elif isinstance(value, javalang.tree.MethodInvocation):
        return parse_method_invocation(value)
    elif isinstance(value, javalang.tree.ClassCreator):
        return parse_type(value.type) + str(value)
    elif isinstance(value, javalang.tree.MemberReference):
        return str(value)
    elif isinstance(value, javalang.tree.ArrayInitializer):
        return str(value)
    elif isinstance(value, javalang.tree.ArrayCreator):
        return str(value)
    elif isinstance(value, javalang.tree.LambdaExpression):
        return str(value)
    elif isinstance(value, javalang.tree.ClassReference):
        return str(value)
    elif value is None:
        return str(None)
    else:
        return value.value


def parse_type(type):
    if isinstance(type, javalang.tree.ReferenceType):
        a = ''
        if type.arguments is not None:
            for arg in type.arguments:
                a = a + parse_argument(arg)
        return type.name + a
    elif isinstance(type, javalang.tree.BasicType):
        return type.name
    elif isinstance(type, javalang.tree.ClassCreator):
        return parse_type(type.type) + str(type)
    else:
        return str(type)


def parse_argument(argument):
    if isinstance(argument, javalang.tree.TypeArgument):
        return parse_type(argument.type)
    else:
        return str(argument)


def parse_method_invocation(method):
    argu = ""
    for ref in method.arguments:
        if isinstance(ref, javalang.tree.ClassReference):
            for ref in method.arguments:
                argu = argu + parse_class_reference(ref)
    return method.qualifier + '.' + method.member + " argu " + argu


def parse_class_reference(refer):
    if isinstance(refer, javalang.tree.MemberReference):
        return str(refer)
    else:
        return parse_type(refer.type)


def parse_parameter(parameters):
    if parameters is None:
        return str(None)
    params = ''
    for para in parameters:
        if isinstance(para, javalang.tree.FormalParameter):
            params = params + para.name + " "
        else:
            params = params + str(para) + " "
    return params
