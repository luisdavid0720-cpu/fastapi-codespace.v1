<!-- Dashboard.svelte -->
<script>
  import { currentUser, logout } from '../../stores/auth.js'
  import PqrModule from './PqrModule.svelte'
  import UsuariosModule from './UsuariosModule.svelte'
  import HomeModule from './HomeModule.svelte'

  let { page = $bindable('home') } = $props()
  let loading = $state(false)

  let isAdmin = $derived($currentUser?.id_rol === 3)
  let isCoordinador = $derived($currentUser?.id_rol === 4)
  let isGestor = $derived(isAdmin || isCoordinador)

  const navItems = [
    { id: 'home', label: 'Inicio', icon: 'home', always: true },
    { id: 'pqrs', label: 'PQRS', icon: 'pqrs', always: true },
    { id: 'usuarios', label: 'Usuarios', icon: 'usuarios', admin: true },
    { id: 'analitica', label: 'Analítica', icon: 'analitica', gestor: true }
  ]

  function handleLogout() {
    logout()
  }

  function navigateTo(id) {
    loading = true
    setTimeout(() => {
      page = id
      loading = false
    }, 250)
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
        <span class="brand-text">Sistema PQRS</span>
      </div>

      <nav>
        {#each navItems as item}
          {#if item.always || (item.admin && isAdmin) || (item.gestor && isGestor)}
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
        <div class="avatar">
          {$currentUser?.nombre?.charAt(0)?.toUpperCase() || '?'}
        </div>

        <div class="user-info">
          <p class="user-name">{$currentUser?.nombre || 'Usuario'}</p>
          <p class="user-role">{getRoleLabel()}</p>
        </div>
      </div>

      <button class="btn-logout" onclick={handleLogout}>
        Salir
      </button>
    </div>
  </aside>

  <main class="main">
    {#if loading}
      <div class="loading">
        Cargando...
      </div>

    {:else if page === 'home'}
      <HomeModule />

    {:else if page === 'pqrs'}
      <PqrModule />

    {:else if page === 'usuarios' && isAdmin}
      <UsuariosModule />

    {:else if page === 'analitica' && isGestor}
      <iframe
        title="Power BI"
        src="https://app.powerbi.com/view?r=eyJrIjoiZmFlM2Y3YzEtMDIwNS00OGM2LTk4OGUtMzc2YjgwZWYzNmE0IiwidCI6ImFjYTUxNjMxLTAwZmUtNDkwZC05MWFiLTE2M2VmODcyNjBlZSIsImMiOjR9"
      ></iframe>

    {:else}
      <div class="loading">
        Sin acceso
      </div>
    {/if}
  </main>
</div>

<style>
.layout{
display:flex;
height:100vh;
overflow:hidden;
font-family:Inter,sans-serif;
}

.sidebar{
width:240px;
background:#111827;
color:white;
display:flex;
flex-direction:column;
justify-content:space-between;
padding:20px;
}

.brand{
font-size:22px;
font-weight:800;
margin-bottom:20px;
}

nav{
display:flex;
flex-direction:column;
gap:8px;
}

.nav-item{
background:transparent;
border:none;
color:#cbd5e1;
padding:12px;
border-radius:10px;
cursor:pointer;
text-align:left;
font-weight:600;
}

.nav-item:hover{
background:#1e293b;
color:white;
}

.nav-item.active{
background:#2563eb;
color:white;
}

.sidebar-bottom{
display:flex;
flex-direction:column;
gap:12px;
}

.user-card{
display:flex;
gap:10px;
align-items:center;
background:#1e293b;
padding:12px;
border-radius:12px;
}

.avatar{
width:38px;
height:38px;
border-radius:50%;
background:#2563eb;
display:flex;
align-items:center;
justify-content:center;
font-weight:800;
}

.user-name,.user-role{
margin:0;
font-size:13px;
}

.btn-logout{
border:none;
padding:12px;
border-radius:10px;
cursor:pointer;
font-weight:700;
}

.main{
flex:1;
background:#f8fafc;
overflow:auto;
}

.loading{
padding:40px;
font-size:18px;
font-weight:700;
}

iframe{
width:100%;
height:100%;
border:none;
}
</style>