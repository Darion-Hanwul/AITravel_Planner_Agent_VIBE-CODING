import "react";
import { Link } from "react-router-dom";
import { MapPin, Star, ArrowRight } from "lucide-react";
import Button from "../common/Button";

const featuredDestinations = [
  {
    id: 1,
    name: "Raja Ampat",
    location: "Papua Barat, Indonesia",
    rating: 4.9,
    category: "Bahari & Alam",
    image: "https://images.unsplash.com/photo-1516690561799-46d8f74f9abf?auto=format&fit=crop&w=800&q=80",
  },
  {
    id: 2,
    name: "Ubud",
    location: "Bali, Indonesia",
    rating: 4.8,
    category: "Budaya & Relaksasi",
    image: "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80",
  },
  {
    id: 3,
    name: "Labuan Bajo",
    location: "Nusa Tenggara Timur, Indonesia",
    rating: 4.9,
    category: "Petualangan",
    image: "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=800&q=80",
  },
];

export const DestinationSection = () => {
  return (
    <section id="destinations" className="py-20 px-6 lg:px-12 bg-slate-950">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">Destinasi Favorit</h2>
            <p className="mt-2 text-sm text-slate-400 max-w-lg">
              Temukan inspirasi lokasi petualangan populer yang siap dijadwalkan oleh AI Assistant.
            </p>
          </div>
          <Link to="/destinations">
            <Button variant="outline" size="sm" className="gap-2 self-start md:self-auto">
              <span>Lihat Semua Destinasi</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {featuredDestinations.map((item) => (
            <div
              key={item.id}
              className="group rounded-2xl bg-slate-900 border border-slate-800 overflow-hidden hover:border-slate-700 transition-all duration-300"
            >
              <div className="relative h-48 overflow-hidden">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-slate-950/70 backdrop-blur-md border border-slate-700 text-amber-400 text-xs font-semibold flex items-center gap-1">
                  <Star className="w-3.5 h-3.5 fill-amber-400" />
                  <span>{item.rating}</span>
                </div>
              </div>
              <div className="p-5">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                  {item.category}
                </span>
                <h3 className="text-lg font-bold text-slate-100 mt-2">{item.name}</h3>
                <p className="text-xs text-slate-400 flex items-center gap-1 mt-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-500" />
                  {item.location}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default DestinationSection;