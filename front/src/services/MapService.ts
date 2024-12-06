// services/MapService.ts
import L from 'leaflet';
import type { IMapService } from '@/types/map.types';

export default class MapService implements IMapService {
  initializeMap(element: string, center: L.LatLng, zoom: number): L.Map {
    const map = L.map(element).setView(center, zoom);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    return map;
  }
}
