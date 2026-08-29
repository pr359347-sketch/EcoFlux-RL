import { useState, useEffect } from 'react';
import type { SimulationData } from './types';

export function useMockStream(): SimulationData {
  const [simulationData, setSimulationData] = useState<SimulationData>({
    status: 'running',
    vehicles: [
      { id: 'veh_1', lat: 12.9716, lng: 77.5946, speed: 12.5 },
      { id: 'veh_2', lat: 12.9750, lng: 77.5900, speed: 14.2 },
    ],
    metrics: {
      timestamps: ['10:00', '10:01', '10:02', '10:03'],
      total_co2: [1200, 1250, 1310, 1420],
      average_wait_time: [35, 33, 36, 34.2],
    }
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setSimulationData((prev) => ({
        ...prev,
        vehicles: prev.vehicles.map(v => ({
          ...v,
          lat: v.lat + (Math.random() - 0.5) * 0.001,
          lng: v.lng + (Math.random() - 0.5) * 0.001,
        })),
        metrics: {
          ...prev.metrics,
          total_co2: [...prev.metrics.total_co2.slice(1), prev.metrics.total_co2[prev.metrics.total_co2.length - 1] + Math.floor(Math.random() * 10)]
        }
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return simulationData;
}