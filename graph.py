import streamlit as st
import pandas as pd
from pyvis import network as net
from IPython.core.display import display, HTML
import numpy as np
import streamlit.components.v1 as components
import networkx as nx
from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx

@st.cache
def get_graph(path):
    df = pd.read_csv(path)
    D = nx.convert_matrix.from_pandas_edgelist(df,'Source','Target',['Weight'],nx.DiGraph)
    G = nx.DiGraph.to_undirected(D)
    return G

def app():
    st.title("Network Graph for AWCA")

    f = get_graph("BERT_edge_list2.csv")

    plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
              tools="", toolbar_location=None)

    graph = from_networkx(f, nx.spring_layout, scale=2, center=(0, 0))
    
    plot.renderers.append(graph)

    output_file("networkx_graph.html")
    show(plot)
    """
    HtmlFile = open("example.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=400,width=600)
    """
    st.write("rendering done!")