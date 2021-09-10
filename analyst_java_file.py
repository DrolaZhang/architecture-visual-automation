import javalang
f=open('C:\\Users\\drola\\IdeaProjects\\leetcode\\interview\\src\\main\\java\\SubSequence.java')
tree = javalang.parse.parse(f.read())
print(tree.imports)
for import_f in tree.imports:
    print(import_f)

def parse_declaration_value(value):
    if isinstance(value,javalang.tree.BinaryOperation):
        return parse_declaration_value(value.operandl)+value.operator+parse_declaration_value(value.operandr)
    elif isinstance(value,javalang.tree.MethodInvocation):
        return parse_method_invocation(value)
    elif isinstance(value,javalang.tree.ClassCreator):
        return parse_type(value.type)+str(value)
    else:
        return value.value
def parse_type(type):
    if isinstance(type,javalang.tree.ReferenceType):
        if type.arguments!=None:
            a=''
            for arg in type.arguments:
                a=a+parse_argument(arg)
            return type.name + a

    elif isinstance(type,javalang.tree.BasicType):
        return type.name
    elif isinstance(type,javalang.tree.ClassCreator):
        return parse_type(type.type) + str(type)
    else:
        return str(type)
def parse_argument(argument):
    if isinstance(argument,javalang.tree.TypeArgument):
        return parse_type(argument.type)
    else:
        return str(argument)

def parse_method_invocation(method):
    for ref in method.arguments:
        if isinstance(ref,javalang.tree.ClassReference):
            argu = ""
            for ref in method.arguments:
                argu = argu+parse_class_reference(ref)
    return  method.qualifier+'.'+method.member+" argu "+argu

def parse_class_reference(refer):
    return parse_type(refer.type)

for declaration in tree.types[0].body:
    if isinstance(declaration,javalang.tree.FieldDeclaration):
        print('FieldDeclaration annotations: '+str(declaration.annotations))
        print('FieldDeclaration modifiers: '+str(declaration.modifiers))
        print('FieldDeclaration type: '+str(declaration.type))
        for declaration in declaration.declarators:
            print('FieldDeclaration declarators name: '+str(declaration.name))
            if declaration.initializer!=None:
                print('FieldDeclaration declarators value: ' + parse_declaration_value(declaration.initializer))

    elif isinstance(declaration,javalang.tree.ConstructorDeclaration):
        print('ConstructorDeclaration type_parameters: '+str(declaration.type_parameters))
        print('ConstructorDeclaration name: '+str(declaration.name))
        print('ConstructorDeclaration body: '+str(declaration.body))

    elif isinstance(declaration,javalang.tree.MethodDeclaration):
        print('MethodDeclaration type_parameters: '+str(declaration.type_parameters))
        print('MethodDeclaration name: '+str(declaration.name))
        print('MethodDeclaration body: '+str(declaration.body))
    elif isinstance(declaration,javalang.tree.ClassDeclaration):
        print('ClassDeclaration type_parameters: '+str(declaration.type_parameters))
        print('ClassDeclaration name: '+str(declaration.name))
        print('ClassDeclaration body: '+str(declaration.body))