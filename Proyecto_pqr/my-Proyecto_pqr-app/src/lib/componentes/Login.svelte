<script>
  import { currentUser } from '../../stores/auth.js';
 
  let username = $state('');
  let password = $state('');
  let showPassword = $state(false);
 
  function loginAs(rol) {
    if (rol === 'admin') {
      currentUser.set({ 
        id_usuario: 1,
        nombre: 'Administrador', 
        correo: 'admin@cul.edu.co', 
        id_rol: 1 
      });
    } else if (rol === 'gestor') {
      currentUser.set({ 
        id_usuario: 2,
        nombre: 'Gestor PQRS', 
        correo: 'gestor@cul.edu.co', 
        id_rol: 3
      });
    } else {
      currentUser.set({ 
        id_usuario: 1,
        nombre: 'Luis Estudiante', 
        correo: 'estudiante@cul.edu.co', 
        id_rol: 2 
      });
    }
  }
</script>
 
<div class="login-page">
  <div class="bg-blob blob-1"></div>
  <div class="bg-blob blob-2"></div>
 
  <div class="login-card">
    <header class="card-header">
      <div class="logo-wrapper">
        <img src="/logo_cul.png" alt="Logo CUL" class="cul-logo" />
      </div>
      <div class="header-titles">
        <h2>Corporación Universitaria Latinoamericana</h2>
        <p>Sistema de Gestión de Peticiones, Quejas y Reclamos</p>
      </div>
    </header>
 
    <div class="divider"></div>
 
    <main class="login-content">
      <div class="welcome-text">
        <h3>Portal de Acceso</h3>
        <p>Selecciona tu perfil o ingresa con tu cuenta institucional</p>
      </div>
 
      <div class="roles-selection">
        <button class="role-card" onclick={() => loginAs('admin')}>
          <div class="role-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 1l3 6.5L22 8.7l-5 4.9 1.2 7L12 17.2l-6.2 3.4L7 13.6 2 8.7l7-1.2z"/>
            </svg>
          </div>
          <span class="role-title">Administrador</span>
          <span class="role-desc">Acceso completo</span>
        </button>
 
        <button class="role-card gestor" onclick={() => loginAs('gestor')}>
          <div class="role-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M9 11l3 3L22 4"/>
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
            </svg>
          </div>
          <span class="role-title">Gestor</span>
          <span class="role-desc">Gestión de PQRs</span>
        </button>
 
        <button class="role-card usuario" onclick={() => loginAs('usuario')}>
          <div class="role-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="8" r="4"/>
              <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
            </svg>
          </div>
          <span class="role-title">Usuario</span>
          <span class="role-desc">Mis solicitudes</span>
        </button>
      </div>
 
      <div class="separator">
        <span>Credenciales de acceso</span>
      </div>
 
      <div class="manual-form">
        <div class="input-group">
          <label for="user">Usuario o Correo</label>
          <div class="input-wrapper">
            <input type="text" id="user" bind:value={username} placeholder="Ej: l.perez@cul.edu.co" />
          </div>
        </div>
 
        <div class="input-group">
          <label for="pass">Contraseña</label>
          <div class="input-wrapper password-field">
            <input 
              type={showPassword ? "text" : "password"} 
              id="pass" 
              bind:value={password} 
              placeholder="••••••••" 
            />
            <button 
              type="button" 
              class="toggle-pass" 
              onclick={() => showPassword = !showPassword}
              aria-label="Mostrar contraseña"
            >
              {#if showPassword}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              {:else}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              {/if}
            </button>
          </div>
        </div>
 
        <button class="btn-submit" onclick={() => loginAs('admin')}>
          Ingresar al Sistema
        </button>
      </div>
    </main>
 
    <footer class="card-footer">
      <p>¿No puedes acceder? <b>Contactar a Soporte TI</b></p>
    </footer>
  </div>
</div>
 
<style>
  :root {
    --cul-blue: #0b1f3f;
    --cul-gold: #fbb03b;
  }
 
  .login-page {
    min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
    font-family: 'Inter', system-ui, sans-serif;
    padding: 24px; position: relative; overflow: hidden;
  }
 
  .bg-blob { position: absolute; border-radius: 50%; filter: blur(80px); z-index: 0; opacity: 0.3; }
  .blob-1 { width: 400px; height: 400px; background: var(--cul-blue); top: -100px; right: -100px; }
  .blob-2 { width: 350px; height: 350px; background: var(--cul-gold); bottom: -50px; left: -100px; }
 
  .login-card {
    position: relative; z-index: 10;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    width: 100%; max-width: 540px;
    border-radius: 32px; border: 1px solid rgba(255,255,255,0.6);
    box-shadow: 0 32px 64px rgba(0,0,0,0.1); overflow: hidden;
  }
 
  .card-header { padding: 40px 32px 25px; text-align: center; }
  .cul-logo { width: 90px; height: auto; margin-bottom: 12px; }
  .header-titles h2 { font-size: 15px; color: var(--cul-blue); margin: 0; font-weight: 800; }
  .header-titles p  { font-size: 11px; color: #475569; }
  .divider { height: 6px; background: linear-gradient(to right, var(--cul-blue), var(--cul-gold)); }
 
  .login-content { padding: 40px; }
  .welcome-text h3 { font-size: 24px; color: #0f172a; margin: 0; font-weight: 800; text-align: center; }
  .welcome-text p  { font-size: 13px; color: #64748b; text-align: center; margin-top: 5px; }
 
  /* 3 roles en grid */
  .roles-selection { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin: 28px 0; }
 
  .role-card {
    display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 18px 12px;
    border-radius: 18px; border: 1.5px solid #e2e8f0;
    background: white; cursor: pointer; transition: all 0.3s ease;
  }
  .role-card:hover { transform: translateY(-4px); box-shadow: 0 10px 20px rgba(11,31,63,0.1); }
 
  .role-card .role-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: #f1f5f9; color: var(--cul-blue); transition: 0.3s; }
  .role-card:hover .role-icon { background: var(--cul-blue); color: white; }
 
  .role-card.gestor:hover .role-icon { background: #16a34a; color: white; }
  .role-card.gestor:hover { border-color: #16a34a; }
 
  .role-card.usuario:hover .role-icon { background: #2563eb; color: white; }
  .role-card.usuario:hover { border-color: #2563eb; }
 
  .role-title { font-weight: 700; color: #1e293b; font-size: 13px; }
  .role-desc  { font-size: 10px; color: #94a3b8; font-weight: 500; }
 
  .separator { display: flex; align-items: center; margin: 24px 0; font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
  .separator::before, .separator::after { content: ''; flex: 1; border-bottom: 1px solid #e2e8f0; }
  .separator span { padding: 0 15px; }
 
  .input-group { margin-bottom: 18px; }
  .input-group label { display: block; font-size: 14px; font-weight: 700; margin-bottom: 8px; color: #334155; }
  .input-wrapper { position: relative; width: 100%; }
 
  input {
    width: 100%; padding: 13px 18px; border: 1.5px solid #e2e8f0;
    border-radius: 14px; font-size: 15px; box-sizing: border-box;
    background: white; transition: all 0.2s; font-family: inherit;
  }
  input:focus { outline: none; border-color: var(--cul-blue); box-shadow: 0 0 0 4px rgba(11,31,63,0.08); }
  .password-field input { padding-right: 50px; }
 
  .toggle-pass {
    position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
    background: none; border: none; cursor: pointer; color: #94a3b8;
    display: flex; align-items: center; justify-content: center; padding: 4px;
    transition: color 0.2s;
  }
  .toggle-pass:hover { color: var(--cul-blue); }
 
  .btn-submit {
    width: 100%; padding: 16px; background: var(--cul-gold);
    border: none; border-radius: 14px; font-weight: 800; color: var(--cul-blue);
    cursor: pointer; margin-top: 8px; font-size: 16px; transition: 0.3s;
    box-shadow: 0 6px 15px rgba(251,176,59,0.3); font-family: inherit;
  }
  .btn-submit:hover { background: #f9a01b; transform: translateY(-2px); }
 
  .card-footer { padding: 22px; background: rgba(248,250,252,0.5); text-align: center; font-size: 13px; border-top: 1px solid #f1f5f9; color: #64748b; }
 
  @media (max-width: 480px) {
    .login-content { padding: 24px 16px; }
    .card-header { padding: 24px 16px 16px; }
    .roles-selection { grid-template-columns: 1fr; gap: 10px; }
    .role-card { flex-direction: row; padding: 14px 16px; gap: 14px; }
    .welcome-text h3 { font-size: 20px; }
  }
</style>