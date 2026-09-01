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
    <div style={{ height: '180px', backgroundColor: '#0f172a', padding: '16px 24px', display: 'flex', gap: '20px', alignItems: 'center', borderTop: '1px solid #1e293b' }}>
      <div style={{ flex: 2, backgroundColor: '#1e293b', padding: '16px', borderRadius: '12px', height: '100%', border: '1px solid #334155', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
          <h4 style={{ margin: 0, fontSize: '13px', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total CO2 Emissions (ppm)</h4>
          <span style={{ fontSize: '11px', color: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', padding: '2px 8px', borderRadius: '4px' }}>Live Stream</span>
        </div>
        <div style={{ width: '100%', flex: 1 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }} />
              <Line type="monotone" dataKey="co2" stroke="#f59e0b" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div style={{ flex: 1, backgroundColor: '#1e293b', padding: '20px', borderRadius: '12px', height: '100%', border: '1px solid #334155', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h4 style={{ margin: '0 0 8px 0', fontSize: '13px', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Average Wait Time</h4>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
          <p style={{ fontSize: '32px', fontWeight: 700, color: '#38bdf8', margin: 0, lineHeight: 1 }}>
            {latestWaitTime}s
          </p>
          <span style={{ fontSize: '12px', color: '#10b981', fontWeight: 600 }}>Optimized</span>
        </div>
      </div>
    </div>
  );
}