// services/StationMarkerService.ts
import L from 'leaflet';
import type { IStationMarkerService } from '@/types/map.types';
import type { Station } from '@/types/metro.types';

export default class StationMarkerService implements IStationMarkerService {
  private circles: L.Circle[] = [];

  addStationMarkers(map: L.Map, stations: Station[]): L.Circle[] {
    this.removeStationMarkers();

    this.circles = stations
      .filter(station => {
        if (!station.gps === null) return false;
        const lat = station.gps!.latitude
        const lng = station.gps!.longitude
        return station.gps !== null && !isNaN(lat) && !isNaN(lng)
    })
      .map(station => {
        const circle = L.circle(
          [station.gps!.latitude, station.gps!.longitude],
          {
            color: this.getStationColor(station),
            fillColor: this.getStationColor(station),
            fillOpacity: 0.75,
            radius: 50,
            weight: 2
          }
        );

        // Add hover effect
        circle.on('mouseover', () => {
          circle.setStyle({
            fillOpacity: 1
          });
          circle.setRadius(75);

          // Show station info
          L.popup()
            .setLatLng([station.gps!.latitude, station.gps!.longitude])
            .setContent(`
              <b>${station.name}</b><br>
              Lines: ${station.lines.join(', ')}
            `)
            .openOn(map);
        });

        circle.on('mouseout', () => {
          circle.setStyle({
            fillOpacity: 0.7
          });
          circle.setRadius(50);
        });

        circle.addTo(map);
        return circle;
      });

    console.log('Station markers added:', this.circles.length);
    return this.circles;
  }

  removeStationMarkers(): void {
    this.circles.forEach(circle => circle.remove());
    this.circles = [];
  }

  private getStationColor(station: Station): string {
    // Color based on number of lines
    const lineCount = station.lines.length;
    if (lineCount > 2) return '#E53E3E'; // Red for major hubs
    if (lineCount === 2) return '#DD6B20'; // Orange for transfers
    return '#3182CE'; // Blue for regular stations
  }
}
