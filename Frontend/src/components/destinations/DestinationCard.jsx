import "react";
import { MapPin, Star, Compass } from "lucide-react";
import Button from "../common/Button";

export const DestinationCard = ({ destination, onSelect }) => {
  return (
    <div className="group rounded-2xl bg-slate-900 border border-slate-800 overflow-hidden hover:border-slate-700 transition-all duration-300 flex flex-col h-full">
      <div className="relative h-44 overflow-hidden">
        <img
          src={destination.image || "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"}
          alt={destination.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        {destination.rating && (
          <div className="absolute top-3 right-3 px-2 py-0.5 rounded-full bg-slate-950/80 backdrop-blur-md border border-slate-700 text-amber-400 text-xs font-semibold flex items-center gap-1">
            <Star className="w-3 h-3 fill-amber-400" />
            <span>{destination.rating}</span>
          </div>
        )}
      </div>

      <div className="p-4 flex flex-col flex-1 justify-between">
        <div>
          <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            {destination.category || "Wisata"}
          </span>
          <h3 className="text-base font-bold text-slate-100 mt-2">{destination.name}</h3>
          <p className="text-xs text-slate-400 flex items-center gap-1 mt-1">
            <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0" />
            <span className="truncate">{destination.location}</span>
          </p>
          {destination.description && (
            <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
              {destination.description}
            </p>
          )}
        </div>

        <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
          <span className="text-xs font-medium text-slate-300">
            {destination.estimatedCost || "Estimasi Budget -"}
          </span>
          <Button size="sm" variant="secondary" onClick={() => onSelect(destination)}>
            <Compass className="w-3.5 h-3.5 mr-1 text-emerald-400" /> Detail
          </Button>
        </div>
      </div>
    </div>
  );
};

export default DestinationCard;