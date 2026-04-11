<script>
  import { onMount } from 'svelte';
  
  // Variables de estado
  let username = $state('');
  let password = $state('');
  let showPassword = $state(false);
  let isLoggingIn = $state(false);

  // Función para simular el ingreso manual por rol
  function fastAccess(role) {
    isLoggingIn = true;
    console.log("Acceso rápido como:", role);
    
    // Aquí simulas la redirección
    setTimeout(() => {
      isLoggingIn = false;
      alert(`Accediendo como ${role}... (Aquí iría la redirección al Dashboard)`);
    }, 1000);
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
        <p>Selecciona un rol para acceso rápido o ingresa tus datos</p>
      </div>

      <div class="role-selector">
        <button class="role-btn admin" onclick={() => fastAccess('Administrador')}>
          <span class="role-icon">⭐</span>
          <div class="role-info">
            <span class="role-name">Administrador</span>
            <span class="role-desc">Gestión y Analítica</span>
          </div>
        </button>

        <button class="role-btn user" onclick={() => fastAccess('Usuario')}>
          <span class="role-icon">👤</span>
          <div class="role-info">
            <span class="role-name">Usuario</span>
            <span class="role-desc">Mis solicitudes</span>
          </div>
        </button>
      </div>

      <div class="separator">
        <span>O ingresa con credenciales</span>
      </div>

      <form onsubmit={(e) => { e.preventDefault(); fastAccess('Login Manual'); }}>
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

        <button type="submit" class="btn-submit" disabled={isLoggingIn}>
          {#if isLoggingIn}
            <span class="loader"></span>
          {:else}
            Ingresar →
          {/if}
        </button>
      </form>
    </main>

    <footer class="card-footer">
      <p>¿Problemas para acceder? <b>Soporte Técnico</b></p>
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
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f1f5f9;
    font-family: 'Inter', sans-serif;
    padding: 20px;
  }

  .login-card {
    background: white;
    width: 100%;
    max-width: 440px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  .card-header { padding: 25px; text-align: center; }
  .cul-logo { width: 80px; height: auto; }
  .header-titles h2 { font-size: 14px; color: var(--cul-blue); margin: 10px 0 0; }
  .header-titles p { font-size: 12px; color: #64748b; margin: 2px 0 0; }
  
  .divider { height: 4px; background: linear-gradient(to right, var(--cul-blue), var(--cul-gold)); }

  .login-content { padding: 30px; }
  
  .welcome-text { margin-bottom: 20px; text-align: center; }
  .welcome-text h3 { font-size: 20px; margin: 0; color: #1e293b; }
  .welcome-text p { font-size: 13px; color: #64748b; }

  /* ESTILO DE LOS BOTONES DE ROL */
  .role-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 25px; }
  
  .role-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    cursor: pointer;
    transition: all 0.2s;
  }

  .role-btn:hover { border-color: var(--cul-blue); background: #eff6ff; transform: translateY(-2px); }
  
  .role-icon { font-size: 20px; margin-bottom: 8px; }
  .role-name { display: block; font-size: 13px; font-weight: 700; color: #1e293b; }
  .role-desc { display: block; font-size: 10px; color: #64748b; }

  .separator { 
    display: flex; align-items: center; text-align: center; 
    margin: 20px 0; font-size: 11px; color: #94a3b8; text-transform: uppercase;
  }
  .separator::before, .separator::after { content: ''; flex: 1; border-bottom: 1px solid #e2e8f0; }
  .separator span { padding: 0 10px; }

  /* FORMULARIO */
  .input-group { margin-bottom: 15px; }
  .input-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 5px; color: #475569; }
  .input-wrapper { position: relative; }
  .input-wrapper input { 
    width: 100%; padding: 10px 15px; border: 1px solid #cbd5e1; 
    border-radius: 10px; outline: none; box-sizing: border-box;
  }
  
  .toggle-pass { position: absolute; right: 10px; top: 8px; border: none; background: none; cursor: pointer; }

  .btn-submit { 
    width: 100%; padding: 12px; background: var(--cul-gold); 
    border: none; border-radius: 10px; font-weight: 700; color: var(--cul-blue);
    cursor: pointer; margin-top: 10px;
  }

  .btn-submit:hover { background: #e69d2f; }

  .card-footer { padding: 15px; background: #f8fafc; text-align: center; font-size: 12px; color: #64748b; }
  
  .loader { 
    width: 16px; height: 16px; border: 2px solid var(--cul-blue); 
    border-bottom-color: transparent; border-radius: 50%; display: inline-block; 
    animation: rotation 1s linear infinite; 
  }
  @keyframes rotation { to { transform: rotate(360deg); } }
</style>