interface SidebarProps {
  onStart: () => void;
  onStop: () => void;
  isRunning: boolean;
  status: string;
}

export default function Sidebar({ onStart, onStop, isRunning, status }: SidebarProps) {
  return (
    <aside style={{ width: '300px', padding: '24px', borderRight: '1px solid #1e293b', backgroundColor: '#0f172a', display: 'flex', flexDirection: 'column', height: 'calc(100vh - 60px)' }}>
      <div>
        <h2 style={{ fontSize: '16px', margin: '0 0 4px 0', color: '#f8fafc' }}>Simulation Control</h2>
        <p style={{ color: '#64748b', fontSize: '13px', margin: 0 }}>Manage live telemetry feed</p>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '24px' }}>
        <button 
          onClick={onStart}
          style={{ padding: '12px 16px', backgroundColor: '#10b981', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600, fontSize: '14px', transition: 'background 0.2s', boxShadow: '0 4px 12px rgba(16, 185, 129, 0.2)' }}>
          ▶ Start Simulation
        </button>
        <button 
          onClick={onStop}
          style={{ padding: '12px 16px', backgroundColor: '#ef4444', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600, fontSize: '14px', transition: 'background 0.2s', boxShadow: '0 4px 12px rgba(239, 68, 68, 0.2)' }}>
          ⏹ Stop Simulation
        </button>
      </div>

      <div style={{ marginTop: 'auto', padding: '16px', backgroundColor: '#1e293b', borderRadius: '10px', border: '1px solid #334155' }}>
        <h4 style={{ margin: '0 0 8px 0', color: '#94a3b8', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>WebSocket Status</h4>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: isRunning ? '#10b981' : '#ef4444' }}></div>
          <p style={{ margin: 0, color: isRunning ? '#34d399' : '#f87171', fontWeight: 600, fontSize: '14px', textTransform: 'uppercase' }}>
            {status}
          </p>
        </div>
      </div>
    </aside>
  );
}