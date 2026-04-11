<script>
  import { currentUser } from '../../stores/auth.js';
 
  function loginAs(rol) {
    if (rol === 'admin') {
      currentUser.set({ nombre: 'Administrador', correo: 'admin@pqr.com', cedula: '123456', id_rol: 1 });
    } else {
      currentUser.set({ nombre: 'Juan Pérez', correo: 'user@pqr.com', cedula: '654321', id_rol: 2 });
    }
  }
</script>
 
<div class="login-bg">
  <div class="glow"></div>
  <div class="login-card">
    <div class="brand">
      <div class="brand-icon">
        <img src="/logo_cul.png" alt="Logo CUL" style="width: 40px; height: 40px; object-fit: contain;" />
      </div>
      <span class="brand-name">Sistema PQRS</span>
    </div>
    <h1>Bienvenido</h1>
    <p class="subtitle">Selecciona tu tipo de acceso para continuar</p>
    <div class="roles-grid">
      <button class="role-card admin" onclick={() => loginAs('admin')}>
        <div class="role-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M12 1l3 6.5L22 8.7l-5 4.9 1.2 7L12 17.2l-6.2 3.4L7 13.6 2 8.7l7-1.2z"/>
          </svg>
        </div>
        <div class="role-info">
          <span class="role-title">Administrador</span>
          <span class="role-desc">Acceso completo al sistema</span>
        </div>
        <span class="role-arrow">→</span>
      </button>
      <button class="role-card user" onclick={() => loginAs('usuario')}>
        <div class="role-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="8" r="4"/>
            <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
          </svg>
        </div>
        <div class="role-info">
          <span class="role-title">Usuario</span>
          <span class="role-desc">Gestión de PQRs propias</span>
        </div>
        <span class="role-arrow">→</span>
      </button>
    </div>
  </div>
</div>
 
<style>
  .login-bg {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    position: relative;
    overflow: hidden;
  }
  .glow {
    position: absolute;
    width: 700px; height: 700px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(45,45,58,0.04) 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }
  .login-card {
    position: relative; z-index: 1;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 20px; padding: 48px 44px;
    width: 100%; max-width: 440px;
    box-shadow: var(--shadow); animation: fadeUp 0.5s ease;
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .brand { display: flex; align-items: center; gap: 10px; margin-bottom: 32px; }
  .brand-name { font-family: var(--font-display); font-weight: 700; font-size: 18px; letter-spacing: -0.02em; }
  h1 { font-family: var(--font-display); font-size: 32px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; margin-bottom: 8px; }
  .subtitle { color: var(--text-muted); font-size: 14px; margin-bottom: 32px; }
  .roles-grid { display: flex; flex-direction: column; gap: 14px; }
  .role-card {
    display: flex; align-items: center; gap: 16px; padding: 20px;
    border-radius: var(--radius); border: 1px solid var(--border);
    background: var(--surface2); color: var(--text);
    text-align: left; transition: all 0.2s; width: 100%;
  }
  .role-card:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
  .role-card.admin:hover { border-color: var(--accent); background: rgba(45,45,58,0.04); box-shadow: var(--shadow-accent); }
  .role-card.user:hover  { border-color: var(--accent2); background: rgba(74,111,165,0.05); }
  .role-icon {
    width: 52px; height: 52px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }
  .admin .role-icon { background: rgba(45,45,58,0.08); color: var(--accent); }
  .user .role-icon  { background: rgba(74,111,165,0.1); color: var(--accent2); }
  .role-info { display: flex; flex-direction: column; gap: 3px; flex: 1; }
  .role-title { font-family: var(--font-display); font-size: 17px; font-weight: 700; letter-spacing: -0.02em; }
  .role-desc { font-size: 13px; color: var(--text-muted); }
  .role-arrow { font-size: 18px; color: var(--text-muted); transition: transform 0.2s, color 0.2s; }
  .role-card:hover .role-arrow { transform: translateX(4px); }
  .admin:hover .role-arrow { color: var(--accent); }
  .user:hover  .role-arrow { color: var(--accent2); }
  @media (max-width: 480px) {
    .login-card { padding: 32px 24px; margin: 16px; }
    h1 { font-size: 26px; }
  }
</style>