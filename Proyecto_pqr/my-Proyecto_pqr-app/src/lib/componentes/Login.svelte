<script>
  import { currentUser } from '../../stores/auth.js';

  let username = $state('');
  let password = $state('');
  let showPassword = $state(false);

  // FUNCIÓN CORREGIDA: Ahora envía el id_usuario para que el filtro funcione
  function loginAs(rol) {
    if (rol === 'admin') {
      currentUser.set({ 
        id_usuario: 1, // ID base para pruebas
        nombre: 'Administrador', 
        correo: 'admin@cul.edu.co', 
        id_rol: 1 
      });
    } else {
      currentUser.set({ 
        id_usuario: 1, // <--- CLAVE: Ahora tus trámites aparecerán
        nombre: 'Luis Estudiante', 
        correo: 'estudiante@cul.edu.co', 
        id_rol: 2 
      });
    }
    // Nota: Aquí podrías añadir un goto('/dashboard') si usas SvelteKit routing
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
          <div class="role-icon">⭐</div>
          <span class="role-title">Administrador</span>
        </button>

        <button class="role-card" onclick={() => loginAs('usuario')}>
          <div class="role-icon">👤</div>
          <span class="role-title">Usuario</span>
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
              {showPassword ? '🙈' : '🐵'}
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

  /* FONDO Y BLOBS */
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

  .bg-blob { position: absolute; border-radius: 50%; filter: blur(80px); z-index: 0; opacity: 0.3; }
  .blob-1 { width: 400px; height: 400px; background: var(--cul-blue); top: -100px; right: -100px; }
  .blob-2 { width: 350px; height: 350px; background: var(--cul-gold); bottom: -50px; left: -100px; }

  /* CARD */
  .login-card {
    position: relative;
    z-index: 10;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    width: 100%;
    max-width: 520px; 
    border-radius: 32px;
    border: 1px solid rgba(255, 255, 255, 0.6);
    box-shadow: 0 32px 64px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  .card-header { padding: 40px 32px 25px; text-align: center; }
  .cul-logo { width: 90px; height: auto; margin-bottom: 12px; }
  .header-titles h2 { font-size: 15px; color: var(--cul-blue); margin: 0; font-weight: 800; }
  .header-titles p { font-size: 11px; color: #475569; }
  .divider { height: 6px; background: linear-gradient(to right, var(--cul-blue), var(--cul-gold)); }

  .login-content { padding: 40px; }
  .welcome-text h3 { font-size: 24px; color: #0f172a; margin: 0; font-weight: 800; text-align: center; }
  .welcome-text p { font-size: 13px; color: #64748b; text-align: center; margin-top: 5px; }

  /* BOTONES DE ROL */
  .roles-selection { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }
  
  .role-card {
    display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 20px;
    border-radius: 20px; border: 1.5px solid #e2e8f0;
    background: white; cursor: pointer; transition: all 0.3s ease;
  }

  .role-card:hover { transform: translateY(-5px); border-color: var(--cul-blue); box-shadow: 0 10px 20px rgba(11, 31, 63, 0.1); }
  .role-icon { font-size: 24px; transition: transform 0.3s ease; }
  .role-card:hover .role-icon { transform: scale(1.2); }
  .role-title { font-weight: 700; color: #1e293b; font-size: 15px; }

  .separator { display: flex; align-items: center; margin: 30px 0; font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
  .separator::before, .separator::after { content: ''; flex: 1; border-bottom: 1px solid #e2e8f0; }
  .separator span { padding: 0 15px; }

  .input-group { margin-bottom: 20px; }
  .input-group label { display: block; font-size: 14px; font-weight: 700; margin-bottom: 8px; color: #334155; }
  
  .input-wrapper { position: relative; width: 100%; }
  
  input { 
    width: 100%; padding: 14px 18px; border: 1.5px solid #e2e8f0; 
    border-radius: 14px; font-size: 15px; box-sizing: border-box;
    background: white; transition: all 0.2s;
  }
  
  input:focus { outline: none; border-color: var(--cul-blue); box-shadow: 0 0 0 4px rgba(11, 31, 63, 0.08); }

  .password-field input { padding-right: 50px; }

  .toggle-pass {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    font-size: 20px;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: opacity 0.2s;
  }

  .btn-submit { 
    width: 100%; padding: 16px; background: var(--cul-gold); 
    border: none; border-radius: 14px; font-weight: 800; color: var(--cul-blue);
    cursor: pointer; margin-top: 10px; font-size: 16px; transition: 0.3s;
    box-shadow: 0 6px 15px rgba(251, 176, 59, 0.3);
  }
  
  .btn-submit:hover { background: #f9a01b; transform: translateY(-2px); }

  .card-footer { padding: 25px; background: rgba(248, 250, 252, 0.5); text-align: center; font-size: 13px; border-top: 1px solid #f1f5f9; }
</style>