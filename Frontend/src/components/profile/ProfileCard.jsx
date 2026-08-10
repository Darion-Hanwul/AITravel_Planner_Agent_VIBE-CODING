import "react";
import { User, Mail, Shield } from "lucide-react";

export const ProfileCard = ({ user }) => {
  const userData = user || {
    name: "Traveler Explorer",
    email: "user@example.com",
    role: "Standard User",
  };

  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex items-center gap-4">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center font-bold text-xl shadow-lg">
        <User className="w-8 h-8" />
      </div>
      <div className="space-y-1">
        <h3 className="text-base font-bold text-slate-100">{userData.name}</h3>
        <p className="text-xs text-slate-400 flex items-center gap-1.5">
          <Mail className="w-3.5 h-3.5 text-slate-500" /> {userData.email}
        </p>
        <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
          <Shield className="w-3 h-3" /> {userData.role}
        </span>
      </div>
    </div>
  );
};

export default ProfileCard;