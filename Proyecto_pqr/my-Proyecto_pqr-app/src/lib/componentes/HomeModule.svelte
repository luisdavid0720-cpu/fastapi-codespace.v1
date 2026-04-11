<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  let { onnavigate } = $props()

  let stats = $state({ pqrs: 0, usuarios: 0, pendientes: 0 })
  let recentPqrs = $state([])
  let loading = $state(true)

  let isAdmin = $derived($currentUser?.id_rol === 1)
  let greeting = $derived(getGreeting())

  function getGreeting() {
    const h = new Date().getHours()
    if (h < 12) return 'Buenos días'
    if (h < 18) return 'Buenas tardes'
    return 'Buenas noches'
  }

  onMount(async () => {
    try {
      const [pqrData, usrData] = await Promise.allSettled([api.getPqrs(), api.getUsuarios()])
      
      let allPqrs = pqrData.value?.resultado || []
      const usuarios = usrData.value?.resultado || []

      // LÓGICA DE FILTRADO PARA USUARIO
      if (!isAdmin) {
        // Solo PQRs que pertenecen al usuario logueado
        allPqrs = allPqrs.filter(p => p.id_usuario === $currentUser?.id_usuario)
      }

      // Actualizamos las estadísticas según el filtro anterior
      stats.pqrs = allPqrs.length
      stats.usuarios = usuarios.length // Este solo se muestra si es Admin
      stats.pendientes = allPqrs.filter(p => p.id_estado === 1).length
      
      // Tomamos las 5 más recientes del set filtrado
      recentPqrs = allPqrs.slice(0, 5)
      
    } catch(e) {
      console.error("Error cargando dashboard:", e)
    }
    loading = false
  })
</script>

<div class="home">
  <header class="page-header">
    <div>
      <p class="greeting">{greeting},</p>
      <h1 style="font-weight: 700;">
        {$currentUser?.nombre || 'Usuario'}
      </h1>
      <span class="role-indicator">{isAdmin ? 'Panel Administrativo' : 'Portal de Estudiante'}</span>
    </div>
    <div class="date-badge">
      {new Date().toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'long' })}
    </div>
  </header>

  <div class="stats-grid">
    <div class="stat-card accent">
      <div class="stat-icon">Mis PQRs</div>
      <div class="stat-num">{loading ? '...' : stats.pqrs}</div>
      <div class="stat-label">{isAdmin ? 'Total en el sistema' : 'Tus solicitudes totales'}</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">En espera</div>
      <div class="stat-num">{loading ? '...' : stats.pendientes}</div>
      <div class="stat-label">Pendientes por revisar</div>
    </div>
    
    {#if isAdmin}
    <div class="stat-card">
      <div class="stat-icon">Comunidad</div>
      <div class="stat-num">{loading ? '...' : stats.usuarios}</div>
      <div class="stat-label">Usuarios registrados</div>
    </div>
    {/if}
  </div>

  <div class="section">
    <h2 class="section-title">Acciones recomendadas</h2>
    <div class="actions-grid">
      <button class="action-card main-action" onclick={() => onnavigate('pqrs')}>
        <span class="action-icon">＋</span>
        <span class="action-label">Nueva PQR</span>
        <span class="action-desc">Radicar una nueva solicitud al sistema</span>
      </button>

      <button class="action-card" onclick={() => onnavigate('pqrs')}>
        <span class="action-icon">📂</span>
        <span class="action-label">{isAdmin ? 'Gestionar PQRs' : 'Mis Trámites'}</span>
        <span class="action-desc">{isAdmin ? 'Ver todas las solicitudes' : 'Ver el estado de mis PQRs'}</span>
      </button>

      {#if isAdmin}
      <button class="action-card admin-only" onclick={() => onnavigate('usuarios')}>
        <span class="action-icon">👥</span>
        <span class="action-label">Base de Usuarios</span>
        <span class="action-desc">Administrar accesos y roles</span>
      </button>
      {/if}
    </div>
  </div>

  {#if recentPqrs.length > 0}
  <div class="section">
    <h2 class="section-title">{isAdmin ? 'Últimas PQRs del sistema' : 'Mis solicitudes recientes'}</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Descripción</th>
            <th>Fecha Radicado</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {#each recentPqrs as pqr}
          <tr>
            <td><span class="badge">#{pqr.id_pqr}</span></td>
            <td class="desc-cell">{pqr.descripcion?.slice(0,70)}{pqr.descripcion?.length > 70 ? '...' : ''}</td>
            <td>{pqr.fecha ? new Date(pqr.fecha).toLocaleDateString('es-CO') : '-'}</td>
            <td>
              <span class="status-badge s{pqr.id_estado}">
                {['','Pendiente','En proceso','Resuelto','Cerrado'][pqr.id_estado] || 'Desconocido'}
              </span>
            </td>
          </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
  {/if}
</div>

<style>
  /* Mantenemos tus estilos con un par de retoques para que se vea más profesional */
  .home { padding: 32px; width: 100%; box-sizing: border-box; }
  .page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 40px; }
  
  .role-indicator { 
    display: inline-block; 
    margin-top: 8px; 
    padding: 4px 12px; 
    background: #e5e7eb; 
    color: #374151; 
    border-radius: 6px; 
    font-size: 11px; 
    font-weight: 700; 
    text-transform: uppercase; 
  }

  .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 48px; }
  .stat-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
  .stat-num { font-size: 36px; font-weight: 800; color: #0f172a; margin: 8px 0; }
  
  .main-action { border-left: 4px solid #2563eb !important; }
  .admin-only { background: #f8fafc !important; }

  /* El resto de tus estilos se mantienen iguales... */
  .table-wrap { border-radius: 16px; border: 1px solid #e2e8f0; }
  th { background: #f8fafc; color: #64748b; font-size: 11px; }
  .status-badge { font-size: 10px; padding: 5px 12px; font-weight: 800; }
</style>