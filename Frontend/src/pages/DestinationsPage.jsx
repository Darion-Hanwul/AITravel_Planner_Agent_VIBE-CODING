// src/pages/DestinationsPage.jsx
import { useState } from 'react';
import PageContainer from '../components/layout/PageContainer';
import DestinationSearch from '../components/destinations/DestinationSearch';
import DestinationList from '../components/destinations/DestinationList';
import DestinationDetails from '../components/destinations/DestinationDetails';
import { useDestinations } from '../hooks/useDestinations';

export default function DestinationsPage() {
  const { destinations, loading, error, searchDestinations } = useDestinations();
  const [selectedDestination, setSelectedDestination] = useState(null);

  return (
    <PageContainer title="Eksplorasi Destinasi" subtitle="Temukan tempat wisata terbaik yang disesuaikan dengan preferensi Anda.">
      <div className="space-y-6">
        <DestinationSearch onSearch={searchDestinations} />
        <DestinationList 
          destinations={destinations} 
          loading={loading} 
          error={error} 
          onSelectDestination={(item) => setSelectedDestination(item)} 
        />
        {selectedDestination && (
          <DestinationDetails 
            destination={selectedDestination} 
            onClose={() => setSelectedDestination(null)} 
          />
        )}
      </div>
    </PageContainer>
  );
}