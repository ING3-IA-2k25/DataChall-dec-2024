# scripts/convert_graph.py
import json
import networkx as nx
import sys

from metroGraph import load_metro_graph

def convert_graph_to_json():
    try:
        G = load_metro_graph()
        
        graph_data = {
            "nodes": [
            {
                "name": node,
                "lines": data.get("lines", []),
                "gps": {
                    "latitude": data.get("gps", 0).split(",")[0],
                    "longitude": data.get("gps", 0).split(",")[1]
                } if data.get("gps", False) else None
            }
            for node, data in G.nodes(data=True)
            ],
            "edges": [
            {
                "source": u,
                "target": v,
                "lineId": data.get("line_id", ""),
                "flow": data.get("flow", 0)
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
    convert_graph_to_json()