// src/components/destinations/DestinationDetails.jsx
import 'react';
import Modal from '../common/Modal';
import Button from '../common/Button';

export default function DestinationDetails({ destination, onClose }) {
  if (!destination) return null;

  return (
    <Modal isOpen={!!destination} onClose={onClose} title={destination.title || 'Detail Destinasi'}>
      <div className="space-y-4 text-slate-300">
        {destination.imageUrl && (
          <img
            src={destination.imageUrl}
            alt={destination.title}
            className="w-full h-48 object-cover rounded-lg"
          />
        )}
        <p>{destination.description || 'Tidak ada deskripsi rinci untuk destinasi ini.'}</p>
        <div className="flex justify-between items-center pt-4 border-t border-slate-800">
          <span className="text-teal-400 font-semibold">{destination.location || 'Lokasi N/A'}</span>
          <Button variant="secondary" onClick={onClose}>
            Tutup
          </Button>
        </div>
      </div>
    </Modal>
  );
}