import "react";
import DestinationCard from "./DestinationCard";

export const DestinationList = ({ destinations = [], onSelectDestination }) => {
  if (destinations.length === 0) {
    return (
      <div className="text-center py-12 bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <p className="text-xs text-slate-400">Tidak ada destinasi yang ditemukan.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {destinations.map((dest) => (
        <DestinationCard
          key={dest.id || dest.name}
          destination={dest}
          onSelect={onSelectDestination}
        />
      ))}
    </div>
  );
};

export default DestinationList;