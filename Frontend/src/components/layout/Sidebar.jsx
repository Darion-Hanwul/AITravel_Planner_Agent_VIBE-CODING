import { Link } from "react-router-dom";
import { useApp } from "../../context/AppContext";
import SidebarMenu from "./SidebarMenu";
import { Compass, PanelLeftClose, PanelLeft, LogOut, User } from "lucide-react";

export const Sidebar = () => {
  const { isSidebarOpen, toggleSidebar, user, logout } = useApp();

  return (
    <aside
      className={`hidden md:flex flex-col bg-slate-950/95 border-r border-slate-800/80 transition-all duration-300 ease-in-out z-30 shrink-0 ${
        isSidebarOpen ? "w-64" : "w-20"
      }`}
    >
      {/* App Header / Brand */}
      <div className="h-16 px-4 flex items-center justify-between border-b border-slate-800/80">
        <Link to="/dashboard" className="flex items-center gap-3 overflow-hidden">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white shrink-0 shadow-lg shadow-emerald-950/40">
            <Compass className="w-5 h-5 animate-pulse" />
          </div>
          {isSidebarOpen && (
            <span className="font-bold text-base tracking-wide bg-gradient-to-r from-slate-100 to-slate-400 bg-clip-text text-transparent truncate">
              Travel AI
            </span>
          )}
        </Link>
        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
          title={isSidebarOpen ? "Sembunyikan Sidebar" : "Tampilkan Sidebar"}
        >
          {isSidebarOpen ? <PanelLeftClose className="w-5 h-5" /> : <PanelLeft className="w-5 h-5" />}
        </button>
      </div>

      {/* Navigation Menu */}
      <SidebarMenu isCollapsed={!isSidebarOpen} />

      {/* Bottom User Profile Section */}
      <div className="p-3 border-t border-slate-800/80">
        {user ? (
          <div
            className={`flex items-center gap-3 p-2 rounded-xl bg-slate-900/60 border border-slate-800/60 ${
              !isSidebarOpen ? "justify-center" : ""
            }`}
          >
            <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs shrink-0 border border-emerald-500/30">
              {user.full_name ? user.full_name.charAt(0).toUpperCase() : <User className="w-4 h-4" />}
            </div>
            {isSidebarOpen && (
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-slate-200 truncate">{user.full_name || "User"}</p>
                <p className="text-[10px] text-slate-400 truncate">{user.email || ""}</p>
              </div>
            )}
            {isSidebarOpen && (
              <button
                onClick={logout}
                title="Keluar"
                className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            )}
          </div>
        ) : (
          isSidebarOpen && (
            <div className="text-center p-2">
              <span className="text-xs text-slate-500">Travel AI Assistant</span>
            </div>
          )
        )}
      </div>
    </aside>
  );
};

export default Sidebar;