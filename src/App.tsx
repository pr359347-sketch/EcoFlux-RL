import { useState } from 'react';
import Sidebar from './components/Sidebar';
import MapDashboard from './components/MapDashboard';
import MetricsPanel from './components/MetricsPanel';
import { useSimulationStream } from './useSimulationStream';
import './App.css';

export default function App() {
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const simulationData = useSimulationStream(isRunning);

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', margin: 0, overflow: 'hidden', backgroundColor: '#0f172a', color: '#ffffff' }}>
      <Sidebar 
        onStart={() => setIsRunning(true)} 
        onStop={() => setIsRunning(false)} 
        isRunning={isRunning}
        status={simulationData.status}
      />
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
        <MapDashboard vehicles={simulationData.vehicles} />
        <MetricsPanel metrics={simulationData.metrics} />
      </div>
    </div>
  );
}