<script>
  // Simulación de estados para la visualización
  let username = $state('');
  let password = $state('');
  let showPassword = $state(false);
  let isLoggingIn = $state(false);

  function handleLogin() {
    isLoggingIn = true;
    // Simulación de proceso de entrada
    setTimeout(() => {
      isLoggingIn = false;
      console.log("Credenciales enviadas:", { username, password });
    }, 2000);
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

    <main class="login-form">
      <div class="welcome-text">
        <h3>Iniciar Sesión</h3>
        <p>Ingresa tus credenciales para continuar</p>
      </div>

      <form onsubmit={(e) => { e.preventDefault(); handleLogin(); }}>
        <div class="input-group">
          <label for="user">Usuario</label>
          <div class="input-wrapper">
            <span class="icon">👤</span>
            <input 
              type="text" 
              id="user" 
              bind:value={username} 
              placeholder="Usuario o correo institucional"
              required
            />
          </div>
        </div>

        <div class="input-group">
          <label for="pass">Contraseña</label>
          <div class="input-wrapper">
            <span class="icon">🔒</span>
            <input 
              type={showPassword ? "text" : "password"} 
              id="pass" 
              bind:value={password} 
              placeholder="••••••••"
              required
            />
            <button 
              type="button" 
              class="toggle-pass" 
              onclick={() => showPassword = !showPassword}
            >
              {showPassword ? '👁️' : '🙈'}
            </button>
          </div>
        </div>

        <button type="submit" class="btn-submit" disabled={isLoggingIn}>
          {#if isLoggingIn}
            <span class="loader"></span>
            Verificando...
          {:else}
            Ingresar →
          {/if}
        </button>
      </form>
    </main>

    <footer class="card-footer">
      <a href="#olvido">¿Olvidaste tu contraseña?</a>
      <p>Aviso de Privacidad</p>
    </footer>
  </div>
</div>

<style>
  /* CONFIGURACIÓN DE COLORES INSTITUCIONALES */
  :root {
    --cul-blue: #0b1f3f; /* Azul oscuro del escudo */
    --cul-gold: #fbb03b; /* Amarillo/Naranja del escudo */
    --bg-gray: #f1f5f9;
  }

  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--bg-gray) 0%, #e2e8f0 100%);
    font-family: 'Inter', system-ui, sans-serif;
    padding: 20px;
  }

  .login-card {
    background: white;
    width: 100%;
    max-width: 420px;
    border-radius: 20px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    overflow: hidden;
    animation: slideUp 0.5s ease-out;
  }

  @keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* CABECERA */
  .card-header {
    padding: 30px 20px;
    text-align: center;
    background: #fff;
  }

  .logo-wrapper {
    margin-bottom: 15px;
  }

  .cul-logo {
    width: 100px;
    height: auto;
    object-fit: contain;
  }

  .header-titles h2 {
    font-size: 16px;
    color: var(--cul-blue);
    margin: 0;
    font-weight: 700;
  }

  .header-titles p {
    font-size: 13px;
    color: #64748b;
    margin: 5px 0 0;
    font-weight: 500;
  }

  .divider {
    height: 4px;
    background: linear-gradient(to right, var(--cul-blue), var(--cul-gold));
  }

  /* CUERPO DEL LOGIN */
  .login-form {
    padding: 40px 35px;
  }

  .welcome-text {
    margin-bottom: 30px;
  }

  .welcome-text h3 {
    font-size: 24px;
    color: #0f172a;
    margin: 0;
  }

  .welcome-text p {
    font-size: 14px;
    color: #64748b;
    margin-top: 5px;
  }

  .input-group {
    margin-bottom: 20px;
  }

  .input-group label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #475569;
    margin-bottom: 8px;
  }

  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  .input-wrapper .icon {
    position: absolute;
    left: 12px;
    font-size: 16px;
  }

  .input-wrapper input {
    width: 100%;
    padding: 12px 40px;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 15px;
    transition: all 0.3s;
    outline: none;
  }

  .input-wrapper input:focus {
    border-color: var(--cul-blue);
    box-shadow: 0 0 0 4px rgba(11, 31, 63, 0.1);
  }

  .toggle-pass {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
  }

  /* BOTÓN INGRESAR */
  .btn-submit {
    width: 100%;
    padding: 14px;
    background: var(--cul-gold);
    border: none;
    border-radius: 12px;
    color: var(--cul-blue);
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
    margin-top: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }

  .btn-submit:hover {
    background: #e69d2f;
    transform: translateY(-2px);
  }

  .btn-submit:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
    transform: none;
  }

  /* FOOTER */
  .card-footer {
    padding: 20px;
    text-align: center;
    background: #f8fafc;
    font-size: 13px;
  }

  .card-footer a {
    color: var(--cul-blue);
    text-decoration: none;
    font-weight: 600;
  }

  .card-footer p {
    color: #94a3b8;
    margin-top: 10px;
  }

  /* LOADER */
  .loader {
    width: 18px;
    height: 18px;
    border: 2px solid white;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    animation: rotation 1s linear infinite;
  }

  @keyframes rotation {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>