import { useEffect } from "react";
import { useApp } from "../../context/AppContext";
import SidebarMenu from "./SidebarMenu";
import { Compass, X, LogOut, User } from "lucide-react";

export const MobileSidebar = () => {
  const { isMobileMenuOpen, setMobileMenuOpen, user, logout } = useApp();

  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
  }, [isMobileMenuOpen]);

  if (!isMobileMenuOpen) return null;

  return (
    <div className="md:hidden fixed inset-0 z-50 flex">
      {/* Overlay Backdrop */}
      <div
        className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity"
        onClick={() => setMobileMenuOpen(false)}
      />

      {/* Drawer Content */}
      <div className="relative w-4/5 max-w-xs bg-slate-950 h-full border-r border-slate-800 flex flex-col z-10 animate-in slide-in-from-left duration-200">
        <div className="h-14 px-4 flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-emerald-600 text-white">
              <Compass className="w-4 h-4" />
            </div>
            <span className="font-bold text-sm text-slate-100">Travel AI</span>
          </div>
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <SidebarMenu onItemClick={() => setMobileMenuOpen(false)} />

        {/* User Footer Info */}
        <div className="p-4 border-t border-slate-800">
          {user && (
            <div className="flex items-center justify-between bg-slate-900 p-2.5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2.5 min-w-0">
                <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs shrink-0">
                  {user.full_name ? user.full_name.charAt(0).toUpperCase() : <User className="w-4 h-4" />}
                </div>
                <div className="min-w-0">
                  <p className="text-xs font-medium text-slate-200 truncate">{user.full_name || "User"}</p>
                  <p className="text-[10px] text-slate-400 truncate">{user.email || ""}</p>
                </div>
              </div>
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  logout();
                }}
                className="p-1.5 text-slate-400 hover:text-rose-400 rounded-lg"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MobileSidebar;