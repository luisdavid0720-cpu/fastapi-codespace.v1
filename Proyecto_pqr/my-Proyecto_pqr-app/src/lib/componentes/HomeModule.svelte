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
    if (h < 12) return 'Buenos dias'
    if (h < 18) return 'Buenas tardes'
    return 'Buenas noches'
  }

  onMount(async () => {
    try {
      const [pqrData, usrData] = await Promise.allSettled([api.getPqrs(), api.getUsuarios()])
      const pqrs = pqrData.value?.resultado || []
      const usuarios = usrData.value?.resultado || []
      stats.pqrs = pqrs.length
      stats.usuarios = usuarios.length
      stats.pendientes = pqrs.filter(p => p.id_estado === 1).length
      recentPqrs = pqrs.slice(0, 5)
    } catch(e) {}
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
    </div>
    <div class="date-badge">
      {new Date().toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'long' })}
    </div>
  </header>

  <div class="stats-grid">
    <div class="stat-card accent">
      <div class="stat-icon">total</div>
      <div class="stat-num">{loading ? '...' : stats.pqrs}</div>
      <div class="stat-label">Total PQRs</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">pendiente</div>
      <div class="stat-num">{loading ? '...' : stats.pendientes}</div>
      <div class="stat-label">Pendientes</div>
    </div>
    {#if isAdmin}
    <div class="stat-card">
      <div class="stat-icon">usuarios</div>
      <div class="stat-num">{loading ? '...' : stats.usuarios}</div>
      <div class="stat-label">Usuarios</div>
    </div>
    {/if}
  </div>

  <div class="section">
    <h2 class="section-title">Acciones rapidas</h2>
    <div class="actions-grid">
      <button class="action-card" onclick={() => onnavigate('pqrs')}>
        <span class="action-icon">+</span>
        <span class="action-label">Nueva PQR</span>
        <span class="action-desc">Registrar peticion, queja o reclamo</span>
      </button>
      <button class="action-card" onclick={() => onnavigate('pqrs')}>
        <span class="action-icon">ver</span>
        <span class="action-label">Ver PQRs</span>
        <span class="action-desc">Consultar y gestionar solicitudes</span>
      </button>
      {#if isAdmin}
      <button class="action-card" onclick={() => onnavigate('usuarios')}>
        <span class="action-icon">usr</span>
        <span class="action-label">Gestionar Usuarios</span>
        <span class="action-desc">CRUD completo de usuarios</span>
      </button>
      {/if}
    </div>
  </div>

  {#if recentPqrs.length > 0}
  <div class="section">
    <h2 class="section-title">PQRs recientes</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>ID</th><th>Descripcion</th><th>Fecha</th><th>Estado</th></tr></thead>
        <tbody>
          {#each recentPqrs as pqr}
          <tr>
            <td><span class="badge">#{pqr.id_pqr}</span></td>
            <td class="desc-cell">{pqr.descripcion?.slice(0,60)}{pqr.descripcion?.length > 60 ? '...' : ''}</td>
            <td>{pqr.fecha ? new Date(pqr.fecha).toLocaleDateString('es-CO') : '-'}</td>
            <td><span class="status-badge s{pqr.id_estado}">{['','Pendiente','En proceso','Resuelto','Cerrado'][pqr.id_estado] || pqr.id_estado}</span></td>
          </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
  {/if}
</div>

<style>
  /* CAMBIO CLAVE: Quitamos el max-width para que use todo el ancho y alineamos el padding */
  .home { 
    padding: 24px; /* Igualamos al margen que tiene el Power BI en Dashboard.svelte */
    width: 100%;
    max-width: none; /* Eliminamos el límite de 1100px */
    box-sizing: border-box;
  }

  .page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 40px; flex-wrap: wrap; gap: 16px; }
  .greeting { font-size: 14px; color: #9ca3af; letter-spacing: 0.3px; }
  h1 { font-family: var(--font-display); font-size: 36px; font-weight: 800; letter-spacing: -0.03em; }
  .date-badge { background: #fff; border: 1px solid #e5e7eb; border-radius: 100px; padding: 8px 16px; font-size: 13px; color: #6b7280; text-transform: capitalize; align-self: center; }
  
  .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 40px; }
  .stat-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .stat-card:hover { transform: translateY(-2px); }
  .stat-card.accent { background: #f9fafb; border-color: #e5e7eb; }
  .stat-icon { font-size: 11px; margin-bottom: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
  .stat-num { font-size: 32px; font-weight: 800; letter-spacing: -1px; color: #111; }
  .stat-label { font-size: 12px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; }
  
  .section { margin-bottom: 40px; }
  .section-title { font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; color: #9ca3af; }
  
  .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
  .action-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; text-align: left; display: flex; flex-direction: column; gap: 4px; transition: all 0.2s; cursor: pointer; }
  .action-card:hover { border-color: #2563eb; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  .action-icon { font-size: 11px; color: #2563eb; margin-bottom: 8px; text-transform: uppercase; font-weight: 800; }
  .action-label { font-size: 15px; font-weight: 700; color: #111; }
  .action-desc { font-size: 12px; color: #6b7280; }
  
  .table-wrap { overflow-x: auto; border-radius: 12px; border: 1px solid #e5e7eb; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f9fafb; padding: 12px 16px; text-align: left; font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; border-bottom: 1px solid #e5e7eb; }
  td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; color: #374151; }
  tr:last-child td { border-bottom: none; }
  
  .badge { background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600; color: #4b5563; }
  .status-badge { padding: 4px 10px; border-radius: 100px; font-size: 10px; font-weight: 700; letter-spacing: 0.02em; }
  .s1 { background: #fef3c7; color: #92400e; } /* Pendiente */
  .s2 { background: #e0f2fe; color: #075985; } /* En proceso */
  .s3 { background: #dcfce7; color: #166534; } /* Resuelto */
  .s4 { background: #f3f4f6; color: #374151; } /* Cerrado */

  @media (max-width: 768px) { .home { padding: 16px; } h1 { font-size: 26px; } }
</style>