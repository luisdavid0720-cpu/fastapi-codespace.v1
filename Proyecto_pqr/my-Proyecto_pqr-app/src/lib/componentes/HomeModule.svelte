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
  .home { padding: 40px 48px; max-width: 1100px; }
  .page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 40px; flex-wrap: wrap; gap: 16px; }
  .greeting { font-size: 14px; color: #9ca3af; letter-spacing: 0.3px; }
  h1 { font-family: var(--font-display); font-size: 36px; font-weight: 800; letter-spacing: -0.03em; }
  .date-badge { background: var(--surface); border: 1px solid var(--border); border-radius: 100px; padding: 8px 16px; font-size: 13px; color: var(--text-muted); text-transform: capitalize; align-self: center; }
  .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 40px; }
  .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; transition: transform 0.2s; }
  .stat-card:hover { transform: translateY(-2px); }
  .stat-card.accent { background: rgba(45,45,58,0.04); border-color: rgba(232,255,71,0.25); }
  .stat-icon { font-size: 14px; margin-bottom: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; }
  .stat-num { font-family: var(--font-display); font-size: 42px; font-weight: 800; letter-spacing: -1px; color: #111; }
  .stat-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
  .section { margin-bottom: 40px; }
  .section-title { font-family: var(--font-display); font-size: 18px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 16px; color: var(--text-muted); }
  .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
  .action-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; text-align: left; display: flex; flex-direction: column; gap: 4px; transition: all 0.2s; color: var(--text); }
  .action-card:hover { border-color: var(--accent); background: rgba(232,255,71,0.05); transform: translateY(-2px); }
  .action-icon { font-size: 13px; color: var(--accent); margin-bottom: 8px; text-transform: uppercase; font-weight: 700; }
  .action-label { font-family: var(--font-display); font-size: 15px; font-weight: 700; }
  .action-desc { font-size: 12px; color: var(--text-muted); }
  .table-wrap { overflow-x: auto; border-radius: var(--radius); border: 1px solid var(--border); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: var(--surface); padding: 12px 16px; text-align: left; font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; border-bottom: 1px solid var(--border); }
  td { padding: 14px 16px; border-bottom: 1px solid rgba(42,42,56,0.5); }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: rgba(255,255,255,0.02); }
  .badge { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 3px 8px; font-size: 12px; font-family: monospace; }
  .desc-cell { max-width: 300px; }
  .status-badge { padding: 4px 10px; border-radius: 100px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
  .s1 { background: rgba(225,112,85,0.12); color: var(--warning); }
  .s2 { background: rgba(74,111,165,0.12); color: #4a6fa5; }
  .s3 { background: rgba(0,184,148,0.12); color: #00a381; }
  .s4 { background: rgba(136,144,160,0.12); color: var(--text-muted); }
  @media (max-width: 768px) { .home { padding: 24px 16px; } h1 { font-size: 26px; } }
</style>
