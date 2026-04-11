<script>
  import { createEventDispatcher } from 'svelte';
 
  const dispatch = createEventDispatcher();
 
  let role = 'admin';
  let email = '';
  let password = '';
  let showPassword = false;
 
  function selectRole(r) {
    role = r;
  }
 
  function handleLogin() {
    dispatch('login', { role, email, password });
  }
 
  function handleForgotPassword() {
    dispatch('forgotPassword');
  }
 
  function handleRegister() {
    dispatch('register');
  }
</script>
 
<div class="wrapper">
  <div class="card">
 
    <!-- Header -->
    <div class="header">
      <div class="brand">
        <img src="/logo-cul.jpg" alt="Logo CUL" class="logo" />
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
 
    <!-- Title -->
    <h1>Iniciar sesión</h1>
    <p class="subtitle">Acceso de administrador al sistema</p>
 
    <!-- Role selector -->
    <div class="roles">
      <button
        class="role-card {role === 'admin' ? 'active' : ''}"
        on:click={() => selectRole('admin')}
        type="button"
      >
        <div class="role-icon admin-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <span class="role-label">Administrador</span>
        <span class="role-desc">Acceso completo</span>
      </button>
 
      <button
        class="role-card {role === 'user' ? 'active' : ''}"
        on:click={() => selectRole('user')}
        type="button"
      >
        <div class="role-icon user-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <span class="role-label">Usuario</span>
        <span class="role-desc">PQRs propias</span>
      </button>
    </div>
 
    <!-- Active role badge -->
    <div class="active-badge {role}">
      {#if role === 'admin'}
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
        Administrador — acceso completo
      {:else}
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        Usuario — PQRs propias
      {/if}
    </div>
 
    <!-- Fields -->
    <div class="field">
      <label for="email">Correo institucional</label>
      <input
        id="email"
        type="email"
        placeholder="usuario@ul.edu.co"
        bind:value={email}
      />
    </div>
 
    <div class="field">
      <label for="password">Contraseña</label>
      <div class="password-wrapper">
        <input
          id="password"
          type={showPassword ? 'text' : 'password'}
          placeholder="••••••••"
          bind:value={password}
        />
        <button
          class="toggle-pwd"
          type="button"
          on:click={() => (showPassword = !showPassword)}
          aria-label="Mostrar/ocultar contraseña"
        >
          {#if showPassword}
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
              <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          {:else}
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          {/if}
        </button>
      </div>
    </div>
 
    <button class="btn-secondary" type="button" on:click={handleForgotPassword}>
      ¿Olvidaste tu contraseña?
    </button>
 
    <button class="btn-primary" type="button" on:click={handleLogin}>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
        <polyline points="10 17 15 12 10 7"/>
        <line x1="15" y1="12" x2="3" y2="12"/>
      </svg>
      Ingresar
    </button>
 
    <p class="register-link">
      ¿No tienes cuenta?
      <button type="button" on:click={handleRegister}>Regístrate →</button>
    </p>
 
  </div>
</div>
 
<style>
  .wrapper {
    min-height: 100vh;
    background: #1a1a1a;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    font-family: 'Segoe UI', system-ui, sans-serif;
  }
 
  .card {
    background: #2a2a2a;
    border-radius: 16px;
    padding: 2rem;
    width: 100%;
    max-width: 420px;
    border: 0.5px solid rgba(255, 255, 255, 0.1);
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
    object-fit: cover;
    flex-shrink: 0;
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
 
  /* Title */
  h1 {
    margin: 0 0 4px;
    font-size: 22px;
    font-weight: 500;
    color: white;
  }
 
  .subtitle {
    margin: 0 0 1.5rem;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
  }
 
  /* Roles */
  .roles {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 1rem;
  }
 
  .role-card {
    background: rgba(255, 255, 255, 0.04);
    border: 0.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 12px;
    cursor: pointer;
    text-align: left;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: border-color 0.15s, background 0.15s;
  }
 
  .role-card.active {
    background: rgba(255, 255, 255, 0.06);
    border: 1.5px solid rgba(255, 255, 255, 0.35);
  }
 
  .role-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
 
  .admin-icon {
    background: rgba(99, 102, 241, 0.2);
    color: #818cf8;
  }
 
  .user-icon {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.5);
  }
 
  .role-label {
    font-size: 13px;
    font-weight: 500;
    color: white;
  }
 
  .role-desc {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.4);
  }
 
  /* Active badge */
  .active-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 20px;
    padding: 5px 12px;
    margin-bottom: 1.25rem;
    font-size: 12px;
    transition: all 0.2s;
  }
 
  .active-badge.admin {
    background: rgba(99, 102, 241, 0.15);
    border: 0.5px solid rgba(99, 102, 241, 0.4);
    color: #a5b4fc;
  }
 
  .active-badge.user {
    background: rgba(56, 189, 248, 0.1);
    border: 0.5px solid rgba(56, 189, 248, 0.4);
    color: #7dd3fc;
  }
 
  /* Fields */
  .field {
    margin-bottom: 1rem;
  }
 
  .field label {
    display: block;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 6px;
  }
 
  .field input {
    width: 100%;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.06);
    border: 0.5px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    padding: 10px 14px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    outline: none;
    transition: border-color 0.15s;
  }
 
  .field input::placeholder {
    color: rgba(255, 255, 255, 0.25);
  }
 
  .field input:focus {
    border-color: rgba(255, 255, 255, 0.35);
  }
 
  .password-wrapper {
    position: relative;
  }
 
  .password-wrapper input {
    padding-right: 48px;
  }
 
  .toggle-pwd {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.08);
    border: 0.5px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    width: 32px;
    height: 28px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.5);
    transition: background 0.15s;
  }
 
  .toggle-pwd:hover {
    background: rgba(255, 255, 255, 0.14);
  }
 
  /* Buttons */
  .btn-secondary {
    width: 100%;
    background: rgba(255, 255, 255, 0.06);
    border: 0.5px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    padding: 10px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    cursor: pointer;
    margin-bottom: 0.75rem;
    transition: background 0.15s;
  }
 
  .btn-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
  }
 
  .btn-primary {
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    border: none;
    border-radius: 8px;
    padding: 12px;
    color: #1a1a1a;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-bottom: 1.25rem;
    transition: background 0.15s, transform 0.1s;
  }
 
  .btn-primary:hover {
    background: white;
  }
 
  .btn-primary:active {
    transform: scale(0.98);
  }
 
  /* Register link */
  .register-link {
    text-align: center;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
    margin: 0;
  }
 
  .register-link button {
    background: none;
    border: none;
    color: #60a5fa;
    font-size: 13px;
    cursor: pointer;
    padding: 0;
    margin-left: 4px;
  }
 
  .register-link button:hover {
    text-decoration: underline;
  }
</style>