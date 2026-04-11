<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list')
  let selected = $state(null)
  let saving = $state(false)
  let toastMsg = $state('')
  let toastType = $state('success')
  let searchText = $state('')
  let filterEstado = $state('')
  let tipos = $state([]), estados = $state([]), departamentos = $state([]), prioridades = $state([])
  
  // Determinamos el rol una sola vez para usarlo en todo el componente
  let isAdmin = $derived($currentUser?.id_rol === 1)

  function defaultForm() {
    return {
      descripcion: '',
      fecha: new Date().toISOString().slice(0,16),
      id_usuario: $currentUser?.id_usuario || 1,
      id_tipo: '', 
      id_estado: 1, // Por defecto: Pendiente
      id_departamento: '', 
      id_prioridad: 1 // Por defecto: Baja (para que el usuario no tenga que elegirla)
    }
  }

  let form = $state(defaultForm())

  // FILTRO DE SEGURIDAD: Solo el admin ve todo. El usuario solo ve sus PQRs.
  let filtered = $derived(pqrs.filter(p => {
    // 1. Filtro por Rol (Privacidad)
    const belongsToMe = isAdmin || p.id_usuario === $currentUser?.id_usuario
    
    // 2. Filtros de búsqueda y estado
    const matchText = !searchText || p.descripcion?.toLowerCase().includes(searchText.toLowerCase())
    const matchEstado = !filterEstado || p.id_estado == filterEstado
    
    return belongsToMe && matchText && matchEstado
  }))

  onMount(async () => { await loadAll() })

  async function loadAll() {
    loading = true
    try {
      const [p, t, e, d, pr] = await Promise.allSettled([
        api.getPqrs(), api.getTiposPqr(), api.getEstados(), api.getDepartamentos(), api.getPrioridades(),
      ])
      pqrs = p.value?.resultado || []
      tipos = t.value || []
      estados = e.value || []
      departamentos = d.value || []
      prioridades = pr.value || []
    } catch(e) {}
    loading = false
  }

  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(pqr) { form = { ...pqr, fecha: pqr.fecha?.slice(0,16) }; selected = pqr; view = 'form' }
  function openDetail(pqr) { selected = pqr; view = 'detail' }

  async function savePqr() {
    // Si no es admin, forzamos valores de control internos
    if (!isAdmin) {
      form.id_prioridad = 1; // El usuario no asigna prioridad
      form.id_estado = 1;    // Siempre entra como pendiente
    }

    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Completa los campos obligatorios', 'error'); return
    }
    
    saving = true
    try {
      const payload = {
        ...form,
        fecha: new Date(form.fecha).toISOString(),
        id_usuario: $currentUser?.id_usuario,
        id_tipo: parseInt(form.id_tipo),
        id_estado: parseInt(form.id_estado),
        id_departamento: parseInt(form.id_departamento),
        id_prioridad: parseInt(form.id_prioridad),
      }
      if (selected) {
        await api.updatePqr(selected.id_pqr, payload)
        showToast('PQR actualizada')
      } else {
        await api.createPqr(payload)
        showToast('PQR enviada correctamente')
      }
      await loadAll(); view = 'list'
    } catch(e) { showToast('Error al guardar', 'error') }
    saving = false
  }

  async function deletePqr(id) {
    if (!confirm('¿Eliminar esta PQR?')) return
    try {
      await api.deletePqr(id)
      pqrs = pqrs.filter(p => p.id_pqr !== id)
      showToast('PQR eliminada')
      if (view === 'detail') view = 'list'
    } catch(e) { showToast('Error al eliminar', 'error') }
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3500)
  }

  function getLabelEstado(id) { return ['','Pendiente','En proceso','Resuelto','Cerrado'][id] || id }
  function getLabelTipo(id) { return tipos.find(t => t.id_tipo == id)?.nombre || id }
  function getLabelDep(id) { return departamentos.find(d => d.id_departamento == id)?.nombre || id }
  function getLabelPrio(id) { return prioridades.find(p => p.id_prioridad == id)?.nombre || id }
</script>

