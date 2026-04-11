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
  
  let isAdmin = $derived($currentUser?.id_rol === 1)

  function defaultForm() {
    return {
      descripcion: '',
      fecha: new Date().toISOString().slice(0,16),
      id_usuario: $currentUser?.id_usuario || 1,
      id_tipo: '', 
      id_estado: 1, 
      id_departamento: '', 
      id_prioridad: 1 
    }
  }

  let form = $state(defaultForm())

  let filtered = $derived(pqrs.filter(p => {
    const belongsToMe = isAdmin || p.id_usuario === $currentUser?.id_usuario
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
    if (!isAdmin) { form.id_prioridad = 1; form.id_estado = 1; }
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
        showToast('Solicitud actualizada')
      } else {
        await api.createPqr(payload)
        showToast('Solicitud enviada correctamente')
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
    <div class="toast {toastType}">{toastMsg}</div>
  {/if}

  <div class="page-header">
    <div>
      <h1>
        {#if view === 'list'}{isAdmin ? 'Gestión Global de PQRs' : 'Mis Solicitudes'}
        {:else if view === 'form'}{selected ? 'Editar Solicitud' : 'Nueva PQR'}
        {:else}Detalle de Solicitud{/if}
      </h1>
      <p class="subtitle">
        {#if view === 'list'}{isAdmin ? 'Panel administrativo CUL' : 'Historial de tus trámites institucionales'}
        {:else}Completa los datos para procesar tu requerimiento{/if}
      </p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}<button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>{/if}
      {#if view === 'list'}<button class="btn-primary" onclick={openCreate}>＋ Radicar PQR</button>{/if}
    </div>
  </div>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input class="search-input" type="text" placeholder="Buscar en mis PQRs…" bind:value={searchText} />
      </div>
      <select class="filter-select" bind:value={filterEstado}>
        <option value="">Todos los estados</option>
        {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
      </select>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Sincronizando información...</p></div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              {#if isAdmin}<th>Dpto</th>{/if}
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr (pqr.id_pqr)}
              <tr onclick={() => openDetail(pqr)} class="clickable-row">
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td class="desc-cell">{pqr.descripcion?.slice(0,55)}...</td>
                <td><span class="chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                {#if isAdmin}<td>{getLabelDep(pqr.id_departamento)}</td>{/if}
                <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                <td class="date-cell">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td onclick={(e) => e.stopPropagation()}>
                  <div class="row-actions">
                    <button class="icon-btn edit" onclick={(e) => { e.stopPropagation(); openEdit(pqr) }}>
                      {isAdmin ? '✎' : '👁'}
                    </button>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else if view === 'form'}
    <div class="form-container">
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
              <label>Prioridad</label>
              <select bind:value={form.id_prioridad}>
                {#each prioridades as pr}<option value={pr.id_prioridad}>{pr.nombre}</option>{/each}
              </select>
            </div>
            <div class="field">
              <label>Estado</label>
              <select bind:value={form.id_estado}>
                {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
              </select>
            </div>
          {/if}
        </div>
        <div class="form-actions">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={savePqr} disabled={saving}>
            {#if saving}<span class="spinner-sm"></span>{/if}
            <span>🚀</span> {selected ? 'Guardar Cambios' : 'Enviar Solicitud'}
          </button>
        </div>
      </div>
      <p class="form-footer">Al enviar esta solicitud, aceptas el tratamiento de tus datos personales según la política institucional de la CUL.</p>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; max-width: 1200px; margin: 0 auto; }
  
  /* Header */
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em; }
  .subtitle { color: #64748b; font-size: 15px; margin-top: 4px; }

  /* Toolbar */
  .toolbar { display: flex; gap: 16px; margin-bottom: 24px; }
  .search-wrap { position: relative; flex: 1; }
  .search-input { width: 100%; padding: 12px 16px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; transition: 0.2s; }
  .search-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,0.06); }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.5; }
  .filter-select { padding: 12px 16px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: white; cursor: pointer; }

  /* Tabla */
  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f8fafc; padding: 16px 20px; font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  .clickable-row:hover { background: #f8fafc; cursor: pointer; }

  /* Badges */
  .id-badge { background: #f1f5f9; padding: 4px 8px; border-radius: 6px; font-weight: 700; color: #475569; }
  .chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 100px; font-size: 12px; font-weight: 700; }
  .status-badge { padding: 6px 14px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; }
  .s2 { background: #e0f2fe; color: #075985; }
  .s3 { background: #dcfce7; color: #166534; }

  /* Formulario Mejorado */
  .form-container { display: flex; flex-direction: column; align-items: center; gap: 20px; }
  .form-card { 
    background: white; padding: 40px; border-radius: 28px; border: 1px solid rgba(0,0,0,0.05); 
    width: 100%; max-width: 750px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); 
  }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .field { display: flex; flex-direction: column; gap: 10px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 14px; font-weight: 700; color: #1e293b; }
  input, select, textarea { 
    padding: 14px; border-radius: 14px; border: 1.5px solid #e2e8f0; 
    background: #f8fafc; font-size: 15px; outline: none; transition: 0.2s; 
  }
  input:focus, select:focus, textarea:focus { border-color: #2563eb; background: white; box-shadow: 0 0 0 4px rgba(37,99,235,0.06); }
  
  .form-footer { font-size: 12px; color: #94a3b8; text-align: center; max-width: 500px; }

  /* Botones */
  .btn-primary { 
    background: #2563eb; color: white; border: none; padding: 14px 28px; 
    border-radius: 14px; font-weight: 700; cursor: pointer; transition: 0.3s; 
    display: flex; align-items: center; gap: 10px;
  }
  .btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 10px 15px rgba(37,99,235,0.2); }
  .btn-secondary { background: #f1f5f9; border: none; padding: 14px 24px; border-radius: 14px; color: #475569; font-weight: 600; cursor: pointer; }
  
  .form-actions { margin-top: 32px; display: flex; gap: 12px; justify-content: flex-end; }
  
  .toast { position: fixed; top: 24px; right: 24px; background: #1e293b; color: white; padding: 12px 24px; border-radius: 12px; z-index: 100; font-weight: 600; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>