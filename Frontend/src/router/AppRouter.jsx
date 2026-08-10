/* eslint-disable no-unused-vars */
// src/router/AppRouter.jsx
import  { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ROUTES } from './routes';
import MainLayout from '../components/layout/MainLayout';
import Loading from '../components/common/Loading';

// Lazy loading halaman
const LandingPage = lazy(() => import('../pages/LandingPage'));
const DashboardPage = lazy(() => import('../pages/DashboardPage'));
const ChatPage = lazy(() => import('../pages/ChatPage'));
const DestinationsPage = lazy(() => import('../pages/DestinationsPage'));
const ItineraryPage = lazy(() => import('../pages/ItineraryPage'));
const DocumentsPage = lazy(() => import('../pages/DocumentsPage'));
const ProfilePage = lazy(() => import('../pages/ProfilePage'));
const NotFoundPage = lazy(() => import('../pages/NotFoundPage'));

const PageLoader = () => (
  <div className="flex justify-center items-center h-screen w-full bg-slate-900 text-white">
    <Loading size="lg" text="Memuat halaman..." />
  </div>
);

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* Public Landing Page */}
          <Route path={ROUTES.LANDING} element={<LandingPage />} />

          {/* Protected/App Shell Layout Routes */}
          <Route element={<MainLayout />}>
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route path={ROUTES.CHAT} element={<ChatPage />} />
            <Route path={ROUTES.CHAT_SESSION} element={<ChatPage />} />
            <Route path={ROUTES.DESTINATIONS} element={<DestinationsPage />} />
            <Route path={ROUTES.ITINERARY} element={<ItineraryPage />} />
            <Route path={ROUTES.DOCUMENTS} element={<DocumentsPage />} />
            <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
          </Route>

          {/* 404 Not Found Page */}
          <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}