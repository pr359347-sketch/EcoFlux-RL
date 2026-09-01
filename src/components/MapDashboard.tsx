import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import type { Vehicle } from '../types';
import 'leaflet/dist/leaflet.css';

interface MapDashboardProps {
  vehicles: Vehicle[];
}

export default function MapDashboard({ vehicles }: MapDashboardProps) {
  const centerPosition: [number, number] = [12.9716, 77.5946];

  return (
    <div style={{ flex: 2, position: 'relative', width: '100%', height: '100%', borderBottom: '1px solid #1e293b' }}>
      <MapContainer center={centerPosition} zoom={14} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {vehicles.map((veh) => (
          <Marker key={veh.id} position={[veh.lat, veh.lng]}>
            <Popup>
              <div style={{ color: '#0f172a', fontWeight: 600 }}>Vehicle ID: {veh.id}</div>
              <div style={{ color: '#475569', fontSize: '12px' }}>Speed: {veh.speed} m/s</div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}