<div class="module">
  {#if toastMsg}
    <div class="toast {toastType}" role="alert">{toastMsg}</div>
  {/if}

  <div class="page-header">
    <div>
      <h1>
        {#if view === 'list'}{isAdmin ? 'Gestión Global de PQRs' : 'Mis Solicitudes'}
        {:else if view === 'form'}{selected ? 'Editar Solicitud' : 'Nueva PQR'}
        {:else}Detalle de Solicitud{/if}
      </h1>
      <p class="subtitle">
        {#if view === 'list'}{isAdmin ? 'Panel de control administrativo' : 'Historial personal de peticiones, quejas y reclamos'}
        {:else}Completa la información para procesar tu solicitud{/if}
      </p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}<button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>{/if}
      {#if view === 'list'}<button class="btn-primary" onclick={openCreate}>＋ Crear Solicitud</button>{/if}
    </div>
  </div>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" type="text" placeholder="Buscar en mis PQRs…" bind:value={searchText} />
      </div>
      <select class="filter-select" bind:value={filterEstado}>
        <option value="">Todos los estados</option>
        {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
      </select>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Cargando información…</p></div>
    {:else if filtered.length === 0}
      <div class="empty-state">
        <div class="empty-icon">◈</div>
        <p>{searchText ? 'No se encontraron coincidencias' : 'Aún no has registrado ninguna solicitud'}</p>
        <button class="btn-primary" onclick={openCreate}>Radicar mi primera PQR</button>
      </div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              {#if isAdmin}<th>Departamento</th>{/if}
              {#if isAdmin}<th>Prioridad</th>{/if}
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr (pqr.id_pqr)}
              <tr onclick={() => openDetail(pqr)} class="clickable-row">
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td class="desc-cell">{pqr.descripcion?.slice(0,60)}...</td>
                <td><span class="chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                
                {#if isAdmin}<td>{getLabelDep(pqr.id_departamento)}</td>{/if}
                {#if isAdmin}<td><span class="prio p{pqr.id_prioridad}">{getLabelPrio(pqr.id_prioridad)}</span></td>{/if}
                
                <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                <td class="date-cell">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td onclick={(e) => e.stopPropagation()}>
                  <div class="row-actions">
                    <button class="icon-btn edit" title="Ver/Editar" onclick={(e) => { e.stopPropagation(); openEdit(pqr) }}>
                       {isAdmin ? '✎' : '👁'}
                    </button>
                    {#if isAdmin}
                      <button class="icon-btn delete" onclick={(e) => { e.stopPropagation(); deletePqr(pqr.id_pqr) }}>✕</button>
                    {/if}
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else if view === 'form'}
    <div class="form-card">
      <div class="form-grid">
        <div class="field full">
          <label>¿Qué deseas reportar? <span class="req">*</span></label>
          <textarea bind:value={form.descripcion} rows="5" placeholder="Describe detalladamente los hechos..."></textarea>
        </div>
        <div class="field">
          <label>Tipo de Solicitud <span class="req">*</span></label>
          <select bind:value={form.id_tipo}>
            <option value="">Seleccionar...</option>
            {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
          </select>
        </div>
        <div class="field">
          <label>Departamento Destino <span class="req">*</span></label>
          <select bind:value={form.id_departamento}>
            <option value="">Seleccionar departamento...</option>
            {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
          </select>
        </div>

        {#if isAdmin}
          <div class="field">
            <label>Prioridad Administrativa</label>
            <select bind:value={form.id_prioridad}>
              {#each prioridades as pr}<option value={pr.id_prioridad}>{pr.nombre}</option>{/each}
            </select>
          </div>
          <div class="field">
            <label>Estado del Trámite</label>
            <select bind:value={form.id_estado}>
              {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
            </select>
          </div>
        {/if}
      </div>
      <div class="form-actions">
        <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
        <button class="btn-primary" onclick={savePqr} disabled={saving}>
          {saving ? 'Guardando...' : (selected ? 'Guardar Cambios' : 'Enviar Solicitud')}
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; max-width: 1200px; margin: 0 auto; }
  
  /* Cabecera */
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
  h1 { font-size: 28px; font-weight: 800; color: #0f172a; margin: 0; }
  .subtitle { color: #64748b; font-size: 14px; margin-top: 4px; }

  /* Toolbar de búsqueda y filtros */
  .toolbar { display: flex; gap: 12px; margin-bottom: 24px; align-items: center; }
  .search-wrap { position: relative; flex: 1; }
  .search-input { 
    width: 100%; padding: 10px 16px 10px 40px; border-radius: 10px; 
    border: 1px solid #e2e8f0; background: white; outline: none;
  }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
  .filter-select { padding: 10px 16px; border-radius: 10px; border: 1px solid #e2e8f0; background: white; color: #475569; }

  /* Tabla Profesional */
  .table-wrap { background: white; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
  table { width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }
  th { background: #f8fafc; padding: 14px 20px; font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  .clickable-row:hover { background: #f8fafc; cursor: pointer; }

  /* Badges y Chips */
  .id-badge { background: #f1f5f9; padding: 4px 8px; border-radius: 6px; font-weight: 700; color: #475569; font-size: 12px; }
  .chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 100px; font-size: 12px; font-weight: 600; }
  .status-badge { padding: 6px 12px; border-radius: 100px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; } /* Pendiente */
  .s2 { background: #e0f2fe; color: #075985; } /* Proceso */
  .s3 { background: #dcfce7; color: #166534; } /* Resuelto */

  .prio { padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
  .p1 { background: #f1f5f9; color: #475569; } /* Baja */
  .p3 { background: #fee2e2; color: #991b1b; } /* Alta */

  /* Botones */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 700; cursor: pointer; transition: 0.2s; }
  .btn-primary:hover { background: #1d4ed8; transform: translateY(-1px); }
  .btn-secondary { background: white; border: 1px solid #e2e8f0; padding: 10px 20px; border-radius: 10px; font-weight: 600; cursor: pointer; }

  .icon-btn { border: 1px solid #e2e8f0; background: white; width: 32px; height: 32px; border-radius: 8px; cursor: pointer; transition: 0.2s; }
  .icon-btn:hover { border-color: #2563eb; color: #2563eb; }

  /* Estados de carga */
  .loading-state { padding: 60px; text-align: center; color: #64748b; }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 0 auto 16px; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Formulario */
  .form-card { background: white; padding: 32px; border-radius: 20px; border: 1px solid #e2e8f0; max-width: 800px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .field { display: flex; flex-direction: column; gap: 8px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 13px; font-weight: 700; color: #475569; }
  input, select, textarea { padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; background: #f8fafc; outline: none; }
  input:focus, select:focus, textarea:focus { border-color: #2563eb; background: white; }
</style>
