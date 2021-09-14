import javalang
import json

from JavaClass import JavaClass

f = open('C:\\Users\\drola\\IdeaProjects\\leetcode\\interview\\src\\main\\java\\SubSequence.java')
tree = javalang.parse.parse(f.read())
body = tree.types[0].body
imports = tree.imports


def parse_class(java_class):
    print(java_class.imports)
    print(java_class.methods)
    print(java_class.constructors)
    print(java_class.fields)
    for inner_class in java_class.inner_classes:
        print(inner_class.imports)
        print(inner_class.methods)
        print(inner_class.constructors)
        print(java_class.fields)


java_class = JavaClass(tree.types[0].name, body, imports, tree.package)
# parse_class(java_class)
# print(java_class.toJSON())
print(json.dumps(java_class))