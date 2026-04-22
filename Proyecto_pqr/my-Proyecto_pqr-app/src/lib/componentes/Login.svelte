<script>
  import { currentUser } from '../../stores/auth.js'

  let username = $state('')
  let password = $state('')
  let showPassword = $state(false)
  let errorMsg = $state('')

  // ROLES REALES DE TU BD
  // 1 = Usuario (Estudiante)
  // 3 = Administrador
  // 4 = Coordinador

  function loginAs(tipo) {
    errorMsg = ''

    // ADMINISTRADOR
    if (tipo === 'admin') {
      currentUser.set({
        id_usuario: 1,
        nombre: 'Administrador General',
        correo: 'admin@cul.edu.co',
        id_rol: 3
      })
      return
    }

    // COORDINADOR
    if (tipo === 'coordinador') {
      currentUser.set({
        id_usuario: 2,
        nombre: 'Coordinador Académico',
        correo: 'coordinador@cul.edu.co',
        id_rol: 4
      })
      return
    }

    // USUARIO
    currentUser.set({
      id_usuario: 3,
      nombre: 'Luis Estudiante',
      correo: 'estudiante@cul.edu.co',
      id_rol: 1
    })
  }

  // LOGIN MANUAL DEMO
  function handleLogin() {
    errorMsg = ''

    const user = username.trim().toLowerCase()
    const pass = password.trim()

    if (!user || !pass) {
      errorMsg = 'Completa usuario y contraseña'
      return
    }

    // DEMO ADMIN
    if (user === 'admin' && pass === '1234') {
      loginAs('admin')
      return
    }

    // DEMO COORDINADOR
    if (user === 'coord' && pass === '1234') {
      loginAs('coordinador')
      return
    }

    // DEMO USUARIO
    if (user === 'user' && pass === '1234') {
      loginAs('usuario')
      return
    }

    errorMsg = 'Credenciales inválidas'
  }
</script>

