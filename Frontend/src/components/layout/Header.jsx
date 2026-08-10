import { useLocation } from "react-router-dom";
import { useApp } from "../../context/AppContext";
import { Bell, User, Wifi } from "lucide-react";

export const Header = () => {
  const location = useLocation();
  const { user } = useApp();

  const getPageTitle = (path) => {
    if (path.startsWith("/dashboard")) return "Dashboard Overview";
    if (path.startsWith("/chat")) return "AI Travel Assistant";
    if (path.startsWith("/trips")) return "Perjalanan Saya";
    if (path.startsWith("/itinerary")) return "Perencana Itinerary";
    if (path.startsWith("/destinations")) return "Eksplorasi Destinasi";
    if (path.startsWith("/documents")) return "Knowledge Base (RAG)";
    if (path.startsWith("/profile")) return "Pengaturan Profil";
    return "Travel AI";
  };

  return (
    <header className="hidden md:flex h-16 px-6 bg-slate-950/60 backdrop-blur-md border-b border-slate-800/80 items-center justify-between sticky top-0 z-20">
      <div>
        <h1 className="text-base font-semibold text-slate-100">{getPageTitle(location.pathname)}</h1>
        <p className="text-[11px] text-slate-400">Rencanakan petualangan cerdas Anda bersama AI</p>
      </div>

      <div className="flex items-center gap-4">
        {/* System Status Indicator */}
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <Wifi className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-[11px] font-medium text-slate-300">Sistem Online</span>
        </div>

        {/* Notifications Icon */}
        <button
          className="p-2 rounded-xl text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors relative"
          title="Notifikasi"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-emerald-500" />
        </button>

        {/* User Profile Avatar */}
        {user && (
          <div className="flex items-center gap-2.5 pl-2 border-l border-slate-800">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-slate-200 flex items-center justify-center font-bold text-xs">
              {user.full_name ? user.full_name.charAt(0).toUpperCase() : <User className="w-4 h-4" />}
            </div>
            <div className="hidden lg:block text-left">
              <p className="text-xs font-medium text-slate-200">{user.full_name || "User"}</p>
              <p className="text-[10px] text-slate-400">Pengguna Aktif</p>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;