<script>
import { currentUser, logout } from '../../stores/auth.js'
  import PqrModule      from './PqrModule.svelte'
  import UsuariosModule from './UsuariosModule.svelte'
  import HomeModule     from './HomeModule.svelte'

  let { page = $bindable('home') } = $props()
  let loading = $state(false)

  let isAdmin = $derived($currentUser?.id_rol === 3)
  let isCoordinador = $derived($currentUser?.id_rol === 4)

  const navItems = [
    { id: 'home',      label: 'Inicio',       icon: 'home',     always: true },
    { id: 'pqrs',      label: 'PQRS',         icon: 'pqrs',     always: true },
    { id: 'usuarios',  label: 'Usuarios',     icon: 'usuarios', admin: true  },
    { id: 'analitica', label: 'Analítica',    icon: 'analitica',admin: true  },
  ]

  function handleLogout() { logout() }

  function navigateTo(id) {
    loading = true
    setTimeout(() => { page = id; loading = false }, 300)
  }

  function getRoleLabel() {
    if (isAdmin) return 'Administrador'
    if (isCoordinador) return 'Coordinador'
    return 'Usuario'
  }
</script>

<div class="layout">
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="brand">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#2563eb"/>
            <path d="M8 10h16M8 16h10M8 22h13" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <span class="brand-text">Sistema PQRS</span>
      </div>

      <nav>
        {#each navItems as item}
          {#if item.always || (item.admin && isAdmin)}
            <button
              class="nav-item {page === item.id ? 'active' : ''}"
              onclick={() => navigateTo(item.id)}
            >
              <!-- Íconos SVG por item -->
              {#if item.icon === 'home'}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                  <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>
              {:else if item.icon === 'pqrs'}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10 9 9 9 8 9"/>
                </svg>
              {:else if item.icon === 'usuarios'}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              {:else if item.icon === 'analitica'}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6"  y1="20" x2="6"  y2="14"/>
                </svg>
              {/if}
              <span>{item.label}</span>
            </button>
          {/if}
        {/each}
      </nav>
    </div>

    <div class="sidebar-bottom">
      <div class="user-card">
        <div class="avatar">{$currentUser?.nombre?.charAt(0)?.toUpperCase() || '?'}</div>
        <div class="user-info">
          <p class="user-name">{$currentUser?.nombre || 'Usuario'}</p>
          <p class="user-role">{getRoleLabel()}</p>
        </div>
      </div>
      <button class="btn-logout" onclick={handleLogout}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
        </svg>
        Salir
      </button>
    </div>
  </aside>

  <main class="main">
    {#if loading}
      <div class="loading-container">
        <div class="spinner"></div>
        <p>Cargando módulo...</p>
      </div>

    {:else if page === 'home'}
      <div class="full-width-module scrollable-content">
        <HomeModule onnavigate={(p) => navigateTo(p)} />
      </div>

    {:else if page === 'pqrs'}
      <div class="full-width-module scrollable-content">
        <PqrModule />
      </div>

    {:else if page === 'usuarios' && isAdmin}
      <div class="full-width-module scrollable-content">
        <UsuariosModule />
      </div>

    {:else if page === 'analitica' && isAdmin}
      <div class="full-width-module analitica-wrapper">
        <section class="powerbi-section">
          <div class="section-header">
            <div class="header-info">
              <h3>Panel de Analítica Avanzada</h3>
              <p>Visualización de datos en tiempo real desde Power BI</p>
            </div>
            <div class="live-status">
              <span class="pulse-dot"></span>
              MODO ADMIN
            </div>
          </div>
          <div class="iframe-container">
            <iframe
              title="gestion pqrs"
              width="100%"
              height="100%"
              src="https://app.powerbi.com/view?r=eyJrIjoiZmFlM2Y3YzEtMDIwNS00OGM2LTk4OGUtMzc2YjgwZWYzNmE0IiwidCI6ImFjYTUxNjMxLTAwZmUtNDkwZC05MWFiLTE2M2VmODcyNjBlZSIsImMiOjR9"
              frameborder="0"
              allowFullScreen="true">
            </iframe>
          </div>
        </section>
      </div>

    {:else}
      <div class="no-access">No tienes acceso a esta sección.</div>
    {/if}
  </main>
</div>

<style>
  .layout { display: flex; height: 100vh; overflow: hidden; }

  .sidebar {
    width: 240px; min-width: 240px;
    background: linear-gradient(180deg, #000, #111);
    color: #fff; display: flex; flex-direction: column;
    justify-content: space-between; padding: 24px 16px; height: 100vh;
  }

  .brand {
    display: flex; align-items: center; gap: 10px;
    padding: 0 8px 28px; border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
  }
  .brand-text { font-weight: 700; font-size: 16px; letter-spacing: -0.02em; }

  nav { display: flex; flex-direction: column; gap: 4px; }

  .nav-item {
    display: flex; align-items: center; gap: 10px; padding: 12px;
    border-radius: 8px; border: none; background: transparent; color: #ccc;
    font-size: 14px; font-weight: 500; transition: all 0.2s ease;
    text-align: left; width: 100%; cursor: pointer;
  }
  .nav-item:hover  { background: rgba(255,255,255,0.05); color: #fff; }
  .nav-item.active { background: #2563eb; color: #fff; }

  .sidebar-bottom {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 16px; display: flex; flex-direction: column; gap: 12px;
  }

  .user-card { display: flex; align-items: center; gap: 10px; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 8px; }
  .avatar { width: 36px; height: 36px; border-radius: 50%; background: #2563eb; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; }
  .user-name { font-size: 13px; font-weight: 600; color: #fff; margin: 0; }
  .user-role { font-size: 11px; color: #aaa; margin: 0; }

  .btn-logout {
    display: flex; align-items: center; gap: 8px; padding: 10px 12px;
    border-radius: 8px; border: 1px solid rgba(255,255,255,0.11);
    background: rgba(255,255,255,0.05); color: #ddd; cursor: pointer;
    font-size: 14px; font-family: inherit; transition: 0.2s;
  }
  .btn-logout:hover { background: rgba(255,255,255,0.1); }

  .main { flex: 1; background: #f4f6f9; display: flex; flex-direction: column; height: 100vh; }

  .full-width-module { width: 100%; box-sizing: border-box; display: flex; flex-direction: column; }
  .scrollable-content { overflow-y: auto; padding: 24px 24px 40px 24px; flex: 1; }
  .analitica-wrapper  { flex: 1; padding: 24px; height: 100%; }

  .powerbi-section {
    background: white; border-radius: 16px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.03);
    display: flex; flex-direction: column; flex: 1;
  }
  .section-header { padding: 20px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; flex-shrink: 0; }
  .header-info h3 { margin: 0; font-size: 18px; font-weight: 700; color: #111; }
  .header-info p  { margin: 4px 0 0; font-size: 12.5px; color: #666; }

  .live-status { display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 800; color: #2563eb; background: #eff6ff; padding: 6px 12px; border-radius: 20px; }
  .pulse-dot { width: 8px; height: 8px; background: #2563eb; border-radius: 50%; animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100% { transform: scale(0.95); opacity: 0.7; } 50% { transform: scale(1.2); opacity: 1; } }

  .iframe-container { flex: 1; width: 100%; display: flex; flex-direction: column; }
  iframe { flex: 1; }

  .loading-container { padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; gap: 15px; }
  .spinner { width: 30px; height: 30px; border: 3px solid #eee; border-top: 3px solid #2563eb; border-radius: 50%; animation: spin 1s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .no-access { padding: 40px; color: #666; text-align: center; font-weight: 500; }

  @media (max-width: 768px) {
    .layout { flex-direction: column; height: auto; overflow: visible; }
    .sidebar { width: 100%; height: auto; position: static; flex-direction: row; flex-wrap: wrap; padding: 16px; gap: 8px; }
    .main { height: auto; }
    .analitica-wrapper { padding: 12px; height: 80vh; }
    .scrollable-content { padding: 12px; }
  }
</style>