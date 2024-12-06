// composables/useMetroMap.ts
import { ref, onMounted, onUnmounted } from 'vue';
import L from 'leaflet';
import { useMetrographStore } from '@/stores/metrograph';
import MapService from '@/services/MapService';
import StationMarkerService from '@/services/StationMarkerService';
import ConnectionLineService from '@/services/ConnectionLineService';

let onlyOne = true;

export function useMetroMap() {
  const mapInstance = ref<L.Map | null>(null);
  const store = useMetrographStore();

  const mapService = new MapService();
  const stationService = new StationMarkerService();
  const connectionService = new ConnectionLineService();


  const initMap = (elementId: string) => {
    const parisCenter = new L.LatLng(48.8566, 2.3522);
    mapInstance.value = mapService.initializeMap(elementId, parisCenter, 13);

    if (onlyOne) {
      onlyOne = false;

      setInterval( async () => {
        const oldGraph = store.graph;
        await store.loadGraph();
        if (oldGraph?.nodes.length !== store.graph?.nodes.length || oldGraph?.edges.length !== store.graph?.edges.length) {
          updateMap();
        }
      } , 1000
      );

    }

    updateMap();
  };

  const updateMap = () => {
    if (!mapInstance.value || !store.graph) {
      setTimeout(updateMap, 1000);
      return;
    }

    console.log('Updating map...');
    console.log(store.graph.nodes, 'stations');

    console.log(typeof store.graph.nodes[5].gps);
    const validStations = store.graph.nodes.filter(station =>
      station.gps !== null
    );

    console.log(validStations.length, 'valid stations');

    stationService.addStationMarkers(mapInstance.value as L.Map, validStations);
    connectionService.addConnectionLines(
      mapInstance.value as L.Map,
      store.graph.edges,
      validStations
    );
  };

  onMounted(async () => {
    await store.loadGraph();
  });

  onUnmounted(() => {
    stationService.removeStationMarkers();
    connectionService.removeConnectionLines();
    mapInstance.value?.remove();
  });

  return {
    mapInstance,
    initMap,
    updateMap
  };
}
