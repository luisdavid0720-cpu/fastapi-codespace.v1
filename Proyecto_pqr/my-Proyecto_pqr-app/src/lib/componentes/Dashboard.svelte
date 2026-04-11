<script>
  import { currentUser, logout } from '../../stores/auth.js'
  import PqrModule from './PqrModule.svelte'
  import UsuariosModule from './UsuariosModule.svelte'
  import HomeModule from './HomeModule.svelte'

  let { page = $bindable('home') } = $props()
  let loading = $state(false);
  
  // Lógica de validación de administrador
  let isAdmin = $derived($currentUser?.id_rol === 1)

  const navItems = [
    { id: 'home',     label: 'Inicio',   icon: '⊞', always: true },
    { id: 'pqrs',     label: 'PQRS',     icon: '◈', always: true },
    { id: 'usuarios', label: 'Usuarios', icon: '◉', admin: true  },
  ]

  function handleLogout() {
    logout()
  }
</script>

<div class="layout">
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="brand">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="var(--accent)"/>
            <path d="M8 10h16M8 16h10M8 22h13" stroke="#0a0a0f" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <span class="brand-text">Sistema PQRS</span>
      </div>

      <nav>
        {#each navItems as item}
          {#if item.always || (item.admin && isAdmin)}
            <button
              class="nav-item {page === item.id ? 'active' : ''}"
              onclick={() => {
                loading = true;
                setTimeout(() => {
                  page = item.id;
                  loading = false;
                }, 300);
              }}
            > 
              <span class="nav-icon">{item.icon}</span>
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
          <p class="user-role">{$currentUser?.id_rol === 1 ? 'Administrador' : 'Usuario'}</p>
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
      <HomeModule onnavigate={(p) => page = p} />

      {#if isAdmin}
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
              height="541.25" 
              src="https://app.powerbi.com/view?r=eyJrIjoiZmFlM2Y3YzEtMDIwNS00OGM2LTk4OGUtMzc2YjgwZWYzNmE0IiwidCI6ImFjYTUxNjMxLTAwZmUtNDkwZC05MWFiLTE2M2VmODcyNjBlZSIsImMiOjR9" 
              frameborder="0" 
              allowFullScreen="true">
            </iframe>
          </div>
        </section>
      {/if}

    {:else if page === 'pqrs'}
      <PqrModule />

    {:else if page === 'usuarios' && isAdmin}
      <UsuariosModule />

    {:else}
      <div class="no-access">No tienes acceso a esta sección.</div>
    {/if}
  </main>
</div>

<style>
  .layout {
    display: flex;
    min-height: 100vh;
  }

  .sidebar {
    width: 240px;
    min-width: 240px;
    background: linear-gradient(180deg, #000, #111);
    color: #fff;
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24px 16px;
    position: sticky;
    top: 0;
    height: 100vh;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 8px 28px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
  }

  .brand-text {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 16px;
    letter-spacing: -0.02em;
  }

  nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    border: none;
    background: transparent;
    color: #ccc;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    text-align: left;
    width: 100%;
    cursor: pointer;
  }

  .nav-item:hover {
    background: rgba(255,255,255,0.05);
    color: #fff;
    transform: translateX(3px);
  }

  .nav-item.active {
    background: rgba(255,255,255,0.15);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.2);
  }

  .nav-icon { font-size: 16px; }

  .sidebar-bottom {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .user-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    background: rgba(255,255,255,0.05);
    border-radius: var(--radius-sm);
    border: 1px solid rgba(255,255,255,0.01);
  }

  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #2563eb;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 16px;
    flex-shrink: 0;
  }

  .user-name {
    font-size: 13px;
    font-weight: 600;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .user-role {
    font-size: 11px;
    color: #aaa;
  }

  .btn-logout {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid rgba(255,255,255,0.11);
    background: rgba(255,255,255,0.05);
    color: #ddd;
    font-size: 13px;
    transition: all 0.15s;
    width: 100%;
    cursor: pointer;
  }

  .btn-logout:hover {
    background: rgba(255,71,71,0.2);
    border-color: rgba(255,71,71,0.5);
    color: #ff6b6b;
  }

  .main {
    flex: 1;
    overflow-y: auto;
    background: linear-gradient(180deg, #f4f6f9, #eef1f5);
  }

  .powerbi-section {
    margin: 24px;
    background: white;
    border-radius: 16px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.03);
    overflow: hidden;
  }

  .section-header {
    padding: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f0f0f0;
  }

  .header-info h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 700;
    color: #111;
  }

  .header-info p {
    margin: 4px 0 0;
    font-size: 12px;
    color: #666;
  }

  .live-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 800;
    color: #2563eb;
    background: #eff6ff;
    padding: 6px 12px;
    border-radius: 20px;
  }

  .pulse-dot {
    width: 8px;
    height: 8px;
    background: #2563eb;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.7; }
    50% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.7; }
  }

  .iframe-container {
    width: 100%;
    line-height: 0;
    background: #fdfdfd;
  }

  .loading-container {
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    color: #666;
  }

  .spinner {
    width: 30px;
    height: 30px;
    border: 3px solid #eee;
    border-top: 3px solid #2563eb;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .no-access {
    padding: 40px;
    color: #666;
  }

  @media (max-width: 768px) {
    .layout { flex-direction: column; }
    .sidebar {
      width: 100%;
      height: auto;
      position: static;
      flex-direction: row;
      flex-wrap: wrap;
      padding: 16px;
      gap: 8px;
    }
    .powerbi-section { margin: 12px; }
  }
</style>