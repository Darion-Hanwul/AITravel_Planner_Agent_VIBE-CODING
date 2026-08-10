// src/router/routes.js

export const ROUTES = {
  LANDING: '/',
  DASHBOARD: '/dashboard',
  CHAT: '/chat',
  CHAT_SESSION: '/chat/:sessionId',
  DESTINATIONS: '/destinations',
  ITINERARY: '/itinerary',
  DOCUMENTS: '/documents',
  PROFILE: '/profile',
  NOT_FOUND: '*',
};

export const NAVIGATION_ITEMS = [
  {
    path: ROUTES.DASHBOARD,
    label: 'Dashboard',
    icon: 'LayoutDashboard',
    description: 'Ringkasan aktivitas dan status sistem'
  },
  {
    path: ROUTES.CHAT,
    label: 'AI Assistant',
    icon: 'MessageSquare',
    description: 'Tanya jawab RAG & perencanaan perjalanan'
  },
  {
    path: ROUTES.DESTINATIONS,
    label: 'Destinasi',
    icon: 'Compass',
    description: 'Jelajahi dan cari destinasi wisata'
  },
  {
    path: ROUTES.ITINERARY,
    label: 'Itinerary Planner',
    icon: 'Calendar',
    description: 'Kelola rencana dan susun jadwal liburan'
  },
  {
    path: ROUTES.DOCUMENTS,
    label: 'Knowledge Base',
    icon: 'FileText',
    description: 'Unggah dan kelola dokumen RAG'
  },
  {
    path: ROUTES.PROFILE,
    label: 'Profil & Pengaturan',
    icon: 'User',
    description: 'Preferensi pengguna dan sistem'
  }
];