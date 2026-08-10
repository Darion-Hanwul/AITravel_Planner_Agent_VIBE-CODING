// src/pages/ItineraryPage.jsx
import 'react';
import PageContainer from '../components/layout/PageContainer';
import ItineraryBuilder from '../components/itinerary/ItineraryBuilder';
import ItineraryControls from '../components/itinerary/ItineraryControls';
import { useItinerary } from '../hooks/useItinerary';

export default function ItineraryPage() {
  const { currentItinerary, loading, saveItinerary, exportItinerary } = useItinerary();

  return (
    <PageContainer 
      title="Itinerary Planner" 
      subtitle="Rencanakan dan atur rincian perjalanan liburan Anda secara terstruktur."
      action={<ItineraryControls onSave={saveItinerary} onExport={exportItinerary} />}
    >
      <div className="space-y-6">
        <ItineraryBuilder itinerary={currentItinerary} loading={loading} />
      </div>
    </PageContainer>
  );
}