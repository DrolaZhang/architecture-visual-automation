import javalang
import os
import networkx as nx
from pyvis.network import Network
from JavaClass import JavaClass
nodes = []
G = nx.DiGraph()

for root, dirs, files in os.walk('C:\\Users\\drola\\IdeaProjects\\apollo-master'):
    for file in files:
        file_name = os.path.join(root, file)
        if file_name.endswith('.java'):
            f = open(file_name, encoding='utf-8')
            tree = javalang.parse.parse(f.read())
            if len(tree.types) > 0:
                class_whole = tree.types[0]
                imports = tree.imports
                package = tree.package
                name = class_whole.name
                body = class_whole.body
                extends = class_whole.extends if isinstance(class_whole, javalang.tree.ClassDeclaration) else None
                implements = class_whole.implements if isinstance(class_whole, javalang.tree.ClassDeclaration) else None
                java_class = JavaClass(name, body, extends, implements, imports, package)
                current_node_name = java_class.name if java_class.package is None else java_class.package + '.' + java_class.name
                if java_class not in nodes:
                    nodes.append(java_class)
                    G.add_node(current_node_name, package=str(package))
                    if java_class.extends is not None:
                        for extend in java_class.extends:
                            for import_f in tree.imports:
                                if str(extend) in str(import_f.path):
                                    depends_node_name = import_f.path
                                    depends_node_package = import_f.path.split('.' + str(extend))[0]
                                else:
                                    depends_node_name = java_class.package + '.' + str(java_class.extends.name)
                                    depends_node_package = java_class.package
                                if depends_node_name not in nodes:
                                    nodes.append(depends_node_name)
                                    G.add_node(depends_node_name, package=str(depends_node_package))
                            G.add_edge(current_node_name, depends_node_name)

print(G.nodes)
print(G.edges)
# nt = Network('1000px', '1000px')
# # nt.from_nx(G)
# # nt.show('nx.html')