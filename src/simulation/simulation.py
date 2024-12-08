import numpy as np
from src.metro_graph.metroGraph  import load_metro_graph, GpsCoordinate, save_metro_graph
from src.simulation.passenger_flow import PassengerFlowRepository, PassengerFlow, PassengerDataLoader
from src.simulation.Astart import PathFinder, FlowProcessor, FlowUpdater
from src.metro_graph.accebilite import load_data_set, save_dataset
from src.simulation.disjktra_GPU import Dijkstra_GPU, build_graph_gpu, dijkstras_matrix, FlowUpdaterMatrix
from typing import List
import networkx as nx

    

def test_simulation(iter: int):
    # Initialize components
    graph = load_metro_graph()
    flow_processor = FlowProcessor(graph)
    
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)

    
    # Get all passenger flows
    flows = repository.get_all_flows()
    flow_limit = flows#[:iter]
    
    print("DATA LOADED")
    # Process all flows
    paths = flow_processor.process_flows_parallel(flow_limit)

    # Print results
    # Update graph with flows
    print("FIN A*")
    flow_updater = FlowUpdater(graph)


    # zip(paths.items()).map(lambda flow, path: flow_updater.update_flow(path, flow.count))
    for (source, dest, count), path in paths.items():
        if path:
            # print(count)
            flow_updater.update_flow(path, count)
            print(f"Flow from {source} to {dest} with {count} passengers")
            print(f"Path: {path}")
    #     # print()
    #     pass
    save_metro_graph(graph)

    print("DONE")
    
def run_simulation():
      # Initialize components
    dataset = load_data_set("connected_graphs_1000.pkl")
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)
    # graph = load_metro_graph()
    
    flows = repository.get_all_flows()
    dataset_output = []
    index = 0
    
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
        if index % 25 == 0:
            print(f"Graph {index} done")
        index += 1
    # print(f"Nombre de flux échoués: {echec}")
    # save_metro_graph(graph, "output_graph")
    save_dataset(dataset_output, "output_graphs_1000.pkl")
    

def run_simulation_GPU(adj_matrice: np.array, flows: list[PassengerFlow], station_to_idx):
    # initializations
    processor = Dijkstra_GPU(adj_matrice)
       
    # updater
    updater = FlowUpdaterMatrix(adj_matrice)
    
    # run dijkstra on GPU
    distances, get_path, predecessors = processor.process_passenger_flows(flows)
    
    # update flows
    for flow in flows:
        local_path = get_path(station_to_idx[flow.source], station_to_idx[flow.destination], predecessors)
        updater.update_flow(local_path, flow.count)
    
    return updater.adj_matrix


def run_batch_simulation_GPU(adj_list: List[np.array], station_to_idx):
    # get all flows
    data_loader = PassengerDataLoader()
    repository = PassengerFlowRepository(data_loader)    
    flows = repository.get_all_flows()
    
    # run simulation
    output_matrices = [ run_simulation_GPU(adj_matrice, flows, station_to_idx) for adj_matrice in adj_list] 
    
    # compress output matrices
    # compress_output_matrices(output_matrices)
    
    # save dataset
    #save_dataset(output_matrices, "dataset_output.pkl")
    return output_matrices

def main():
    G = load_metro_graph()
    
    #data_loader = PassengerDataLoader()
    #repository = PassengerFlowRepository(data_loader)    
    #flows = repository.get_all_flows()

    station_to_idx = {name: idx for idx, name in enumerate(G.nodes()) }
    
    batch = [nx.to_numpy_array(G) for _ in range(10)]
    #output = run_simulation_GPU(nx.to_numpy_array(G), flows, station_to_idx)
    output = run_batch_simulation_GPU(batch, station_to_idx)
    print(output[0])


if __name__ == "__main__":
    # test_simulation(900000)
    
    # run_simulation()
    pass
    