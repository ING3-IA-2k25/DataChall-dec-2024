import os
from typing import List
from dataclasses import dataclass
from metroGraph import DataLoader, StationRepository


class StationAnalyzer:
    """Analyzes station data for missing or invalid information"""
    def __init__(self, station_repository: StationRepository):
        self.station_repository = station_repository
        
    def get_stations_without_gps(self) -> List[str]:
        """Returns list of station names that don't have GPS coordinates"""
        stations = self.station_repository.get_all_stations()
        return [
            station.name 
            for station in stations.values() 
            if not station.gps or station.gps.strip() == ""
        ]



def main():
    data_loader = DataLoader()
    station_repository = StationRepository(data_loader)
    analyzer = StationAnalyzer(station_repository)
    
    # Get stations without GPS
    stations_without_gps = analyzer.get_stations_without_gps()
    
    # Print results
    print("\nStations without GPS coordinates:")
    print("=================================")
    for station in stations_without_gps:
        print(f"- {station}")
    print(f"\nTotal: {len(stations_without_gps)} stations without GPS coordinates")
    print(f"Total stations: {len(station_repository.get_all_stations())}")
if __name__ == "__main__":
    main()