
# Actor Partnership Network Visualization

## Project Overview
The goal of this project is to create an **interactive visualization tool** that maps out the collaboration network between actors based on data from the IMDB Top 1000 movies. By analyzing the co-starring relationships between actors, the project generates a dynamic graph and displays it through a Dash web application.

## Project Structure
The project is developed using **Dash** and **NetworkX** and focuses on the following key components:
1. **Data Loading and Cleaning** – Load and clean movie data from `imdb_top_1000.csv`.
2. **Network Graph Creation** – Build a graph using NetworkX to represent co-starring relationships.
3. **Interactive Visualization** – Generate an interactive graph using Pyvis and display it in a Dash web application.
4. **Dynamic Interface** – Allow real-time updates based on user input (slider and dropdown).

## Core Features
- **Interactive Interface:**  
  - Users can adjust the number of actors to display using a slider.  
  - Users can select a specific movie to highlight the related actors and their connections.

- **Dynamic Graph Generation:**  
  - Create a graph network using `NetworkX`.  
  - Generate a visualization with `Pyvis` in HTML format.

- **Real-Time Data Updates:**  
  - Adjust the displayed graph in real-time when the slider value or movie selection changes.

- **Debug Information Panel:**  
  - Display details like total nodes, edges, and selected movie-specific data.

## Technical Highlights
1. **Dash Framework:**  
   - Built with `dash` for the front-end interface.  
   - Used `dcc.Slider` and `dcc.Dropdown` components for dynamic input.

2. **Data Processing and Graph Construction:**  
   - Used `pandas` to load and clean data.  
   - Used `NetworkX` to build a graph of actor relationships based on co-starring frequency.

3. **Visualization:**  
   - Used `Pyvis` to create an HTML-based interactive graph.  
   - Embedded the graph into Dash using `Iframe`.

4. **Dynamic Callbacks:**  
   - Dash callbacks handle dynamic data updates.  
   - Multiple input-output combinations for real-time updates.

## File Structure
```plaintext
project/
├── HYFP.py                    # Main Dash application file
├── imdb_top_1000.csv         # Actor collaboration dataset          
```

## Tech Stack
- **Python** – Main programming language  
- **Dash** – Front-end framework for interactive UI  
- **Pandas** – Data handling and manipulation  
- **NetworkX** – Graph construction and network analysis  
- **Pyvis** – HTML-based graph visualization  

## User Experience
- Adjust the number of actors using a slider.  
- Select a specific movie to highlight actors and connections.  
- Hover over the graph to see collaboration details.  
- Debug panel to display real-time data.  

## Potential Improvements
- Increase the dataset size (beyond 1000 movies).  
- Add more network analysis metrics (e.g., degree centrality, betweenness centrality).  
- Improve graph layout and color scheme.  
- Add search and filtering features.  

## Project Status
- Basic functionality completed  
- Next steps: enhance interactivity and performance  

## Summary
This project builds an interactive visualization tool for actor collaboration networks using Dash, NetworkX, and Pyvis. The application allows users to explore complex actor relationships dynamically, providing an intuitive and powerful data visualization experience.
