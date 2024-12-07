import networkx as nx
from math import sqrt
from src.metro_graph.metroGraph  import load_metro_graph, GpsCoordinate, save_metro_graph
from src.simulation.passenger_flow import PassengerFlowRepository, PassengerFlow, PassengerDataLoader
from src.simulation.Astart import PathFinder, FlowProcessor, FlowUpdater
from src.metro_graph.accebilite import load_data_set, save_dataset

def test_simulation(iter: int):
    # Initialize components
    graph = load_metro_graph()
    flow_processor = FlowProcessor(graph)
    
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)

    
    # Get all passenger flows
    flows = repository.get_all_flows()
    flow_limit = flows[:iter]
    
    print("DATA LOADED")
    # Process all flows
    paths = flow_processor.process_flows(flow_limit)

    # Print results
    # Update graph with flows
    flow_updater = FlowUpdater(graph)


    # zip(paths.items()).map(lambda flow, path: flow_updater.update_flow(path, flow.count))
    for (source, dest, count), path in paths.items():
        if path:
            # print(count)
            flow_updater.update_flow(path, count)
    #     # print(f"Flow from {flow[0]} to {flow[1]}")
    #     # print(f"Path: {path}")
    #     # print()
    #     pass
    save_metro_graph(graph)

    print("DONE")
    
def run_simulation():
      # Initialize components
    dataset = load_data_set("connected_graphs_10.pkl")
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)
    # graph = load_metro_graph()
    
    flows = repository.get_all_flows()
    dataset_output = []
    
    for graph in dataset:
        flow_processor = FlowProcessor(graph)    
        
        flow_updater = FlowUpdater(graph)
        
        # initializations
        # flow_updater.initialize_flow_counters()
        
        # run A*
        paths = flow_processor.process_flows(flows)
        
        # update graph with flows
        echec = 0
        for (source, dest, count), path in paths.items():
            if path:
                flow_updater.update_flow(path, count)
            else:
                echec += 1
        
        dataset_output.append(graph)
    # print(f"Nombre de flux échoués: {echec}")
    # save_metro_graph(graph, "output_graph")
    save_dataset(dataset_output, "output_graphs_1000.pkl")
    
            
    
if __name__ == "__main__":
    # test_simulation(30000)
    # load_metro_graph()
    
    # run_simulation()
    pass
    