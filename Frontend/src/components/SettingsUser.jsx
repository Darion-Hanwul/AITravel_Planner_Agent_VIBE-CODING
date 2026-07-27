export default function SettingsModal({ isOpen, onClose, testUser }) {
  if (!isOpen) return null;

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
      <div style={{ backgroundColor: '#1e1e20', padding: '25px', borderRadius: '12px', width: '450px', border: '1px solid #3c4043', color: '#e3e3e3' }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#fff' }}>⚙️ Pengaturan Aplikasi</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', marginBottom: '25px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#9e9e9e', marginBottom: '5px' }}>DATABASE USER TEST</label>
            <input type="text" readOnly value={testUser.email} style={{ width: '100%', padding: '10px', backgroundColor: '#131314', border: '1px solid #3c4043', borderRadius: '6px', color: '#fff' }} />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#9e9e9e', marginBottom: '5px' }}>TARGET AI ENGINE (FUTURE)</label>
            <select style={{ width: '100%', padding: '10px', backgroundColor: '#131314', border: '1px solid #3c4043', borderRadius: '6px', color: '#fff' }}>
              <option>LangChain Custom Agent (Default)</option>
              <option>Gemini 1.5 Pro</option>
              <option>OpenAI GPT-4o</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#9e9e9e', marginBottom: '5px' }}>ENDPOINT BACKEND</label>
            <input type="text" readOnly value="http://localhost:8000" style={{ width: '100%', padding: '10px', backgroundColor: '#131314', border: '1px solid #3c4043', borderRadius: '6px', color: '#757575' }} />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button 
            onClick={onClose}
            style={{ padding: '8px 16px', backgroundColor: '#0b57d0', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Tutup & Simpan
          </button>
        </div>
      </div>
    </div>
  );
}