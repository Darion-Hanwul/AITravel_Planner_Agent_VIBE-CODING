export default function ChatWindow({ messages, currentSessionId, inputUser, setInputUser, handleKirimPesan }) {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#131314' }}>
      {/* Header */}
      <div style={{ height: '60px', borderBottom: '1px solid #2f2f31', display: 'flex', alignItems: 'center', padding: '0 20px' }}>
        <div style={{ fontWeight: '500', color: '#fff' }}>
          {currentSessionId ? `Sesi Aktif: ${currentSessionId.substring(0, 8)}...` : 'Silakan Pilih atau Buat Sesi Baru'}
        </div>
      </div>

      {/* Area Pesan */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '15px' }}>
        {messages.length === 0 ? (
          <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: '#757575', textAlign: 'center' }}>
            <span style={{ fontSize: '40px', marginBottom: '10px' }}>🗺️</span>
            <h3>Mau liburan ke mana kali ini?</h3>
            <p style={{ fontSize: '14px', maxWidth: '400px', margin: '0' }}>Ketikkan rencana perjalanan Anda di kolom bawah. Pesan otomatis tersinkronisasi ke PostgreSQL.</p>
          </div>
        ) : (
          messages.map((msg) => {
            const isUser = msg.role === 'user';
            return (
              <div key={msg.id} style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', width: '100%' }}>
                <div style={{ maxWidth: '70%', padding: '12px 16px', borderRadius: '16px', backgroundColor: isUser ? '#0b57d0' : '#1e1e20', color: '#fff', fontSize: '15px', whiteSpace: 'pre-line' }}>
                  <div style={{ fontSize: '11px', color: isUser ? '#c2dbff' : '#9e9e9e', marginBottom: '4px', fontWeight: 'bold' }}>
                    {isUser ? 'KAMU' : 'AI AGENT'}
                  </div>
                  {msg.message}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Form Input */}
      <div style={{ padding: '20px', borderTop: '1px solid #2f2f31' }}>
        <form onSubmit={handleKirimPesan} style={{ display: 'flex', maxWidth: '800px', margin: '0 auto', gap: '10px' }}>
          <input
            type="text"
            value={inputUser}
            onChange={(e) => setInputUser(e.target.value)}
            disabled={!currentSessionId}
            placeholder={currentSessionId ? "Ketik pesan Anda di sini..." : "Pilih/buat sesi di sidebar untuk mulai mengetik..."}
            style={{ flex: 1, padding: '14px 20px', borderRadius: '24px', border: '1px solid #3c4043', backgroundColor: '#1e1e20', color: '#fff', fontSize: '15px', outline: 'none' }}
          />
          <button
            type="submit"
            disabled={!currentSessionId || !inputUser.trim()}
            style={{ padding: '0 24px', borderRadius: '24px', border: 'none', backgroundColor: (!currentSessionId || !inputUser.trim()) ? '#2f2f31' : '#a8c7fa', color: '#041e49', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Kirim
          </button>
        </form>
      </div>
    </div>
  );
}