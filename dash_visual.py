
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import networkx as nx
import os
import javalang
from JavaClass import JavaClass

def getEdges():
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
                    implements = class_whole.implements if isinstance(class_whole,
                                                                      javalang.tree.ClassDeclaration) else None
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
    return G.edges

def networkGraph(EGDE_VAR):

    edges = getEdges()
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)

    # edges trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(color='black', width=1),
        hoverinfo='none',
        showlegend=False,
        mode='lines')

    # nodes trace
    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y, text=text,
        mode='markers+text',
        showlegend=False,
        hoverinfo='none',
        marker=dict(
            color='pink',
            size=50,
            line=dict(color='black', width=1)))

    # layout
    layout = dict(plot_bgcolor='white',
                  paper_bgcolor='white',
                  margin=dict(t=10, b=10, l=10, r=10, pad=0),
                  xaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True),
                  yaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True))

    # figure
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

    return fig

# Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Dash Networkx'

app.layout = html.Div([
        html.I('Write your EDGE_VAR'),
        html.Br(),
        dcc.Input(id='EGDE_VAR', type='text', value='K', debounce=True),
        dcc.Graph(id='my-graph'),
    ]
)

@app.callback(
    Output('my-graph', 'figure'),
    [Input('EGDE_VAR', 'value')],
)
def update_output(EGDE_VAR):
    return networkGraph(EGDE_VAR)

if __name__ == '__main__':
    app.run_server(debug=True)