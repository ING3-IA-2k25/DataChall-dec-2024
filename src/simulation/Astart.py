from dataclasses import dataclass
from typing import List, Dict, Tuple
import networkx as nx
from math import sqrt
from src.metro_graph.metroGraph  import MetroGraph, DataLoader, StationRepository, load_metro_graph, GpsCoordinate, save_metro_graph, Connection
from src.simulation.passenger_flow import PassengerFlow

class PathFinder:
    """Handles path finding using A* algorithm"""
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def parse_gps(self, gps_str: str) -> Tuple[float, float]:
        """Parse GPS string into latitude and longitude"""
        try:
            lat, lon = map(float, gps_str.split(','))
            return lat, lon
        except (ValueError, AttributeError):
            return 0.0, 0.0

    def heuristic(self, node1: str, node2: str) -> float:
        """Calculate straight-line distance between stations using GPS coords"""
        n1_data = self.graph.nodes[node1]
        n2_data = self.graph.nodes[node2]
        
        if not (n1_data.get('gps') and n2_data.get('gps')):
            return 0.0
            
        # Parse GPS coordinates from string format
        try:
            lat1, lon1 = self.parse_gps(str(n1_data['gps']))
            lat2, lon2 = self.parse_gps(str(n2_data['gps']))
            
            return sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
        except:
            return 0.0

    def find_path(self, start: str, end: str) -> List[str]:
        """Find shortest path using A* algorithm"""
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

    # todo: repaire this function (Map is not defined)
    def initialize_flow_counters(self) -> None:
        """Initialize flow counters for all edges"""
        # self.graph.edges.items().map(lambda u, v: self.graph[u][v].update({
        #     'source_to_dest': 0,
        #     'dest_to_source': 0
        # }))
        pass
        
        
        
    def update_flow(self, path: List[str], counter: int) -> None:
        """Update flow counters for a specific path"""
        # print('\n\n\n')
        # print(path)
        for i in range(len(path) - 1):
            source = path[i]
            destination = path[i + 1]
            
            # get nodes
            if not self.graph.has_edge(source, destination):
                continue
            
            edge: Connection = self.graph.edges[source, destination]
            
            if source == edge['source']:
                edge['visited_STT'] += counter
            else:
                edge['visited_TTS'] +=  counter
            
            
    
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