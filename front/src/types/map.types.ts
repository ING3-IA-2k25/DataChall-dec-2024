// types/map.types.ts
import type { LatLng, Map, Circle , Polyline } from 'leaflet';
import type { Station, Connection } from '@/types/metro.types';

export interface IMapService {
  initializeMap(element: string, center: LatLng, zoom: number): Map;
}

export interface IStationMarkerService {
  addStationMarkers(map: Map, stations: Station[]): Circle[];
  removeStationMarkers(): void;
}

export interface IConnectionLineService {
  addConnectionLines(map: Map, connections: Connection[], stations: Station[]): Polyline[];
  removeConnectionLines(): void;
}