<div class="login-page">
  <div class="bg-blob blob-1"></div>
  <div class="bg-blob blob-2"></div>

  <div class="login-card">
    <header class="card-header">
      <img src="/logo_cul.png" alt="CUL" class="cul-logo" />

      <h2>Corporación Universitaria Latinoamericana</h2>
      <p>Sistema de Gestión PQRS</p>
    </header>

    <div class="divider"></div>

    <main class="login-content">
      <div class="welcome-text">
        <h3>Portal de Acceso</h3>
        <p>Selecciona un perfil o usa credenciales demo</p>
      </div>

      <!-- BOTONES RÁPIDOS -->
      <div class="roles-selection">
        <button class="role-card admin" onclick={() => loginAs('admin')}>
          <span class="role-icon">⭐</span>
          <span class="role-title">Administrador</span>
        </button>

        <button class="role-card coord" onclick={() => loginAs('coordinador')}>
          <span class="role-icon">🧩</span>
          <span class="role-title">Coordinador</span>
        </button>

        <button class="role-card user" onclick={() => loginAs('usuario')}>
          <span class="role-icon">👤</span>
          <span class="role-title">Usuario</span>
        </button>
      </div>

      <div class="separator">
        <span>Ingreso Manual</span>
      </div>

      <!-- FORM LOGIN -->
      <div class="manual-form">
        <div class="input-group">
          <label>Usuario</label>
          <input
            type="text"
            bind:value={username}
            placeholder="admin / coord / user"
          />
        </div>

        <div class="input-group">
          <label>Contraseña</label>

          <div class="password-wrap">
            <input
              type={showPassword ? 'text' : 'password'}
              bind:value={password}
              placeholder="1234"
            />

            <button
              type="button"
              class="eye-btn"
              onclick={() => showPassword = !showPassword}
            >
              {showPassword ? '🙈' : '👁️'}
            </button>
          </div>
        </div>

        {#if errorMsg}
          <div class="error-box">{errorMsg}</div>
        {/if}

        <button class="btn-submit" onclick={handleLogin}>
          Ingresar al Sistema
        </button>
      </div>

      <div class="demo-box">
        <b>Usuarios Demo:</b><br>
        admin / 1234<br>
        coord / 1234<br>
        user / 1234
      </div>
    </main>
  </div>
</div>

<style>
  :root {
    --blue: #0b1f3f;
    --gold: #fbb03b;
  }

  .login-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 24px;
    background: linear-gradient(135deg,#e2e8f0,#cbd5e1);
    font-family: Inter, sans-serif;
    position: relative;
    overflow: hidden;
  }

  .bg-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(90px);
    opacity: .25;
  }

  .blob-1 {
    width: 350px;
    height: 350px;
    background: var(--blue);
    top: -100px;
    right: -100px;
  }

  .blob-2 {
    width: 320px;
    height: 320px;
    background: var(--gold);
    bottom: -80px;
    left: -80px;
  }

  .login-card {
    width: 100%;
    max-width: 560px;
    background: rgba(255,255,255,.92);
    backdrop-filter: blur(14px);
    border-radius: 28px;
    box-shadow: 0 30px 60px rgba(0,0,0,.12);
    overflow: hidden;
    position: relative;
    z-index: 5;
  }

  .card-header {
    padding: 34px 30px 24px;
    text-align: center;
  }

  .cul-logo {
    width: 80px;
    margin-bottom: 12px;
  }

  h2 {
    margin: 0;
    font-size: 16px;
    color: var(--blue);
    font-weight: 800;
  }

  .card-header p {
    margin: 6px 0 0;
    font-size: 12px;
    color: #64748b;
  }

  .divider {
    height: 5px;
    background: linear-gradient(to right,var(--blue),var(--gold));
  }

  .login-content {
    padding: 32px;
  }

  .welcome-text {
    text-align: center;
    margin-bottom: 24px;
  }

  .welcome-text h3 {
    margin: 0;
    font-size: 24px;
    color: #111827;
  }

  .welcome-text p {
    margin-top: 5px;
    color: #64748b;
    font-size: 13px;
  }

  .roles-selection {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 14px;
    margin-bottom: 28px;
  }

  .role-card {
    border: 1px solid #e2e8f0;
    background: white;
    border-radius: 18px;
    padding: 18px 10px;
    cursor: pointer;
    transition: .25s;
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
  }

  .role-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,.08);
  }

  .role-icon {
    font-size: 22px;
  }

  .role-title {
    font-size: 14px;
    font-weight: 700;
  }

  .separator {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 24px 0;
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 700;
  }

  .separator::before,
  .separator::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #e2e8f0;
  }

  .input-group {
    margin-bottom: 18px;
  }

  label {
    display: block;
    margin-bottom: 7px;
    font-size: 13px;
    font-weight: 700;
    color: #334155;
  }

  input {
    width: 100%;
    box-sizing: border-box;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #dbe2ea;
    font-size: 14px;
  }

  input:focus {
    outline: none;
    border-color: #2563eb;
  }

  .password-wrap {
    position: relative;
  }

  .password-wrap input {
    padding-right: 50px;
  }

  .eye-btn {
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
    border: none;
    background: none;
    cursor: pointer;
    font-size: 18px;
  }

  .btn-submit {
    width: 100%;
    border: none;
    padding: 16px;
    border-radius: 14px;
    background: var(--gold);
    color: var(--blue);
    font-weight: 800;
    font-size: 15px;
    cursor: pointer;
    margin-top: 8px;
  }

  .btn-submit:hover {
    background: #f5a21c;
  }

  .error-box {
    background: #fef2f2;
    color: #b91c1c;
    padding: 12px;
    border-radius: 12px;
    font-size: 13px;
    margin-bottom: 12px;
  }

  .demo-box {
    margin-top: 18px;
    background: #f8fafc;
    border-radius: 14px;
    padding: 14px;
    font-size: 12px;
    color: #475569;
    line-height: 1.7;
  }

  @media (max-width: 640px) {
    .roles-selection {
      grid-template-columns: 1fr;
    }

    .login-content {
      padding: 22px;
    }
  }
</style>