import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Location } from '../types/api';
import L from 'leaflet';

interface ForecastMapProps {
  location: Location;
}

const icon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

export function ForecastMap({ location }: ForecastMapProps) {
  return (
    <MapContainer
      center={[location.latitude, location.longitude]}
      zoom={10}
      scrollWheelZoom={false}
      className="h-64 w-full rounded-xl overflow-hidden"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[location.latitude, location.longitude]} icon={icon}>
        <Popup>
          <strong>{location.name ?? 'Selected location'}</strong>
          <br />
          lat {location.latitude.toFixed(3)}, lon {location.longitude.toFixed(3)}
        </Popup>
      </Marker>
    </MapContainer>
  );
}
