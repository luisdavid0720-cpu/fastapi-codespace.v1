<script>
  import { currentUser, logout } from '../../stores/auth.js'
  import PqrModule      from './PqrModule.svelte'
  import UsuariosModule from './UsuariosModule.svelte'
  import HomeModule     from './HomeModule.svelte'

  let { page = $bindable('home') } = $props()
  let loading = $state(false)

  let isAdmin = $derived($currentUser?.id_rol === 1)

  const navItems = [
    { id: 'home',      label: 'Inicio',    icon: 'home',     always: true },
    { id: 'pqrs',      label: 'PQRS',      icon: 'pqrs',     always: true },
    { id: 'usuarios',  label: 'Usuarios',  icon: 'usuarios', admin: true  },
    { id: 'analitica', label: 'Analítica', icon: 'analitica',admin: true  },
  ]

  function handleLogout() { logout() }

  function navigateTo(id) {
    loading = true
    setTimeout(() => { page = id; loading = false }, 300)
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
              <h3>Panel de Analítica</h3>
              <p>Visualización de datos en tiempo real</p>
            </div>

            <div class="live-status">
              <span class="pulse-dot"></span>
              ADMIN
            </div>
          </div>

          <!-- 🔥 CONTENEDOR CORRECTO -->
          <div class="iframe-container">
            <iframe
              title="gestion pqrs"
              src="https://app.powerbi.com/view?r=eyJrIjoiZmFlM2Y3YzEtMDIwNS00OGM2LTk4OGUtMzc2YjgwZWYzNmE0IiwidCI6ImFjYTUxNjMxLTAwZmUtNDkwZC05MWFiLTE2M2VmODcyNjBlZSIsImMiOjR9"
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

nav { display: flex; flex-direction: column; gap: 4px; }

.nav-item {
  display: flex; align-items: center; gap: 10px; padding: 12px;
  border-radius: 8px; border: none; background: transparent; color: #ccc;
  font-size: 14px; font-weight: 500; cursor: pointer;
}
.nav-item.active { background: #2563eb; color: #fff; }

.sidebar-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 16px;
}

.user-card { display: flex; gap: 10px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #2563eb; color: white; display: flex; align-items: center; justify-content: center; }

.main { 
  flex: 1; 
  display: flex; 
  flex-direction: column; 
  background: #f4f6f9; 
  min-height: 0; /* 🔥 FIX CLAVE */
}

.scrollable-content { overflow-y: auto; padding: 24px; flex: 1; }

/* 🔥 ANALÍTICA */
.analitica-wrapper { 
  flex: 1; 
  padding: 16px; 
  display: flex;
  flex-direction: column;
}

.powerbi-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 16px;
}

/* 🔥 HEADER */
.section-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
}

/* 🔥 IFRAME */
.iframe-container {
  flex: 1;
  width: 100%;
  height: 100%;
}

iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* LOADING */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  flex: 1;
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

/* MOBILE */
@media (max-width: 768px) {
  .layout { flex-direction: column; }
  .sidebar { width: 100%; }
}
</style>