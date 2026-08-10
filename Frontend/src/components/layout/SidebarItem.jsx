import { Link } from "react-router-dom";
import * as Icons from "lucide-react";

export const SidebarItem = ({ item, isActive, isCollapsed, onClick }) => {
  // Dynamic Icon Loader dari Lucide Icons
  const IconComponent = Icons[item.iconName] || Icons.Circle;

  return (
    <Link
      to={item.path}
      onClick={onClick}
      title={isCollapsed ? item.label : undefined}
      className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl transition-all duration-200 group relative select-none ${
        isActive
          ? "bg-emerald-500/10 text-emerald-400 font-medium border border-emerald-500/20 shadow-sm"
          : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60"
      }`}
    >
      <IconComponent
        className={`w-5 h-5 shrink-0 transition-transform duration-200 group-hover:scale-110 ${
          isActive ? "text-emerald-400" : "text-slate-400 group-hover:text-slate-200"
        }`}
      />
      {!isCollapsed && (
        <span className="text-sm truncate font-medium">{item.label}</span>
      )}

      {/* Indicator Dot jika aktif dan collapsed */}
      {isActive && isCollapsed && (
        <div className="absolute right-2 w-1.5 h-1.5 rounded-full bg-emerald-400" />
      )}
    </Link>
  );
};

export default SidebarItem;