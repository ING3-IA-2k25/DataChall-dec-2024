from dataclasses import dataclass
from typing import List, Dict, Tuple
import networkx as nx
from math import sqrt
from src.metro_graph.metroGraph  import MetroGraph, DataLoader, StationRepository, load_metro_graph, GpsCoordinate

@dataclass
class PersonFlow:
    """Represents a flow of people between stations"""
    from_station: str
    to_station: str
    num_people: int

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

    def process_flows(self, flows: List[PersonFlow]) -> Dict[Tuple[str, str], List[str]]:
        """Process all flows and return paths"""
        paths = {}
        for flow in flows:
            path_key = (flow.from_station, flow.to_station)
            if path_key not in paths:
                try:
                    paths[path_key] = self.path_finder.find_path(
                        flow.from_station, 
                        flow.to_station
                    )
                except nx.NetworkXNoPath:
                    print(f"No path found between {flow.from_station} and {flow.to_station}")
                    paths[path_key] = []
        return paths

def main():
    # Example usage
    graph = load_metro_graph()
    
    # Sample flows
    flows = [
        PersonFlow("Châtelet", "Nation", 100),
        PersonFlow("La Défense", "Gare de Lyon", 50),
        # Add more flows as needed
    ]
    
    # Process flows
    processor = FlowProcessor(graph)
    paths = processor.process_flows(flows)
    
    # Print results
    for (start, end), path in paths.items():
        if path:
            print(f"\nPath from {start} to {end}:")
            print(" -> ".join(path))

if __name__ == "__main__":
    main()
    # G = load_metro_graph()