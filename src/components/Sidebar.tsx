interface SidebarProps {
  onStart: () => void;
  onStop: () => void;
  isRunning: boolean;
  status: string;
}

export default function Sidebar({ onStart, onStop, isRunning, status }: SidebarProps) {
  return (
    <div style={{ width: '280px', padding: '20px', borderRight: '1px solid #334155', backgroundColor: '#1e293b', display: 'flex', flexDirection: 'column', height: '100%' }}>
      <h2>EcoTwin Dashboard</h2>
      <p style={{ color: '#94a3b8', fontSize: '14px' }}>Production Control Panel</p>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '20px' }}>
        <button 
          onClick={onStart}
          style={{ padding: '12px', backgroundColor: '#22c55e', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>
          Start Simulation
        </button>
        <button 
          onClick={onStop}
          style={{ padding: '12px', backgroundColor: '#ef4444', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>
          Stop Simulation
        </button>
      </div>

      <div style={{ marginTop: 'auto', padding: '15px', backgroundColor: '#0f172a', borderRadius: '8px' }}>
        <h4 style={{ margin: '0 0 10px 0', color: '#94a3b8', fontSize: '13px' }}>Connection Status</h4>
        <p style={{ margin: 0, color: isRunning ? '#22c55e' : '#ef4444', fontWeight: 'bold', textTransform: 'uppercase' }}>
          {status}
        </p>
      </div>
    </div>
  );
}