/* eslint-disable no-unused-vars */
import "react";
import { MessageSquare, FileText, Calendar, Compass } from "lucide-react";
import StatCard from "./StatCard";
import RecentActivities from "./RecentActivities";
import RecentDocuments from "./RecentDocuments";
import SystemStatus from "./SystemStatus";

export const DashboardOverview = ({
  stats = { sessions: 0, documents: 0, itineraries: 0 },
  recentActivities = [],
  recentDocuments = [],
}) => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard title="Total Sesi Chat AI" value={stats.sessions} icon={MessageSquare} />
        <StatCard title="Dokumen RAG Ingested" value={stats.documents} icon={FileText} />
        <StatCard title="Itinerary Tersimpan" value={stats.itineraries} icon={Calendar} />
      </div>

      <SystemStatus />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentActivities activities={recentActivities} />
        <RecentDocuments documents={recentDocuments} />
      </div>
    </div>
  );
};

export default DashboardOverview;