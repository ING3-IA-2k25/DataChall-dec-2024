// types/map.types.ts
import type { LatLng, Map, Marker, Polyline } from 'leaflet';
import type { Station, Connection } from '@/types/metro.types';

export interface IMapService {
  initializeMap(element: string, center: LatLng, zoom: number): Map;
}

export interface IStationMarkerService {
  addStationMarkers(map: Map, stations: Station[]): Marker[];
  removeStationMarkers(): void;
}

export interface IConnectionLineService {
  addConnectionLines(map: Map, connections: Connection[], stations: Station[]): Polyline[];
  removeConnectionLines(): void;
}
