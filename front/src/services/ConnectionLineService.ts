// services/ConnectionLineService.ts
import L from 'leaflet';
import type { IConnectionLineService } from '@/types/map.types';
import type { Connection, Station } from '@/types/metro.types';

export default class ConnectionLineService implements IConnectionLineService {
  private lines: L.Polyline[] = [];

  addConnectionLines(map: L.Map, connections: Connection[], stations: Station[]): L.Polyline[] {
    this.removeConnectionLines();

    const stationMap = new Map(
      stations.filter(station =>
        station.gps !== null
      ).map(station => [station.name, station])
    );

    this.lines = connections
      .filter(connection => {
        const source = stationMap.get(connection.source);
        const target = stationMap.get(connection.target);
        console.log('source:', source);
        return !(!source || !target || source!.gps === null || target!.gps=== null || isNaN(source!.gps.latitude) || isNaN(source!.gps.longitude) || isNaN(target!.gps.latitude) || isNaN(target!.gps.longitude));
      })
      .map(connection => {
        const source = stationMap.get(connection.source)!;
        const target = stationMap.get(connection.target)!;

        if (!source.gps || !target.gps) {
          return null;
        }

        const coords = [
          [source.gps.latitude, source.gps.longitude],
          [target.gps.latitude, target.gps.longitude]
        ] as L.LatLngExpression[];

        const line = L.polyline(coords, {
          color: this.getLineColor(connection.lineId),
          weight: 4
        });

        line.addTo(map);
        return line;
      })
      .filter((line): line is L.Polyline => line !== null);

    console.log('Connection lines added:', this.lines.length);
    return this.lines;
  }


  removeConnectionLines(): void {
    this.lines.forEach(line => line.remove());
    this.lines = [];
  }

  private getLineColor(lineId: string): string {
    // Map metro line numbers to colors
    const lineColors: Record<string, string> = {
      '1': '#FFCD00',
      '2': '#003CA6',
      '3': '#837902',
      '4': '#CF009E',
      '5': '#FF7E2E',
      '6': '#6ECA97',
      '7': '#FA9ABA',
      '8': '#9B9B9B',
      '9': '#B6BD00',
      '10': '#C9910D',
      '11': '#704B1C',
      '12': '#007852',
      '13': '#6EC4E8',
      '14': '#62259D'
    };
    return lineColors[lineId] || '#666666';
  }
}
