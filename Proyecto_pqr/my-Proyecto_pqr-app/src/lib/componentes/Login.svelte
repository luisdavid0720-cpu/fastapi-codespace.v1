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
  <div class="login-card">
 
    <!-- Header -->
    <div class="header">
      <div class="brand">
        <img src="/logo_cul.png" alt="Logo CUL" class="logo" />
        <div class="brand-text">
          <span class="brand-name">Corporación Universitaria</span>
          <span class="brand-sub">Latinoamericana</span>
          <span class="brand-loc">Barranquilla, Colombia</span>
        </div>
      </div>
      <div class="system-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="3" width="20" height="18" rx="2"/>
          <line x1="8" y1="3" x2="8" y2="21"/>
        </svg>
        Sistema PQRS
      </div>
    </div>
 
    <div class="divider-gradient"></div>
 
    <h1>Iniciar sesión</h1>
    <p class="subtitle">Acceso de administrador al sistema</p>
 
    <!-- Roles -->
    <div class="roles-grid">
      <button class="role-card admin" onclick={() => loginAs('admin')}>
        <div class="role-icon admin-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
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
        <div class="role-icon user-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
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
    background: #1a1a1a;
    padding: 2rem;
  }
 
  .login-card {
    background: #2a2a2a;
    border-radius: 16px;
    padding: 2rem;
    width: 100%;
    max-width: 420px;
    border: 0.5px solid rgba(255, 255, 255, 0.1);
    animation: fadeUp 0.4s ease;
  }
 
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }
 
  /* Header */
  .header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 0.5px solid rgba(255, 255, 255, 0.1);
  }
 
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
  }
 
  .logo {
    width: 52px;
    height: 52px;
    border-radius: 8px;
    object-fit: contain;
    flex-shrink: 0;
    mix-blend-mode: lighten;
  }
 
  .brand-text {
    display: flex;
    flex-direction: column;
  }
 
  .brand-name {
    font-size: 13px;
    font-weight: 600;
    color: #E8921A;
    line-height: 1.3;
  }
 
  .brand-sub {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    line-height: 1.3;
  }
 
  .brand-loc {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.35);
    line-height: 1.3;
  }
 
  .system-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.05);
    border: 0.5px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
    white-space: nowrap;
    flex-shrink: 0;
  }
 
  .divider-gradient {
    height: 2px;
    background: linear-gradient(to right, #E8921A, #1B6B3A, #1B4A7A);
    border-radius: 2px;
    margin-bottom: 1.5rem;
  }
 
  h1 {
    margin: 0 0 4px;
    font-size: 22px;
    font-weight: 700;
    color: white;
  }
 
  .subtitle {
    margin: 0 0 1.5rem;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
  }
 
  /* Roles */
  .roles-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
 
  .role-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 18px 20px;
    background: rgba(255, 255, 255, 0.04);
    border: 0.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
    width: 100%;
    color: white;
  }
 
  .role-card:hover {
    transform: translateY(-2px);
  }
 
  .role-card.admin:hover {
    border-color: #E8921A;
    background: rgba(232, 146, 26, 0.08);
  }
 
  .role-card.user:hover {
    border-color: #4a6fa5;
    background: rgba(74, 111, 165, 0.08);
  }
 
  .role-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
 
  .admin-icon {
    background: rgba(232, 146, 26, 0.15);
    color: #E8921A;
  }
 
  .user-icon {
    background: rgba(74, 111, 165, 0.15);
    color: #7aadff;
  }
 
  .role-info {
    display: flex;
    flex-direction: column;
    gap: 3px;
    flex: 1;
  }
 
  .role-title {
    font-size: 15px;
    font-weight: 600;
    color: white;
  }
 
  .role-desc {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.45);
  }
 
  .role-arrow {
    font-size: 18px;
    color: rgba(255, 255, 255, 0.3);
    transition: transform 0.2s, color 0.2s;
  }
 
  .role-card:hover .role-arrow {
    transform: translateX(4px);
  }
 
  .admin:hover .role-arrow { color: #E8921A; }
  .user:hover  .role-arrow { color: #7aadff; }
 
  @media (max-width: 480px) {
    .login-card { padding: 1.5rem; }
    h1 { font-size: 20px; }
    .header { flex-wrap: wrap; }
    .system-badge { font-size: 11px; padding: 5px 8px; }
  }
</style>