// src/pages/DashboardPage.jsx
import 'react';
import PageContainer from '../components/layout/PageContainer';
import DashboardOverview from '../components/dashboard/DashboardOverview';
import RecentActivities from '../components/dashboard/RecentActivities';
import RecentDocuments from '../components/dashboard/RecentDocuments';
import SystemStatus from '../components/dashboard/SystemStatus';

export default function DashboardPage() {
  return (
    <PageContainer title="Dashboard Perjalanan" subtitle="Ringkasan asisten AI, data dokumen, dan aktivitas terkini Anda.">
      <div className="space-y-6">
        {/* Ringkasan Statistik */}
        <DashboardOverview />

        {/* Baris Kedua: Aktivitas & Status Dokumen */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <RecentActivities />
            <RecentDocuments />
          </div>
          <div className="lg:col-span-1">
            <SystemStatus />
          </div>
        </div>
      </div>
    </PageContainer>
  );
}