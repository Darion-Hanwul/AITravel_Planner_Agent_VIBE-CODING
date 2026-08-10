// src/pages/ProfilePage.jsx
import 'react';
import PageContainer from '../components/layout/PageContainer';
import ProfileCard from '../components/profile/ProfileCard';
import PreferencesForm from '../components/profile/PreferencesForm';
import ProfileSettings from '../components/profile/ProfileSettings';

export default function ProfilePage() {
  return (
    <PageContainer title="Profil & Pengaturan" subtitle="Atur profil pribadi dan preferensi sistem rekomendasi AI.">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <ProfileCard />
        </div>
        <div className="lg:col-span-2 space-y-6">
          <PreferencesForm />
          <ProfileSettings />
        </div>
      </div>
    </PageContainer>
  );
}