import javalang
import os
import networkx as nx
from pyvis.network import Network

nodes=[]
G=nx.DiGraph()

for root, dirs, files in os.walk('C:\\Users\\drola\\IdeaProjects'):
    for file in files:
        file_name = os.path.join(root,file)
        if file_name.endswith('.java'):
            f=open(file_name,encoding='utf-8')
            tree=javalang.parse.parse(f.read())
            if tree.package !=None:
                current_node_name = tree.package.name +'.'+tree.types[0].name
                if current_node_name not in nodes:
                    nodes.append(current_node_name)
                    G.add_node(current_node_name)
                    for import_f in tree.imports:
                        depends_node_name = import_f.path
                        if depends_node_name not in nodes:
                            nodes.append(depends_node_name)
                            G.add_node(depends_node_name)
                        G.add_edge(current_node_name,depends_node_name)

nt=Network('2000px','2000px')
nt.from_nx(G)
nt.show('nx.html')



