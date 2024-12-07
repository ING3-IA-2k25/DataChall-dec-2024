# scripts/convert_graph.py
import json
import networkx as nx
import sys

from src.metro_graph.metroGraph import load_metro_graph, GpsCoordinate

def convert_graph_to_json(G: nx.Graph = None):
    if G is None:
        raise ValueError("G is None")
    
    try:
        
        graph_data = {
            "nodes": [
            {
                "name": node,
                "lines": data.get("lines", []),
                "gps": {
                    "latitude": data.get("gps", 0).latitude,
                    "longitude": data.get("gps", 0).longitude
                } if data.get("gps", False) else "null"
            }
            for node, data in G.nodes(data=True)
            ],
            "edges": [
            {
                "source": data.get("source", "ERROR"),
                "target": data.get("destination", "ERROR"),
                "lineId": data.get("line_id", "ERROR"),
                "flow": data.get("flow", 0),
                "visited-source-To-target": data.get("visited_STT", 0),
                "visited-target-To-source": data.get("visited_TTS", 0)
            }
            for u, v, data in G.edges(data=True)
            ]
        }
        
        # Ensure proper encoding of special characters
        with open("data/metro_graph.json", "w", encoding='utf-8') as f:
            print("Saving graph data to data/metro_graph.json")
            json.dump(graph_data, f, indent=4, ensure_ascii=False)
       
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
        
        
if __name__ == "__main__":
    convert_graph_to_json(load_metro_graph())