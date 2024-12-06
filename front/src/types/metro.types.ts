// types/metro.types.ts
export interface GpsCoordinate {
  latitude: number;
  longitude: number;
}

export interface Station {
  name: string;
  lines: string[];
  gps: GpsCoordinate | null;
}

export interface Connection {
  source: string;
  target: string;
  lineId: string;
  flow: number;
}

export interface MetroGraph {
  nodes: Station[];
  edges: Connection[];
}
