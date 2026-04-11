<script>
  import { currentUser } from '../../stores/auth.js';

  let username = $state('');
  let password = $state('');
  let showPassword = $state(false);

  function loginAs(rol) {
    if (rol === 'admin') {
      currentUser.set({ 
        nombre: 'Administrador', 
        correo: 'admin@cul.edu.co', 
        cedula: '123456', 
        id_rol: 1 
      });
    } else {
      currentUser.set({ 
        nombre: 'Usuario', 
        correo: 'estudiante@cul.edu.co', 
        cedula: '654321', 
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
        <img src="/logo_cul.jpg" alt="Logo CUL" class="cul-logo" />
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
        <button class="role-card admin" onclick={() => loginAs('admin')}>
          <div class="role-icon">⭐</div>
          <div class="role-info">
            <span class="role-title">Administrador</span>
            <span class="role-desc">Analítica y Control</span>
          </div>
          <span class="role-arrow">→</span>
        </button>

        <button class="role-card user" onclick={() => loginAs('usuario')}>
          <div class="role-icon">👤</div>
          <div class="role-info">
            <span class="role-title">Usuario</span>
            <span class="role-desc">Radicar y Consultar</span>
          </div>
          <span class="role-arrow">→</span>
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
          <div class="input-wrapper">
            <input type={showPassword ? "text" : "password"} id="pass" bind:value={password} placeholder="••••••••" />
            <button type="button" class="toggle-pass" onclick={() => showPassword = !showPassword}>
              {showPassword ? '👁️' : '🙈'}
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
    --border-glass: rgba(255, 255, 255, 0.6);
  }

  /* 1. FONDO CON PROFUNDIDAD */
  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
    font-family: 'Inter', system-ui, sans-serif;
    padding: 24px;
    position: relative;
    overflow: hidden;
  }

  .bg-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
    opacity: 0.4;
  }
  .blob-1 { width: 400px; height: 400px; background: var(--cul-blue); top: -100px; right: -100px; }
  .blob-2 { width: 350px; height: 350px; background: var(--cul-gold); bottom: -50px; left: -100px; }

  /* 3. SOMBRAS DINÁMICAS (Layered Shadows) */
  .login-card {
    position: relative;
    z-index: 10;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    width: 100%;
    max-width: 520px; 
    border-radius: 32px;
    border: 1px solid var(--border-glass);
    box-shadow: 
      0 1px 2px rgba(0,0,0,0.05),
      0 4px 8px rgba(0,0,0,0.05),
      0 16px 32px rgba(0,0,0,0.05),
      0 32px 64px rgba(0,0,0,0.05);
    overflow: hidden;
    animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes slideUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .card-header { padding: 45px 32px 30px; text-align: center; }
  .cul-logo { width: 100px; height: auto; margin-bottom: 16px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)); }
  .header-titles h2 { font-size: 16px; color: var(--cul-blue); margin: 0; font-weight: 800; letter-spacing: 0.5px; }
  .header-titles p { font-size: 12px; color: #475569; margin-top: 4px; font-weight: 500; }
  
  .divider { height: 6px; background: linear-gradient(to right, var(--cul-blue), var(--cul-gold)); }

  .login-content { padding: 40px; }
  .welcome-text h3 { font-size: 26px; color: #0f172a; margin: 0; font-weight: 800; }

  /* 2. TRANSICIONES DE ESTADO (Hover Effects) */
  .roles-selection { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 32px; }
  
  .role-card {
    display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 24px;
    border-radius: 20px; border: 1px solid rgba(0,0,0,0.05);
    background: rgba(255, 255, 255, 0.5); cursor: pointer; 
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
  }

  .role-card:hover { 
    transform: translateY(-8px); 
    background: white;
    border-color: var(--cul-blue);
    box-shadow: 0 12px 20px rgba(11, 31, 63, 0.1);
  }

  .role-icon { 
    width: 54px; height: 54px; background: white; border-radius: 16px;
    display: flex; align-items: center; justify-content: center; font-size: 24px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    transition: all 0.4s ease;
  }

  .role-card:hover .role-icon {
    transform: scale(1.15);
    background: var(--cul-blue);
    color: white;
    box-shadow: 0 0 15px rgba(11, 31, 63, 0.3); /* Brillo del icono */
  }

  .role-title { font-weight: 700; color: #1e293b; font-size: 16px; }
  .role-desc { font-size: 11px; color: #64748b; }

  .role-arrow { 
    position: absolute; right: 15px; top: 15px; opacity: 0; 
    transition: 0.3s; transform: rotate(-45deg); 
  }
  .role-card:hover .role-arrow { opacity: 1; transform: rotate(0deg); color: var(--cul-blue); }

  .separator { margin: 32px 0; font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
  .separator::before, .separator::after { content: ''; flex: 1; border-bottom: 1px solid rgba(0,0,0,0.08); }
  .separator span { padding: 0 15px; }

  /* INPUTS MEJORADOS */
  .input-group label { display: block; font-size: 14px; font-weight: 700; margin-bottom: 10px; color: #334155; }
  .input-wrapper input { 
    width: 100%; padding: 16px 20px; border: 1.5px solid #e2e8f0; 
    border-radius: 14px; font-size: 15px; box-sizing: border-box;
    background: rgba(248, 250, 252, 0.8); transition: all 0.3s;
  }
  .input-wrapper input:focus { 
    border-color: var(--cul-blue); background: white; 
    box-shadow: 0 0 0 4px rgba(11, 31, 63, 0.08);
  }
  
  .btn-submit { 
    width: 100%; padding: 18px; background: var(--cul-gold); 
    border: none; border-radius: 14px; font-weight: 800; color: var(--cul-blue);
    cursor: pointer; margin-top: 15px; font-size: 16px; transition: 0.4s;
    box-shadow: 0 6px 20px rgba(251, 176, 59, 0.3);
  }
  .btn-submit:hover { 
    background: #f9a01b; 
    transform: translateY(-3px); 
    box-shadow: 0 10px 25px rgba(251, 176, 59, 0.4); 
  }

  .card-footer { padding: 30px; background: rgba(248, 250, 252, 0.5); border-top: 1px solid rgba(0,0,0,0.03); text-align: center; font-size: 13px; }

  @media (max-width: 580px) {
    .login-card { border-radius: 0; }
    .roles-selection { grid-template-columns: 1fr; }
  }
</style>