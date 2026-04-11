<script>
  import { currentUser, logout } from '../../stores/auth.js'
  import PqrModule from './PqrModule.svelte'
  import UsuariosModule from './UsuariosModule.svelte'
  import HomeModule from './HomeModule.svelte'

  let { page = $bindable('home') } = $props()
  let loading = $state(false);
  
  // Seguridad: Determinamos si el usuario es administrador
  let isAdmin = $derived($currentUser?.id_rol === 1)

  const navItems = [
    { id: 'home',      label: 'Inicio',    icon: '⊞', always: true },
    { id: 'pqrs',      label: 'PQRS',      icon: '◈', always: true },
    { id: 'usuarios',  label: 'Usuarios',  icon: '◉', admin: true  },
    { id: 'analitica', label: 'Analítica', icon: '📊', admin: true  },
  ]

  // GUARDIA DE SEGURIDAD: 
  // Si la página cambia a una prohibida para el usuario, lo redirigimos a home.
  $effect(() => {
    if (!isAdmin && (page === 'usuarios' || page === 'analitica')) {
      page = 'home';
    }
  });

  function handleLogout() {
    logout()
  }

  function navigateTo(id) {
    // Bloqueo preventivo en la función de navegación
    if (!isAdmin && (id === 'usuarios' || id === 'analitica')) return;

    loading = true;
    setTimeout(() => {
      page = id;
      loading = false;
    }, 300);
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
          <p class="user-role">{isAdmin ? 'Administrador' : 'Usuario'}</p>
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
      <div class="no-access">
        <div class="error-msg">
           <span>⚠️</span>
           <p>No tienes permisos para acceder a esta sección.</p>
           <button class="btn-secondary" onclick={() => page = 'home'}>Ir al Inicio</button>
        </div>
      </div>
    {/if}
  </main>
</div>

<style>
  /* Estilos base del Layout */
  .layout { display: flex; height: 100vh; overflow: hidden; }

  /* Sidebar con diseño Dark Industrial */
  .sidebar {
    width: 240px;
    min-width: 240px;
    background: linear-gradient(180deg, #0b1f3f 0%, #050d1a 100%);
    color: #fff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24px 16px;
    height: 100vh;
    border-right: 1px solid rgba(255,255,255,0.05);
  }

  .brand { display: flex; align-items: center; gap: 10px; padding: 0 8px 28px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
  .brand-text { font-weight: 700; font-size: 16px; letter-spacing: -0.02em; }
  
  nav { display: flex; flex-direction: column; gap: 4px; }

  .nav-item {
    display: flex; align-items: center; gap: 10px; padding: 12px;
    border-radius: 10px; border: none; background: transparent; color: #94a3b8;
    font-size: 14px; font-weight: 500; transition: all 0.2s ease;
    text-align: left; width: 100%; cursor: pointer;
  }

  .nav-item:hover { background: rgba(255,255,255,0.05); color: #fff; }
  .nav-item.active { background: #2563eb; color: #fff; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }

  .sidebar-bottom { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 16px; display: flex; flex-direction: column; gap: 12px; }
  .user-card { display: flex; align-items: center; gap: 10px; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 10px; }
  .avatar { width: 36px; height: 36px; border-radius: 50%; background: #fbb03b; color: #0b1f3f; display: flex; align-items: center; justify-content: center; font-weight: 800; }
  .user-name { font-size: 13px; font-weight: 600; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .user-role { font-size: 11px; color: #94a3b8; }

  .btn-logout {
    display: flex; align-items: center; gap: 8px; padding: 10px 12px;
    border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.03); color: #cbd5e1; cursor: pointer; font-size: 13px;
  }
  .btn-logout:hover { background: rgba(239, 68, 68, 0.1); color: #f87171; border-color: rgba(239, 68, 68, 0.2); }

  /* Main Container */
  .main { flex: 1; background: #f1f5f9; display: flex; flex-direction: column; height: 100vh; }
  .full-width-module { width: 100%; box-sizing: border-box; display: flex; flex-direction: column; }
  .scrollable-content { overflow-y: auto; padding: 32px; flex: 1; }

  /* Power BI Wrapper */
  .analitica-wrapper { flex: 1; padding: 24px; height: 100%; }
  .powerbi-section { background: white; border-radius: 20px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; flex: 1; overflow: hidden; }
  .section-header { padding: 20px 24px; display: flex; justify-content: space-between; align-items: center; background: #fff; border-bottom: 1px solid #f1f5f9; }
  .header-info h3 { margin: 0; font-size: 18px; font-weight: 800; color: #0f172a; }
  .iframe-container { flex: 1; width: 100%; background: #f8fafc; }

  /* Utils */
  .loading-container { padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; gap: 15px; }
  .spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top: 3px solid #2563eb; border-radius: 50%; animation: spin 1s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .no-access { padding: 60px; display: flex; justify-content: center; }
  .error-msg { text-align: center; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
  .error-msg span { font-size: 40px; display: block; margin-bottom: 10px; }

  @media (max-width: 768px) {
    .sidebar { width: 70px; min-width: 70px; padding: 20px 10px; }
    .brand-text, .user-info, .nav-item span:not(.nav-icon) { display: none; }
    .nav-item { justify-content: center; padding: 12px 0; }
  }
</style>