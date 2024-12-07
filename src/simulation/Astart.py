from dataclasses import dataclass
from typing import List, Dict, Tuple
import networkx as nx
from math import sqrt
from src.metro_graph.metroGraph  import MetroGraph, DataLoader, StationRepository, load_metro_graph, GpsCoordinate, save_metro_graph
from src.simulation.passenger_flow import PassengerFlow

class PathFinder:
    """Handles path finding using A* algorithm"""
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def heuristic(self, node1: str, node2: str) -> float:
        """Calculate straight-line distance between stations using GPS coords"""
        n1_data = self.graph.nodes[node1]
        n2_data = self.graph.nodes[node2]
        
        if not (n1_data.get('gps') and n2_data.get('gps')):
            return 0
            
        lat1, lon1 = n1_data['gps'].latitude, n1_data['gps'].longitude
        lat2, lon2 = n2_data['gps'].latitude, n2_data['gps'].longitude
        
        return sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

    def find_path(self, start: str, end: str) -> List[str]:
        """Find shortest path using A*"""
        return nx.astar_path(
            self.graph, 
            start, 
            end, 
            heuristic=lambda n1, n2: self.heuristic(n1, n2)
        )

class FlowProcessor:
    """Processes multiple person flows and finds optimal paths"""
    def __init__(self, graph: nx.Graph):
        self.path_finder = PathFinder(graph)
        self.graph = graph

    def process_flows(self, flows: List[PassengerFlow]) -> Dict[Tuple[str, str, int], List[str]]:
        """Process all flows and return paths"""
        paths = {}
        for flow in flows:
            path_key = (flow.source, flow.destination, flow.count)
            if path_key not in paths:
                try:
                    paths[path_key] = self.path_finder.find_path(
                        flow.source, 
                        flow.destination
                    )
                except nx.NetworkXNoPath:
                    print(f"No path found between {flow.source} and {flow.destination}")
                    paths[path_key] = []
        return paths

class FlowUpdater:
    """Updates graph edges with passenger flow data"""
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def initialize_flow_counters(self) -> None:
        """Initialize flow counters for all edges"""
        self.graph.edges.map(lambda u, v: self.graph[u][v].update({
            'source_to_dest': 0,
            'dest_to_source': 0
        }))
        
        
        
    def update_flow(self, path: List[str], count: int) -> None:
        """Update flow counters for a specific path"""
        print('\n\n\n')
        print(path)
        for i in range(len(path) - 1):
            source = path[i]
            destination = path[i + 1]
            
            # get nodes
            if not self.graph.has_edge(source, destination):
                continue
            
            edge = self.graph.edges[source, destination]
            
            if source == edge['source']:
                edge['visited_STT'] += count
            else:
                edge['visited_TTS'] += count
            
            
    
def main():
    # Example usage
    graph = load_metro_graph()
    
    # Sample flows
    flows = [
        PassengerFlow("Châtelet", "Nation", 100),
        PassengerFlow("La Défense", "Gare de Lyon", 50),
        # Add more flows as needed
    ]
    
    # Process flows
    processor = FlowProcessor(graph)
    paths = processor.process_flows(flows)
    
    flow_updater = FlowUpdater(graph)
    
    for (start, end, count), path in paths.items():
        if path:
            print(f"\nPath from {start} to {end}: {count} passengers")
            print(" -> ".join(path))
            flow_updater.update_flow(path, count)
            # update_graph_with_flows(graph, paths, count)
    
    # Save updated graph
    save_metro_graph(graph)        
    

if __name__ == "__main__":
    main()
    # G = load_metro_graph()