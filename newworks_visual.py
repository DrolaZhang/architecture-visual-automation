import javalang
import os
import networkx as nx
from pyvis.network import Network

from JavaClass import JavaClass, JavaClassEncoder

nodes = []
G = nx.DiGraph()

for root, dirs, files in os.walk('C:\\Users\\drola\\IdeaProjects'):
    for file in files:
        file_name = os.path.join(root, file)
        if file_name.endswith('.java'):
            f = open(file_name, encoding='utf-8')
            tree = javalang.parse.parse(f.read())
            java_class = JavaClass(tree.types[0].name, tree.types[0].body, tree.imports, tree.package)
            current_node_name = java_class.package + '.' + java_class.name
            if java_class not in nodes:
                nodes.append(java_class)
                G.add_node(current_node_name, data=java_class.tojson())
                for import_f in tree.imports:
                    depends_node_name = import_f.path
                    if depends_node_name not in nodes:
                        nodes.append(depends_node_name)
                        G.add_node(depends_node_name)
                    G.add_edge(current_node_name, depends_node_name)

nt = Network('1000px', '1000px')
nt.from_nx(G)
nt.show('nx.html')
