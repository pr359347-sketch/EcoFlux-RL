import { useState, useEffect } from 'react';
import type { SimulationData } from './types';

export function useMockStream(enabled: boolean): SimulationData {
  const [data, setData] = useState<SimulationData>({
    status: enabled ? 'running' : 'stopped',
    vehicles: [
      { id: 'v_101', lat: 12.9716, lng: 77.5946, speed: 15.4 },
      { id: 'v_102', lat: 12.9740, lng: 77.5920, speed: 12.1 },
    ],
    metrics: {
      timestamps: ['12:00', '12:01', '12:02'],
      total_co2: [1100, 1150, 1120],
      average_wait_time: [28.5, 27.2, 26.8],
    }
  });

  useEffect(() => {
    if (!enabled) return;
    const interval = setInterval(() => {
      setData(prev => ({
        ...prev,
        metrics: {
          ...prev.metrics,
          total_co2: [...prev.metrics.total_co2.slice(1), prev.metrics.total_co2[prev.metrics.total_co2.length - 1] + 5]
        }
      }));
    }, 1000);
    return () => clearInterval(interval);
  }, [enabled]);

  return data;
}