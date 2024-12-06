// stores/metrograph.ts
import { defineStore } from 'pinia';
import type { MetroGraph } from '@/types/metro.types';
import { MetroGraphService } from '@/services/MetroGraphService';

interface MetroState {
  graph: MetroGraph | null;
  loading: boolean;
  error: string | null;
}

export const useMetrographStore = defineStore('metrograph', {
  state: (): MetroState => ({
    graph: null,
    loading: false,
    error: null
  }),

  actions: {
    async loadGraph() {
      const service = new MetroGraphService();
      this.loading = true;
      this.error = null;

      try {
        // const response = await fetch('http://localhost:3000/metro_graph.json');
        // this.graph = await response.json() as MetroGraph;
        this.graph = await service.loadGraph();
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unknown error';
      } finally {
        this.loading = false;
      }
    }
  },

  getters: {
    getStationByName: (state) => {
      return (name: string) =>
        state.graph?.nodes.find(station => station.name === name);
    },

    getStationConnections: (state) => {
      return (stationName: string) =>
        state.graph?.edges.filter(
          edge => edge.source === stationName || edge.target === stationName
        ) || [];
    },

    getAllLines: (state) => {
      return () => {
        const lines = new Set<string>();
        state.graph?.nodes.forEach(station =>
          station.lines.forEach(line => lines.add(line))
        );
        return Array.from(lines);
      };
    }
  }
});
