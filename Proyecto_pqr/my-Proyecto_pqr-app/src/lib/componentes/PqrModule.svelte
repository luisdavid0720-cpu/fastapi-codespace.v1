<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'detail'
  let selected = $state(null)
  let searchText = $state('')

  // Catálogos
  let tipos = $state([]), estados = $state([]), departamentos = $state([])
  
  // Seguridad: Solo Luis (Usuario) ve sus datos
  let isAdmin = $derived($currentUser?.id_rol === 1)

  let filtered = $derived(pqrs.filter(p => {
    const belongsToMe = isAdmin || Number(p.id_usuario) === Number($currentUser?.id_usuario)
    const matchText = !searchText || p.descripcion?.toLowerCase().includes(searchText.toLowerCase())
    return belongsToMe && matchText
  }))

  onMount(async () => {
    loading = true
    try {
      const [p, t, e, d] = await Promise.allSettled([
        api.getPqrs(), api.getTiposPqr(), api.getEstados(), api.getDepartamentos()
      ])
      pqrs = p.value?.resultado || []
      tipos = t.value || []
      estados = e.value || []
      departamentos = d.value || []
    } catch(e) { console.error(e) }
    loading = false
  })

  // Función para abrir el detalle (Solo lectura)
  function openDetail(pqr) { 
    selected = pqr; 
    view = 'detail'; 
  }

  // Helpers
  const getLabelEstado = (id) => estados.find(e => e.id_estado == id)?.nombre || 'PENDIENTE'
  const getLabelTipo = (id) => tipos.find(t => t.id_tipo == id)?.nombre || 'Petición'
  const getLabelDep = (id) => departamentos.find(d => d.id_departamento == id)?.nombre || 'Sistemas'
</script>

<div class="module">
  <header class="page-header">
    <div class="header-content">
      <h1>{view === 'list' ? 'Mis Solicitudes' : 'Detalle del Radicado'}</h1>
      <p class="subtitle">Gestiona y consulta el estado de tus trámites institucionales</p>
    </div>
    {#if view === 'detail'}
      <button class="btn-back" onclick={() => view = 'list'}>← Volver al listado</button>
    {/if}
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-box">
        <span class="icon">🔍</span>
        <input type="text" placeholder="Buscar por palabra clave..." bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loader-wrap"><span class="spinner"></span><p>Sincronizando...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción Breve</th>
              <th>Categoría</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th class="text-center">Ver</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr>
                <td><span class="id-tag">#{pqr.id_pqr}</span></td>
                <td class="text-main">{pqr.descripcion?.slice(0, 45)}...</td>
                <td><span class="type-chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td><span class="status-pill s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                <td class="date-text">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td class="text-center">
                  <button class="view-btn" onclick={() => openDetail(pqr)}>👁</button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else if view === 'detail' && selected}
    <div class="detail-container">
      <div class="detail-card">
        <div class="card-top">
          <div class="badge-row">
            <span class="id-large">Solicitud #{selected.id_pqr}</span>
            <span class="status-pill s{selected.id_estado}">{getLabelEstado(selected.id_estado)}</span>
          </div>
          <p class="date-sub">Registrado el {new Date(selected.fecha).toLocaleString('es-CO')}</p>
        </div>

        <div class="card-body">
          <div class="info-section">
            <label>Descripción de la solicitud</label>
            <div class="content-box">
              {selected.descripcion}
            </div>
          </div>

          <div class="info-grid">
            <div class="info-item">
              <span class="label">Categoría</span>
              <span class="value">{getLabelTipo(selected.id_tipo)}</span>
            </div>
            <div class="info-item">
              <span class="label">Área Encargada</span>
              <span class="value">{getLabelDep(selected.id_departamento)}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <p>Esta es una copia informativa de tu radicado. Si necesitas adjuntar evidencias, contacta a soporte.</p>
          <button class="btn-primary" onclick={() => view = 'list'}>Entendido</button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  /* --- DISEÑO BASE --- */
  .module { padding: 40px; font-family: 'Inter', system-ui, sans-serif; background: #fcfdfe; min-height: 100vh; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
  h1 { font-size: 30px; font-weight: 800; color: #1e293b; margin: 0; letter-spacing: -0.8px; }
  .subtitle { color: #94a3b8; font-size: 15px; margin-top: 5px; }

  /* --- TABLA --- */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 18px 20px; text-align: left; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; border-bottom: 1px solid #f1f5f9; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
  
  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; }
  .text-main { font-weight: 500; color: #334155; }
  .type-chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 12px; }
  
  /* ESTADOS */
  .status-pill { padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; } /* Pendiente */
  
  .view-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: #3b82f6; transition: 0.2s; }
  .view-btn:hover { transform: scale(1.3); }

  /* --- TARJETA DE DETALLE (EL "BONITO") --- */
  .detail-container { display: flex; justify-content: center; padding-top: 20px; }
  .detail-card { 
    background: white; width: 100%; max-width: 650px; 
    border-radius: 30px; border: 1px solid #e2e8f0; 
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.08);
    overflow: hidden;
  }

  .card-top { padding: 35px 40px; background: linear-gradient(to right, #ffffff, #f8fafc); border-bottom: 1px solid #f1f5f9; }
  .badge-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .id-large { font-size: 24px; font-weight: 800; color: #0f172a; }
  .date-sub { color: #94a3b8; font-size: 13px; margin: 0; }

  .card-body { padding: 40px; }
  .info-section label { display: block; font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
  .content-box { 
    background: #f8fafc; padding: 25px; border-radius: 18px; 
    line-height: 1.7; color: #334155; border: 1px solid #edf2f7; 
    font-size: 15px; margin-bottom: 30px;
  }

  .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
  .info-item { display: flex; flex-direction: column; gap: 5px; }
  .info-item .label { font-size: 11px; color: #94a3b8; font-weight: 700; text-transform: uppercase; }
  .info-item .value { font-size: 15px; font-weight: 700; color: #1e293b; }

  .card-footer { padding: 30px 40px; background: #f8fafc; text-align: center; }
  .card-footer p { font-size: 12px; color: #94a3b8; margin-bottom: 20px; }

  /* --- BOTONES --- */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 14px 40px; border-radius: 14px; font-weight: 700; cursor: pointer; transition: 0.3s; width: 100%; }
  .btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3); }
  .btn-back { background: #f1f5f9; border: none; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; }

  .toolbar { margin-bottom: 25px; }
  .search-box { position: relative; max-width: 400px; }
  .search-box input { width: 100%; padding: 12px 15px 12px 40px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; transition: 0.2s; }
  .search-box input:focus { border-color: #2563eb; background: white; }
  .search-box .icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
</style>