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

      // Lógica de privacidad: Si no es admin, filtramos solo sus PQRs
      if (!isAdmin) {
        allPqrs = allPqrs.filter(p => p.id_usuario === $currentUser?.id_usuario)
      }

      stats.pqrs = allPqrs.length
      stats.usuarios = usuarios.length
      stats.pendientes = allPqrs.filter(p => p.id_estado === 1).length
      
      // Tomamos las 5 más recientes del set ya filtrado
      recentPqrs = allPqrs.slice(0, 5)
      
    } catch(e) {
      console.error("Error al cargar datos:", e)
    }
    loading = false
  })
</script>

<div class="home">
  <header class="page-header">
    <div>
      <p class="greeting">{greeting},</p>
      <h1 class="user-name">
        {$currentUser?.nombre || 'Usuario'}
      </h1>
      <span class="role-badge">{isAdmin ? 'Panel de Administración' : 'Portal de Estudiante'}</span>
    </div>
    <div class="date-badge">
      {new Date().toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'long' })}
    </div>
  </header>

  <div class="stats-grid">
    <div class="stat-card accent">
      <div class="stat-icon-label">Mis PQRs</div>
      <div class="stat-num">{loading ? '...' : stats.pqrs}</div>
      <div class="stat-label">{isAdmin ? 'Total en sistema' : 'Tus solicitudes totales'}</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon-label">En espera</div>
      <div class="stat-num">{loading ? '...' : stats.pendientes}</div>
      <div class="stat-label">Pendientes por revisar</div>
    </div>
    {#if isAdmin}
    <div class="stat-card">
      <div class="stat-icon-label">Usuarios</div>
      <div class="stat-num">{loading ? '...' : stats.usuarios}</div>
      <div class="stat-label">Registrados en plataforma</div>
    </div>
    {/if}
  </div>

  <div class="section">
    <h2 class="section-title">Acciones recomendadas</h2>
    <div class="actions-grid">
      <button class="action-card main-action" onclick={() => onnavigate('pqrs')}>
        <span class="action-icon">＋</span>
        <div class="action-content">
          <span class="action-label">Nueva PQR</span>
          <span class="action-desc">Registrar una nueva petición, queja o reclamo</span>
        </div>
      </button>

      <button class="action-card" onclick={() => onnavigate('pqrs')}>
        <span class="action-icon">📂</span>
        <div class="action-content">
          <span class="action-label">{isAdmin ? 'Gestionar PQRs' : 'Mis Trámites'}</span>
          <span class="action-desc">Consultar el historial y estado de solicitudes</span>
        </div>
      </button>

      {#if isAdmin}
      <button class="action-card admin-card" onclick={() => onnavigate('usuarios')}>
        <span class="action-icon">👥</span>
        <div class="action-content">
          <span class="action-label">Usuarios</span>
          <span class="action-desc">Administrar accesos y roles del sistema</span>
        </div>
      </button>
      {/if}
    </div>
  </div>

  {#if recentPqrs.length > 0}
  <div class="section">
    <h2 class="section-title">{isAdmin ? 'Actividad reciente del sistema' : 'Mis solicitudes recientes'}</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Descripción</th>
            <th>Fecha</th>
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
                {['','Pendiente','En proceso','Resuelto','Cerrado'][pqr.id_estado] || '—'}
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
  .home { padding: 32px; width: 100%; box-sizing: border-box; }
  
  /* Header */
  .page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 40px; }
  .greeting { font-size: 14px; color: #94a3b8; font-weight: 500; }
  .user-name { font-size: 32px; font-weight: 800; color: #0f172a; margin: 4px 0; letter-spacing: -0.02em; }
  .role-badge { display: inline-block; padding: 4px 12px; background: #f1f5f9; color: #475569; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
  .date-badge { background: #fff; border: 1px solid #e2e8f0; border-radius: 100px; padding: 8px 16px; font-size: 13px; color: #64748b; }

  /* Stats */
  .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 48px; }
  .stat-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
  .stat-icon-label { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 12px; }
  .stat-num { font-size: 36px; font-weight: 800; color: #0f172a; }
  .stat-label { font-size: 12px; color: #64748b; margin-top: 4px; }

  /* Actions Grid (RESTAURADO) */
  .section-title { font-size: 13px; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 20px; letter-spacing: 0.05em; }
  .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
  
  .action-card { 
    background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; 
    display: flex; align-items: center; gap: 20px; cursor: pointer; transition: all 0.3s ease; text-align: left;
  }
  .action-card:hover { transform: translateY(-4px); border-color: #2563eb; box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1); }
  
  .action-icon { 
    width: 48px; height: 48px; background: #eff6ff; color: #2563eb; 
    border-radius: 12px; display: flex; align-items: center; justify-content: center; 
    font-size: 20px; font-weight: 800; flex-shrink: 0;
  }
  
  .action-content { display: flex; flex-direction: column; gap: 2px; }
  .action-label { font-size: 16px; font-weight: 700; color: #1e293b; }
  .action-desc { font-size: 13px; color: #64748b; line-height: 1.4; }
  .main-action { border-left: 5px solid #2563eb; }

  /* Table */
  .table-wrap { background: #fff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f8fafc; padding: 12px 16px; text-align: left; color: #64748b; font-size: 11px; font-weight: 700; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px; border-bottom: 1px solid #f1f5f9; }
  .badge { background: #f1f5f9; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; color: #475569; }
  .status-badge { padding: 4px 12px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; }
  .s2 { background: #e0f2fe; color: #075985; }
  .s3 { background: #dcfce7; color: #166534; }
  .s4 { background: #f1f5f9; color: #475569; }

  @media (max-width: 768px) { .actions-grid { grid-template-columns: 1fr; } .page-header { flex-direction: column; } }
</style>