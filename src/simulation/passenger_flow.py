
from dataclasses import dataclass
from typing import Dict, List
import pandas as pd
from pathlib import Path

@dataclass
class PassengerFlow:
    """Represents a flow of passengers between stations"""
    source: str
    destination: str
    count: int

class PassengerDataLoader:
    """Handles loading passenger data from CSV"""
    def __init__(self, data_path: str = "./data/passagers.csv"):
        self.data_path = Path(data_path)

    def load_passenger_data(self) -> pd.DataFrame:
        """Load passenger flow data from CSV"""
        try:
            return pd.read_csv(self.data_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Passenger data file not found at {self.data_path}")

class PassengerFlowRepository:
    """Manages passenger flow data and operations"""
    def __init__(self, data_loader: PassengerDataLoader):
        self.data_loader = data_loader
        self.flows: Dict[tuple[str, str], PassengerFlow] = {}
        self._init_flows()

    def _init_flows(self) -> None:
        """Initialize passenger flows from data"""
        df = self.data_loader.load_passenger_data()
        for _, row in df.iterrows():
            key = (row['de'], row['vers'])
            self.flows[key] = PassengerFlow(
                source=row['de'],
                destination=row['vers'],
                count=row['nombre']
            )

    def get_all_flows(self) -> List[PassengerFlow]:
        """Return all passenger flows"""
        return list(self.flows.values())

    def get_flow(self, source: str, destination: str) -> PassengerFlow:
        """Get specific flow between two stations"""
        key = (source, destination)
        if key not in self.flows:
            raise KeyError(f"No flow found between {source} and {destination}")
        return self.flows[key]

def main():
    """Example usage"""
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)
  
    #print resume
    print("Nombre de flux de passagers: ", len(repository.get_all_flows()))
    print("Nombre de passagers total: ", sum([flow.count for flow in repository.get_all_flows()]))
      
    # Print all flows
    # for flow in repository.get_all_flows():
    #     print(f"{flow.source} -> {flow.destination}: {flow.count} passengers")

if __name__ == "__main__":
    main()