export default function Header() {
  return (
    <header style={{ height: '60px', backgroundColor: '#0f172a', borderBottom: '1px solid #1e293b', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#10b981', boxShadow: '0 0 10px #10b981' }}></div>
        <h1 style={{ margin: 0, fontSize: '18px', fontWeight: 600, letterSpacing: '0.5px' }}>EcoTwin <span style={{ color: '#38bdf8', fontWeight: 400 }}>| Urban Traffic & Emissions Intelligence</span></h1>
      </div>
      <div style={{ display: 'flex', gap: '16px', fontSize: '13px', color: '#94a3b8' }}>
        <span>Environment: <strong style={{ color: '#10b981' }}>Production</strong></span>
        <span>Version: <strong style={{ color: '#f8fafc' }}>v1.0.4</strong></span>
      </div>
    </header>
  );
}