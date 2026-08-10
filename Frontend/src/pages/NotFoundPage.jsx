// src/pages/NotFoundPage.jsx
import 'react';
import { Link } from 'react-router-dom';
import { MapPinOff, ArrowLeft } from 'lucide-react';
import { ROUTES } from '../router/routes';
import Button from '../components/common/Button';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-6 bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-rose-500/10 text-rose-500 rounded-full border border-rose-500/20">
          <MapPinOff className="w-10 h-10" />
        </div>
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-white tracking-tight">404</h1>
          <h2 className="text-xl font-semibold text-slate-200">Destinasi Tidak Ditemukan</h2>
          <p className="text-sm text-slate-400">
            Jalur atau halaman yang Anda tuju tampaknya tidak ada dalam peta aplikasi kami.
          </p>
        </div>
        <div className="pt-2">
          <Link to={ROUTES.DASHBOARD}>
            <Button variant="primary" className="w-full flex items-center justify-center gap-2">
              <ArrowLeft className="w-4 h-4" /> Kembali ke Dashboard
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}