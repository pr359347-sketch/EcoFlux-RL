import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MapDashboard from './components/MapDashboard';
import MetricsPanel from './components/MetricsPanel';
import Footer from './components/Footer';
import ErrorBoundary from './components/ErrorBoundary';
import { useSimulationStream } from './useSimulationStream';
import './App.css';

export default function App() {
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const simulationData = useSimulationStream(isRunning);

  return (
    <ErrorBoundary>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', margin: 0, overflow: 'hidden', backgroundColor: '#090d16', color: '#f8fafc' }}>
        <Header />
        <div style={{ display: 'flex', flex: 1, height: 'calc(100vh - 92px)', overflow: 'hidden' }}>
          <Sidebar 
            onStart={() => setIsRunning(true)} 
            onStop={() => setIsRunning(false)} 
            isRunning={isRunning}
            status={simulationData.status}
          />
          <div style={{ display: 'flex', flexDirection: 'column', flex: 1, height: '100%', overflow: 'hidden' }}>
            <MapDashboard vehicles={simulationData.vehicles} />
            <MetricsPanel metrics={simulationData.metrics} />
          </div>
        </div>
        <Footer />
      </div>
    </ErrorBoundary>
  );
}