// services/MetroGraphService.ts
import type { MetroGraph } from '@/types/metro.types';
import graphData from '@/data/metro_graph.json';

export interface IMetroGraphService {
  loadGraph(): Promise<MetroGraph>;
}

export class MetroGraphService implements IMetroGraphService {
  async loadGraph(): Promise<MetroGraph> {
    return Promise.resolve(graphData as MetroGraph);
  }
}
