// services/MetroGraphService.ts
import type { MetroGraph } from '@/types/metro.types';

export interface IMetroGraphService {
  loadGraph(): Promise<MetroGraph>;
}

export class MetroGraphService implements IMetroGraphService {
  async loadGraph(): Promise<MetroGraph> {
    return fetch('http://localhost:3000/metro_graph.json').then(response =>  response.json() as Promise<MetroGraph>);
  }
}
