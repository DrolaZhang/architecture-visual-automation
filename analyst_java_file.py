import javalang

from JavaClass import JavaClass

f = open('C:\\Users\\drola\\IdeaProjects\\leetcode\\interview\\src\\main\\java\\SubSequence.java')
tree = javalang.parse.parse(f.read())

java_class = JavaClass(tree)
