export default function Sidebar({ 
  sessions, 
  currentSessionId, 
  setCurrentSessionId, 
  handleInisialisasiAkun, 
  handleBuatSesiBaru, 
  authToken, 
  loading, 
  statusLog,
  onOpenSettings 
}) {
  return (
    <div style={{ width: '280px', backgroundColor: '#1e1e20', borderRight: '1px solid #2f2f31', display: 'flex', flexDirection: 'column', padding: '15px' }}>
      <h3 style={{ margin: '0 0 15px 0', fontSize: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: '#fff' }}>
        ✈️ Travel AI Agent
      </h3>
      
      <button
        onClick={handleInisialisasiAkun}
        disabled={!!authToken || loading}
        style={{ width: '100%', padding: '10px', backgroundColor: authToken ? '#2e7d32' : '#0b57d0', color: '#fff', border: 'none', borderRadius: '8px', cursor: authToken ? 'default' : 'pointer', fontWeight: 'bold', marginBottom: '10px' }}
      >
        {authToken ? '✓ Autentikasi Siap' : 'Inisialisasi Akun Tes'}
      </button>

      <button
        onClick={handleBuatSesiBaru}
        disabled={!authToken || loading}
        style={{ width: '100%', padding: '10px', backgroundColor: 'transparent', color: '#a8c7fa', border: '1px dashed #a8c7fa', borderRadius: '8px', cursor: 'pointer', marginBottom: '20px' }}
      >
        + Buat Sesi Perjalanan Baru
      </button>

      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <div style={{ fontSize: '12px', color: '#757575', fontWeight: 'bold', marginBottom: '5px' }}>RIWAYAT PERJALANAN</div>
        {sessions.map((sess) => {
          const sessId = sess.id || sess.session_id;
          const isActive = currentSessionId === sessId;
          return (
            <div
              key={sessId}
              onClick={() => setCurrentSessionId(sessId)}
              style={{ padding: '10px', borderRadius: '8px', backgroundColor: isActive ? '#004b87' : 'transparent', cursor: 'pointer', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', transition: 'background 0.2s' }}
            >
              📍 {sess.title || 'Sesi Tanpa Judul'}
            </div>
          );
        })}
      </div>
      
      <div style={{ borderTop: '1px solid #2f2f31', paddingTop: '10px', marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <button 
          onClick={onOpenSettings}
          style={{ width: '100%', padding: '8px', backgroundColor: '#2d2d30', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '13px' }}
        >
          ⚙️ Pengaturan Sistem
        </button>
        <div style={{ fontSize: '11px', color: '#757575' }}>
          Status: {statusLog}
        </div>
      </div>
    </div>
  );
}