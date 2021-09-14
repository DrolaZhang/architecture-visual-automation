import javalang
import json

from JavaClass import JavaClass

f = open('C:\\Users\\drola\\IdeaProjects\\apollo-master\\apollo-portal\\src\\main\\java\\com\\ctrip\\framework\\apollo\\portal\\spi\\configuration\\LdapExtendProperties.java')
tree = javalang.parse.parse(f.read())
class_whole = tree.types[0]
imports = tree.imports
package = tree.package
name = class_whole.name
body = class_whole.body
extends = class_whole.extends
implements = class_whole.implements

java_class = JavaClass(name, body, extends, implements, imports, package)
print(java_class)
