import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";
import MobileHeader from "./MobileHeader";
import MobileSidebar from "./MobileSidebar";
import Toast from "../common/Toast";

export const MainLayout = () => {
  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Desktop Sidebar */}
      <Sidebar />

      {/* Mobile Sidebar / Drawer */}
      <MobileSidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden relative">
        {/* Top Header Navigation */}
        <Header />
        <MobileHeader />

        {/* Dynamic Page Views */}
        <main className="flex-1 overflow-y-auto relative bg-gradient-to-b from-slate-950 via-slate-900/40 to-slate-950">
          <Outlet />
        </main>
      </div>

      {/* Global Toast Container */}
      <Toast />
    </div>
  );
};

export default MainLayout;