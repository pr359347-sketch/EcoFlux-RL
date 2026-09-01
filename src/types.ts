export interface Vehicle {
  id: string;
  lat: number;
  lng: number;
  speed: number;
}

export interface SimulationMetrics {
  timestamps: string[];
  total_co2: number[];
  average_wait_time: number[];
}

export interface SimulationData {
  status: string;
  vehicles: Vehicle[];
  metrics: SimulationMetrics;
}

export type ConnectionState = 'connected' | 'disconnected' | 'connecting' | 'stopped' | 'error';