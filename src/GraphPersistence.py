import pickle
from pathlib import Path
import networkx as nx


class GraphPersistence:
    """Handles saving and loading of metro graphs"""
    def __init__(self, save_dir: str = "./data"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def save_graph(self, graph: nx.Graph, filename: str = "metro_graph.pkl") -> None:
        """Save graph to pickle file"""
        save_path = self.save_dir / filename
        with open(save_path, 'wb') as f:
            pickle.dump(graph, f)
            
    def load_graph(self, filename: str = "metro_graph.pkl") -> nx.Graph:
        """Load graph from pickle file"""
        load_path = self.save_dir / filename
        with open(load_path, 'rb') as f:
            return pickle.load(f)