from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle
from pathlib import Path

from GraphPersistence_oriented import GraphPersistence

@dataclass
class GpsCoordinate:
    """Represents a GPS coordinate with latitude and longitude"""
    latitude: float
    longitude: float

    @classmethod
    def from_string(cls, gps_string: str) -> Optional['GpsCoordinate']:
        """Creates a GpsCoordinate from a string format 'latitude, longitude'"""
        if not gps_string or gps_string.strip() == "":
            return None
        try:
            lat_str, lon_str = gps_string.split(',')
            return cls(
                latitude=float(lat_str.strip()),
                longitude=float(lon_str.strip())
            )
        except (ValueError, AttributeError):
            return None

@dataclass
class Station:
    """Station entity with name, lines and GPS coordinates"""
    name: str
    lines: Set[str]
    gps: Optional[GpsCoordinate]

@dataclass
class Connection:
    """Connection between stations with line ID and flow"""
    line_id: str
    flow: int = 0
    source: str = ""
    target: str = ""
    visited: int = 0
    
class DataLoader:
    """Responsible for loading and parsing CSV files"""
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)

    def load_metro_plan(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "plan du métro.csv")

    def load_station_positions(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "position gps des stations de métro.csv")

class StationRepository:
    """Handles station data processing and storage"""
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.stations: Dict[str, Station] = {}
        self._init_stations()

    """Handles station data processing and storage"""
    def _init_stations(self):
        metro_plan = self.data_loader.load_metro_plan()
        positions = self.data_loader.load_station_positions()
        
        # Create stations with their lines
        station_lines = {}
        for _, row in metro_plan.iterrows():
            for station in [row['de Station'], row['vers Station']]:
                if station not in station_lines:
                    station_lines[station] = set()
                station_lines[station].add(row['de Ligne'])

        # Add GPS coordinates
        positions_dict = dict(zip(positions['Station'], positions['GPS']))
        
        # Create Station objects
        for station_name, lines in station_lines.items():
            gps_str = positions_dict.get(station_name, "")
            gps_coord = GpsCoordinate.from_string(gps_str)
            self.stations[station_name] = Station(
                name=station_name,
                lines=lines,
                gps=gps_coord
            )

    def get_all_stations(self) -> Dict[str, Station]:
        return self.stations

class MetroGraph:
    """Handles graph creation and operations"""
    def __init__(self, station_repository: StationRepository):
        self.station_repository = station_repository
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        # Add nodes (stations)
        stations = self.station_repository.get_all_stations()
        for station in stations.values():
            self.graph.add_node(station.name, 
                              lines=list(station.lines),
                              gps=station.gps)

        # Add edges (connections)
        metro_plan = DataLoader().load_metro_plan()
        for _, row in metro_plan.iterrows():
            self.graph.add_edge(
                row['de Station'],
                row['vers Station'],
                source= row['de Station'],
                destination =row['vers Station'],
                line_id=row['de Ligne'],
                flow=0,
                visited=0
            )
            self.graph.add_edge(
                row['de Station'],
                row['vers Station'],
                source= row['vers Station'],
                destination =row['de Station'],
                line_id=row['de Ligne'],
                flow=0,
                visited=0
            )

    def get_graph(self) -> nx.DiGraph:
        return self.graph


def generate_metro_graph() -> nx.DiGraph:
    """Returns a fully initialized metro graph with stations and connections"""
    data_loader = DataLoader()
    station_repository = StationRepository(data_loader)
    metro_graph = MetroGraph(station_repository)
    return metro_graph.get_graph()


def load_metro_graph() -> nx.DiGraph:
    """Loads the saved metro graph"""
    persistence = GraphPersistence()
    return persistence.load_graph()

def save_metro_graph(G: nx.DiGraph, filename:str = "metro_graph_oriented") -> None:
    """Saves the metro graph to disk"""
    persistence = GraphPersistence()
    persistence.save_graph(G, filename + ".pkl")

def main():
    # Initialize components
    data_loader = DataLoader()
    station_repository = StationRepository(data_loader)
    metro_graph = MetroGraph(station_repository)
    
    # Get the resulting graph
    G = metro_graph.get_graph()
    
    # Print some basic information
    print(f"Number of stations: {G.number_of_nodes()}")
    print(f"Number of connections: {G.number_of_edges()}")
    
    # Example: print first station's details
    first_station = list(G.nodes(data=True))[-1]
    print(f"\nExample station: {first_station}")
    
    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()
    
    # Save the graph
    persistence = GraphPersistence()
    persistence.save_graph(G)
    
    # delete the graph
    del G
    
    
    # Load the saved graph
    G = persistence.load_graph()
    
    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()
    
    # Example: print first station's details
    first_station = list(G.nodes(data=True))[0]
    print(f"\nExample station: {first_station}")
    
    
    

if __name__ == "__main__":
    main()
    