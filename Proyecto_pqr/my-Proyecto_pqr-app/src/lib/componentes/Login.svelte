<script>
  import { currentUser } from '../../stores/auth.js';

  // Variables para los campos (aunque por ahora solo usaremos los botones de rol)
  let username = $state('');
  let password = $state('');
  let showPassword = $state(false);

  // Mantenemos tu lógica original de loginAs
  function loginAs(rol) {
    if (rol === 'admin') {
      currentUser.set({ 
        nombre: 'Luis (Administrador)', 
        correo: 'admin@cul.edu.co', 
        cedula: '123456', 
        id_rol: 1 
      });
    } else {
      currentUser.set({ 
        nombre: 'Juan Pérez', 
        correo: 'estudiante@cul.edu.co', 
        cedula: '654321', 
        id_rol: 2 
      });
    }
  }
</script>

<div class="login-page">
  <div class="login-card">
    <header class="card-header">
      <div class="logo-wrapper">
        <img src="/logo_cul.jpg" alt="Logo CUL" class="cul-logo" />
      </div>
      <div class="header-titles">
        <h2>Corporación Universitaria Latinoamericana</h2>
        <p>Sistema de Gestión PQRS</p>
      </div>
    </header>

    <div class="divider"></div>

    <main class="login-content">
      <div class="welcome-text">
        <h3>Bienvenido</h3>
        <p>Selecciona tu tipo de acceso para continuar</p>
      </div>

      <div class="roles-selection">
        <button class="role-card admin" onclick={() => loginAs('admin')}>
          <div class="role-icon">⭐</div>
          <div class="role-info">
            <span class="role-title">Administrador</span>
            <span class="role-desc">Acceso completo y analítica</span>
          </div>
          <span class="role-arrow">→</span>
        </button>

        <button class="role-card user" onclick={() => loginAs('usuario')}>
          <div class="role-icon">👤</div>
          <div class="role-info">
            <span class="role-title">Usuario</span>
            <span class="role-desc">Gestión de PQRs propias</span>
          </div>
          <span class="role-arrow">→</span>
        </button>
      </div>

      <div class="separator">
        <span>O ingresa con tus credenciales</span>
      </div>

      <div class="manual-form">
        <div class="input-group">
          <label for="user">Usuario</label>
          <div class="input-wrapper">
            <input type="text" id="user" bind:value={username} placeholder="Usuario o correo" />
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
          Ingresar →
        </button>
      </div>
    </main>

    <footer class="card-footer">
      <p>¿Necesitas ayuda? <b>Soporte Técnico CUL</b></p>
    </footer>
  </div>
</div>

<style>
  :root {
    --cul-blue: #0b1f3f;
    --cul-gold: #fbb03b;
    --border-color: #e2e8f0;
  }

  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f1f5f9;
    font-family: 'Inter', system-ui, sans-serif;
    padding: 20px;
  }

  .login-card {
    background: white;
    width: 100%;
    max-width: 440px;
    border-radius: 20px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    animation: fadeIn 0.4s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Header con Logo */
  .card-header { padding: 30px 24px; text-align: center; }
  .cul-logo { width: 90px; height: auto; margin-bottom: 12px; }
  .header-titles h2 { font-size: 15px; color: var(--cul-blue); margin: 0; font-weight: 700; }
  .header-titles p { font-size: 12px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .divider { height: 4px; background: linear-gradient(to right, var(--cul-blue), var(--cul-gold)); }

  .login-content { padding: 32px; }
  .welcome-text { margin-bottom: 24px; text-align: center; }
  .welcome-text h3 { font-size: 22px; color: #0f172a; margin: 0; font-weight: 800; }
  .welcome-text p { font-size: 14px; color: #64748b; margin-top: 6px; }

  /* Estilo de las tarjetas de Rol */
  .roles-selection { display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; }
  
  .role-card {
    display: flex; align-items: center; gap: 16px; padding: 16px;
    border-radius: 12px; border: 1px solid var(--border-color);
    background: #f8fafc; cursor: pointer; transition: all 0.2s;
    width: 100%; text-align: left;
  }

  .role-card:hover { 
    transform: translateY(-2px); 
    border-color: var(--cul-blue);
    background: #eff6ff;
  }

  .role-icon { 
    width: 44px; height: 44px; background: white; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }

  .role-info { flex: 1; display: flex; flex-direction: column; }
  .role-title { font-weight: 700; color: #1e293b; font-size: 15px; }
  .role-desc { font-size: 11px; color: #64748b; }
  .role-arrow { color: #cbd5e1; font-weight: bold; }
  .role-card:hover .role-arrow { color: var(--cul-blue); transform: translateX(3px); }

  .separator { 
    display: flex; align-items: center; text-align: center; 
    margin: 24px 0; font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;
  }
  .separator::before, .separator::after { content: ''; flex: 1; border-bottom: 1px solid var(--border-color); }
  .separator span { padding: 0 12px; }

  /* Formulario Manual */
  .input-group { margin-bottom: 16px; }
  .input-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #475569; }
  .input-wrapper { position: relative; }
  .input-wrapper input { 
    width: 100%; padding: 11px 16px; border: 1px solid var(--border-color); 
    border-radius: 10px; font-size: 14px; outline: none; transition: 0.2s;
    box-sizing: border-box;
  }
  .input-wrapper input:focus { border-color: var(--cul-blue); box-shadow: 0 0 0 3px rgba(11, 31, 63, 0.05); }
  
  .toggle-pass { position: absolute; right: 12px; top: 10px; border: none; background: none; cursor: pointer; opacity: 0.6; }

  .btn-submit { 
    width: 100%; padding: 13px; background: var(--cul-gold); 
    border: none; border-radius: 10px; font-weight: 700; color: var(--cul-blue);
    cursor: pointer; margin-top: 8px; transition: 0.2s;
  }
  .btn-submit:hover { background: #e69d2f; transform: translateY(-1px); }

  .card-footer { padding: 20px; background: #f8fafc; text-align: center; font-size: 12px; color: #64748b; }
  .card-footer b { color: var(--cul-blue); cursor: pointer; }
</style>