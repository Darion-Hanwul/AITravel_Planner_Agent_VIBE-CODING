import { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import SettingsModal from './components/SettingsUser'; 

function App() {
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState('');
  const [messages, setMessages] = useState([]);
  const [inputUser, setInputUser] = useState('');
  const [loading, setLoading] = useState(false);
  const [authToken, setAuthToken] = useState('');
  const [statusLog, setStatusLog] = useState('Silakan inisialisasi akun pengujian Anda.');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false); // State untuk mengontrol modal setting

  const [testUser] = useState(() => {
    const randomId = Math.floor(100 + Math.random() * 900);
    return {
      full_name: `Traveler Resmi ${randomId}`,
      email: `tester_${randomId}@example.com`,
      password: "PassAman123!"
    };
  });

  const fetchSessions = async (token) => {
    const activeToken = token || authToken;
    if (!activeToken) return;
    try {
      const res = await axios.get('http://localhost:8000/chats/sessions', {
        headers: { Authorization: `Bearer ${activeToken}` }
      });
      setSessions(res.data);
    } catch (err) {
      console.error("Gagal mengambil sesi:", err);
    }
  };

  const handleInisialisasiAkun = async () => {
    setLoading(true);
    setStatusLog('Mendaftarkan user ke PostgreSQL...');
    try {
      await axios.post('http://localhost:8000/auth/signup', {
        full_name: testUser.full_name,
        email: testUser.email,
        password: testUser.password
      });

      setStatusLog('Sign Up sukses! Mengambil Token JWT...');
      
      const loginForm = new URLSearchParams();
      loginForm.append('username', testUser.email);
      loginForm.append('password', testUser.password);

      const loginRes = await axios.post('http://localhost:8000/auth/signin', loginForm, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      const token = loginRes.data.access_token;
      setAuthToken(token);
      setStatusLog('Koneksi aman terjalin! Memuat daftar sesi...');
      
      fetchSessions(token);

    } catch (error) {
      console.error(error);
      setStatusLog(`Gagal: ${error.response?.data?.detail || 'Periksa koneksi backend Anda.'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBuatSesiBaru = async () => {
    if (!authToken) return;
    setLoading(true);
    try {
      const randomNomor = Math.floor(10 + Math.random() * 90);
      const res = await axios.post(
        'http://localhost:8000/chats/sessions',
        { title: `Rencana Wisata #${randomNomor}` },
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      const newSession = res.data;
      setSessions(prev => [newSession, ...prev]);
      setCurrentSessionId(newSession.id || newSession.session_id);
      setMessages([]); 
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKirimPesan = async (e) => {
    e.preventDefault();
    if (!inputUser.trim() || !currentSessionId) return;

    const pesanTeks = inputUser;
    setInputUser('');

    const temporaryMessage = {
      id: Date.now().toString(),
      role: 'user',
      message: pesanTeks,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, temporaryMessage]);

    try {
      await axios.post(
        `http://localhost:8000/chats/sessions/${currentSessionId}/messages`,
        null,
        {
          params: { message_text: pesanTeks },
          headers: { Authorization: `Bearer ${authToken}` }
        }
      );
      
      // Mengambil pesan terbaru dari server secara aman
      const res = await axios.get(`http://localhost:8000/chats/sessions/${currentSessionId}/messages`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setMessages(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  // Efek samping untuk sinkronisasi pesan otomatis saat sesi aktif berubah
  useEffect(() => {
    const loadMessages = async () => {
      if (!currentSessionId || !authToken) return;
      try {
        const res = await axios.get(`http://localhost:8000/chats/sessions/${currentSessionId}/messages`, {
          headers: { Authorization: `Bearer ${authToken}` }
        });
        setMessages(res.data);
      } catch (err) {
        console.error("Gagal mengambil pesan:", err);
      }
    };

    loadMessages();
  }, [currentSessionId, authToken]);

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif', backgroundColor: '#131314', color: '#e3e3e3', overflow: 'hidden' }}>
      
      {/* Memanggil Komponen Sidebar */}
      <Sidebar 
        sessions={sessions}
        currentSessionId={currentSessionId}
        setCurrentSessionId={setCurrentSessionId}
        handleInisialisasiAkun={handleInisialisasiAkun}
        handleBuatSesiBaru={handleBuatSesiBaru}
        authToken={authToken}
        loading={loading}
        statusLog={statusLog}
        onOpenSettings={() => setIsSettingsOpen(true)} // Aksi saat tombol setting di klik
      />
      
      {/* Memanggil Komponen Area Chat */}
      <ChatWindow 
        messages={messages}
        currentSessionId={currentSessionId}
        inputUser={inputUser}
        setInputUser={setInputUser}
        handleKirimPesan={handleKirimPesan}
      />
      
      {/* Memanggil Komponen Modal Pengaturan */}
      <SettingsModal 
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        testUser={testUser}
      />
      
    </div>
  );
}

export default App;