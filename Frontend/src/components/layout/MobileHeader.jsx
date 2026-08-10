import { Link } from "react-router-dom";
import { useApp } from "../../context/AppContext";
import { Compass, Menu, X } from "lucide-react";

export const MobileHeader = () => {
  const { isMobileMenuOpen, toggleMobileMenu } = useApp();

  return (
    <header className="md:hidden h-14 px-4 bg-slate-950/90 backdrop-blur-md border-b border-slate-800 flex items-center justify-between sticky top-0 z-40">
      <Link to="/dashboard" className="flex items-center gap-2.5">
        <div className="p-1.5 rounded-lg bg-emerald-600 text-white">
          <Compass className="w-4 h-4" />
        </div>
        <span className="font-bold text-sm text-slate-100 tracking-wide">Travel AI</span>
      </Link>

      <button
        onClick={toggleMobileMenu}
        className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        aria-label="Toggle Menu"
      >
        {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>
    </header>
  );
};

export default MobileHeader;