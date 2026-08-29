import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import type { Vehicle } from '../types';
import 'leaflet/dist/leaflet.css';

interface MapDashboardProps {
  vehicles: Vehicle[];
}

export default function MapDashboard({ vehicles }: MapDashboardProps) {
  const centerPosition: [number, number] = [12.9716, 77.5946];

  return (
    <div style={{ flex: 2, position: 'relative', width: '100%', height: '100%' }}>
      <MapContainer center={centerPosition} zoom={14} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {vehicles.map((veh) => (
          <Marker key={veh.id} position={[veh.lat, veh.lng]}>
            <Popup>
              Vehicle ID: {veh.id} <br /> Speed: {veh.speed} m/s
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}