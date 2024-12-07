import networkx as nx
from math import sqrt
from src.metro_graph.metroGraph  import load_metro_graph, GpsCoordinate
from src.simulation.passenger_flow import PassengerFlowRepository, PassengerFlow, PassengerDataLoader
from src.simulation.Astart import PathFinder, FlowProcessor, FlowUpdater

def main():
    # Initialize components
    graph = load_metro_graph()
    flow_processor = FlowProcessor(graph)
    
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)

    
    # Get all passenger flows
    flows = repository.get_all_flows()
    flow_limit = flows[:30000]
    
    print("DATA LOADED")
    # Process all flows
    paths = flow_processor.process_flows(flow_limit)

    # Print results
    # Update graph with flows
    paths.items().map(lambda _, path: )
    for flow, path in paths.items():
        # print(f"Flow from {flow[0]} to {flow[1]}")
        # print(f"Path: {path}")
        # print()
        pass

    # update graph

    print("DONE")
    
       
if __name__ == "__main__":
    main()