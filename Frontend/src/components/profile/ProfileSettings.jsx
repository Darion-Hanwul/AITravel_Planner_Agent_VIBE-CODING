import "react";
import ProfileCard from "./ProfileCard";
import PreferencesForm from "./PreferencesForm";

export const ProfileSettings = ({ user, onSavePreferences }) => {
  return (
    <div className="space-y-6">
      <ProfileCard user={user} />
      <PreferencesForm onSave={onSavePreferences} />
    </div>
  );
};

export default ProfileSettings;