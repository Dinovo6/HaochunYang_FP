import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import networkx as nx
from pyvis.network import Network
import json
import os
from collections import defaultdict

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Visualization of actor partnership networks", className="title"),
    html.Div([
        html.Div([
            html.Label("Number of Actors"),
            dcc.Slider(
                id='actor-count-slider',
                min=1,
                max=1000,
                step=50,
                value=50,
                marks={i: str(i) for i in range(0, 1001, 100)},
            ),
        ], className="control-item", style={"width": "50%", "display": "inline-block", "verticalAlign": "top"}),
        
        html.Div([
            html.Label("Select Movie"),
            dcc.Dropdown(
                id='movie-dropdown',
                options=[],
                placeholder="Select a movie",
            ),
        ], className="control-item", style={"width": "50%", "display": "inline-block", "verticalAlign": "top"}),
    ], className="controls", style={"display": "flex", "alignItems": "center"}),
    
    html.Div([
        html.Div([
            html.H3("Information"),
            html.Div(id='debug-info', style={"display": "flex", "flexDirection": "row", "gap": "15px"}),
        ], className="debug-panel"),
        
        html.Div([
            html.Iframe(id='network-graph', style={"height": "600px", "width": "100%", "border": "none"}),
        ], className="graph-container"),
    ], className="main-content"),
    
    dcc.Store(id='network-data'),
   ])

def load_data():
    data=pd.read_csv('imdb_top_1000.csv')
    return data

def create_network(df, max_actors=50):
    G = nx.Graph()
    
    all_actors = []
    for col in ['Star1', 'Star2', 'Star3', 'Star4']:
        all_actors.extend(df[col].tolist())
    
    actor_counts = pd.Series(all_actors).value_counts()
    
    top_actors = actor_counts.head(max_actors).index.tolist()
    
    for actor in top_actors:
        G.add_node(actor)
    
    movie_actors = {}
    for _, row in df.iterrows():
        movie = row['Series_Title']
        actors = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]
        actors = [actor for actor in actors if actor in top_actors]
        movie_actors[movie] = actors
    
    co_appearances = defaultdict(int)
    
    for movie, actors in movie_actors.items():
        for i in range(len(actors)):
            for j in range(i+1, len(actors)):
                actor1 = actors[i]
                actor2 = actors[j]
                co_appearances[(actor1, actor2)] += 1
    
    for (actor1, actor2), weight in co_appearances.items():
        G.add_edge(actor1, actor2, weight=weight, title=f"Co-starred in {weight} movies")
    
    return G, movie_actors

df = load_data()
G, movie_actors = create_network(df)

@app.callback(
    Output('movie-dropdown', 'options'),
    Input('actor-count-slider', 'value')
)
def update_movie_dropdown(max_actors):
    G, movie_actors = create_network(df, max_actors)
    
    valid_movies = [movie for movie, actors in movie_actors.items() if len(actors) >= 2]
    
    options = [{'label': movie, 'value': movie} for movie in valid_movies]
    
    return options

@app.callback(
    Output('network-data', 'data'),
    Input('actor-count-slider', 'value'),
    Input('movie-dropdown', 'value')
)
def update_network_data(max_actors, selected_movie):
    G, movie_actors = create_network(df, max_actors)
    
    net = Network(height="600px", width="100%", notebook=True, directed=False)
    
    movie_related_actors = set()
    movie_related_edges = set()
    
    if selected_movie:
        movie_related_actors = set(movie_actors.get(selected_movie, []))
    
    for node in G.nodes():
        if selected_movie and node in movie_related_actors:
            net.add_node(node, label=node, color='#e74c3c', size=20, title=f"{node} 出演了 {selected_movie}")
        else:
            net.add_node(node, label=node, title=node)
    
    for edge in G.edges(data=True):
        source, target, attrs = edge
        weight = attrs.get('weight', 1)
        title = attrs.get('title', '')
        
        if selected_movie and (source in movie_related_actors or target in movie_related_actors):
            movie_related_edges.add((source, target))
        
        if selected_movie and source in movie_related_actors and target in movie_related_actors:
            net.add_edge(source, target, value=weight, title=title, color='#e74c3c', width=weight*2)
        else:
            net.add_edge(source, target, value=weight, title=title, width=weight)
    
    net.set_options('''
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
          "enabled": true,
          "iterations": 1000
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200
      },
      "edges": {
        "smooth": {
          "type": "continuous",
          "forceDirection": "none"
        }
      }
    }
    ''')
    
    html_data = net.generate_html()
    
    debug_info = {
        'total_actors_count': len(G.nodes()),
        'total_edges_count': len(G.edges()),
        'movie_related_actors_count': len(movie_related_actors) if selected_movie else 0,
        'movie_related_edges_count': len(movie_related_edges) if selected_movie else 0,
        'selected_movie': selected_movie if selected_movie else "None"
    }
    
    return {'html': html_data, 'debug': debug_info}

@app.callback(
    Output('network-graph', 'srcDoc'),
    Input('network-data', 'data')
)
def update_network_graph(data):
    if not data:
        raise PreventUpdate
    
    return data['html']

@app.callback(
    Output('debug-info', 'children'),
    Input('network-data', 'data')
)
def update_debug_info(data):
    if not data:
        raise PreventUpdate
    
    debug = data['debug']
    
    if debug['selected_movie'] == "None":
        return [
            html.Span(f"Total actors: {debug['total_actors_count']} | ", style={"marginRight": "10px"}),
            html.Span(f"Total connections: {debug['total_edges_count']} | ", style={"marginRight": "10px"}),
            html.Span(f"Selected movie: None")
        ]
    else:
        return [
            html.Span(f"Movie actors: {debug['movie_related_actors_count']} | ", style={"marginRight": "10px"}),
            html.Span(f"Movie connections: {debug['movie_related_edges_count']} | ", style={"marginRight": "10px"}),
            html.Span(f"Selected movie: {debug['selected_movie']}")
        ]

if __name__ == '__main__':
    app.run_server(debug=True)