import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import type { SimulationMetrics } from '../types';

interface MetricsProps {
  metrics: SimulationMetrics;
}

export default function MetricsPanel({ metrics }: MetricsProps) {
  const chartData = metrics.timestamps.map((time, index) => ({
    time,
    co2: metrics.total_co2[index] || 0,
  }));

  const latestWaitTime = metrics.average_wait_time[metrics.average_wait_time.length - 1] || 0.0;

  return (
    <div style={{ flex: 1, backgroundColor: '#1e293b', padding: '15px', display: 'flex', gap: '20px', alignItems: 'center' }}>
      <div style={{ flex: 1, backgroundColor: '#0f172a', padding: '15px', borderRadius: '8px', height: '100%' }}>
        <h4 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#94a3b8' }}>Total CO2 Emitted (ppm)</h4>
        <div style={{ width: '100%', height: '100px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <XAxis dataKey="time" stroke="#94a3b8" fontSize={10} />
              <YAxis stroke="#94a3b8" fontSize={10} />
              <Tooltip />
              <Line type="monotone" dataKey="co2" stroke="#f59e0b" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div style={{ width: '220px', backgroundColor: '#0f172a', padding: '15px', borderRadius: '8px', height: '100%' }}>
        <h4 style={{ margin: '0 0 5px 0', fontSize: '14px', color: '#94a3b8' }}>Average Wait Time</h4>
        <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#38bdf8', margin: 0 }}>
          {latestWaitTime}s
        </p>
        <span style={{ fontSize: '12px', color: '#22c55e' }}>Real-time telemetry</span>
      </div>
    </div>
  );
}