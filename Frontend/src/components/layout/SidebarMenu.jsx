import { useLocation } from "react-router-dom";
import { NAVIGATION_ITEMS } from "../../config/navigation";
import SidebarItem from "./SidebarItem";

export const SidebarMenu = ({ isCollapsed = false, onItemClick }) => {
  const location = useLocation();

  return (
    <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
      {NAVIGATION_ITEMS.map((item) => {
        const isActive =
          location.pathname === item.path ||
          (item.path !== "/dashboard" && location.pathname.startsWith(item.path));

        return (
          <SidebarItem
            key={item.id}
            item={item}
            isActive={isActive}
            isCollapsed={isCollapsed}
            onClick={onItemClick}
          />
        );
      })}
    </nav>
  );
};

export default SidebarMenu;