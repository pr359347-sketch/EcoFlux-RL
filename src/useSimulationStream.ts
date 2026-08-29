import { useState, useEffect } from 'react';
import type { SimulationData } from './types';

export function useSimulationStream(isRunning: boolean): SimulationData {
  const [data, setData] = useState<SimulationData>({
    status: 'stopped',
    vehicles: [],
    metrics: {
      timestamps: [],
      total_co2: [],
      average_wait_time: [],
    }
  });

  useEffect(() => {
    if (!isRunning) {
      setData(prev => ({ ...prev, status: 'stopped' }));
      return;
    }

    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/simulation';
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setData(prev => ({ ...prev, status: 'connected' }));
    };

    ws.onmessage = (event) => {
      try {
        const parsed: SimulationData = JSON.parse(event.data);
        setData(parsed);
      } catch (e) {
        console.error("Failed to parse WebSocket message", e);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setData(prev => ({ ...prev, status: 'error' }));
    };

    ws.onclose = () => {
      setData(prev => ({ ...prev, status: 'disconnected' }));
    };

    return () => {
      ws.close();
    };
  }, [isRunning]);

  return data;
}