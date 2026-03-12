<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  let pqrs = []
  let loading = true
  let view = 'list' // 'list' | 'form' | 'detail'
  let selected = null
  let saving = false
  let toastMsg = ''
  let toastType = 'success'
  let searchText = ''
  let filterEstado = ''

  // Datos de apoyo
  let tipos = [], estados = [], departamentos = [], prioridades = []

  // Formulario
  let form = defaultForm()

  function defaultForm() {
    return {
      descripcion: '',
      fecha: new Date().toISOString().slice(0,16),
      id_usuario: $currentUser?.id_usuario || 1,
      id_tipo: '',
      id_estado: 1,
      id_departamento: '',
      id_prioridad: ''
    }
  }

  $: isAdmin = $currentUser?.id_rol === 1

  $: filtered = pqrs.filter(p => {
    const matchText = !searchText || p.descripcion?.toLowerCase().includes(searchText.toLowerCase())
    const matchEstado = !filterEstado || p.id_estado == filterEstado
    return matchText && matchEstado
  })

  onMount(async () => {
    await loadAll()
  })

  async function loadAll() {
    loading = true
    try {
      const [p, t, e, d, pr] = await Promise.allSettled([
        api.getPqrs(),
        api.getTiposPqr(),
        api.getEstados(),
        api.getDepartamentos(),
        api.getPrioridades(),
      ])
      pqrs = p.value?.resultado || []
      tipos = t.value?.resultado || []
      estados = e.value?.resultado || []
      departamentos = d.value?.resultado || []
      prioridades = pr.value?.resultado || []
    } catch(e) {}
    loading = false
  }

  function openCreate() {
    form = defaultForm()
    selected = null
    view = 'form'
  }

  function openEdit(pqr) {
    form = { ...pqr, fecha: pqr.fecha?.slice(0,16) }
    selected = pqr
    view = 'form'
  }

  function openDetail(pqr) {
    selected = pqr
    view = 'detail'
  }

  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento || !form.id_prioridad) {
      showToast('Completa todos los campos requeridos', 'error')
      return
    }
    saving = true
    try {
      const payload = {
        ...form,
        fecha: new Date(form.fecha).toISOString(),
        id_usuario: form.id_usuario || $currentUser?.id_usuario || 1,
        id_tipo: parseInt(form.id_tipo),
        id_estado: parseInt(form.id_estado) || 1,
        id_departamento: parseInt(form.id_departamento),
        id_prioridad: parseInt(form.id_prioridad),
      }
      if (selected) {
        await api.updatePqr(selected.id_pqr, payload)
        showToast('PQR actualizada correctamente')
      } else {
        await api.createPqr(payload)
        showToast('PQR creada correctamente')
      }
      await loadAll()
      view = 'list'
    } catch(e) {
      showToast('Error al guardar: ' + e.message, 'error')
    }
    saving = false
  }

  async function deletePqr(id) {
    if (!confirm('¿Eliminar esta PQR?')) return
    try {
      await api.deletePqr(id)
      pqrs = pqrs.filter(p => p.id_pqr !== id)
      showToast('PQR eliminada')
      if (view === 'detail') view = 'list'
    } catch(e) {
      showToast('Error al eliminar', 'error')
    }
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg
    toastType = type
    setTimeout(() => toastMsg = '', 3500)
  }

  function getLabelEstado(id) {
    const labels = ['','Pendiente','En proceso','Resuelto','Cerrado']
    return labels[id] || id
  }

  function getLabelTipo(id) {
    const t = tipos.find(t => t.id_tipo == id)
    return t?.nombre_tipo || id
  }

  function getLabelDep(id) {
    const d = departamentos.find(d => d.id_departamento == id)
    return d?.nombre_departamento || id
  }

  function getLabelPrio(id) {
    const p = prioridades.find(p => p.id_prioridad == id)
    return p?.nombre_prioridad || id
  }
</script>

<div class="module">
  <!-- TOAST -->
  {#if toastMsg}
    <div class="toast {toastType}" role="alert">{toastMsg}</div>
  {/if}

  <!-- HEADER -->
  <div class="page-header">
    <div>
      <h1>
        {#if view === 'list'}Gestión de PQRs
        {:else if view === 'form'}{ selected ? 'Editar PQR' : 'Nueva PQR'}
        {:else}Detalle PQR
        {/if}
      </h1>
      <p class="subtitle">
        {#if view === 'list'}Peticiones, Quejas y Reclamos del sistema
        {:else if view === 'form'}Completa el formulario con la información requerida
        {:else}Información completa de la solicitud
        {/if}
      </p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}
        <button class="btn-secondary" on:click={() => view = 'list'}>← Volver</button>
      {/if}
      {#if view === 'list'}
        <button class="btn-primary" on:click={openCreate}>＋ Nueva PQR</button>
      {/if}
    </div>
  </div>

  <!-- LIST VIEW -->
  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" type="text" placeholder="Buscar PQRs…" bind:value={searchText} />
      </div>
      <select class="filter-select" bind:value={filterEstado}>
        <option value="">Todos los estados</option>
        <option value="1">Pendiente</option>
        <option value="2">En proceso</option>
        <option value="3">Resuelto</option>
        <option value="4">Cerrado</option>
      </select>
    </div>

    {#if loading}
      <div class="loading-state">
        <span class="spinner-lg"></span>
        <p>Cargando PQRs…</p>
      </div>
    {:else if filtered.length === 0}
      <div class="empty-state">
        <div class="empty-icon">◈</div>
        <p>No hay PQRs {searchText ? 'que coincidan' : 'registradas'}</p>
        <button class="btn-primary" on:click={openCreate}>Crear primera PQR</button>
      </div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              <th>Departamento</th>
              <th>Prioridad</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr (pqr.id_pqr)}
              <tr on:click={() => openDetail(pqr)} class="clickable-row">
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td class="desc-cell">{pqr.descripcion?.slice(0,50)}{pqr.descripcion?.length > 50 ? '…' : ''}</td>
                <td><span class="chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td>{getLabelDep(pqr.id_departamento)}</td>
                <td><span class="prio p{pqr.id_prioridad}">{getLabelPrio(pqr.id_prioridad)}</span></td>
                <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                <td class="date-cell">{pqr.fecha ? new Date(pqr.fecha).toLocaleDateString('es-CO') : '—'}</td>
                <td on:click|stopPropagation>
                  <div class="row-actions">
                    <button class="icon-btn edit" title="Editar" on:click|stopPropagation={() => openEdit(pqr)}>✎</button>
                    {#if isAdmin}
                      <button class="icon-btn delete" title="Eliminar" on:click|stopPropagation={() => deletePqr(pqr.id_pqr)}>✕</button>
                    {/if}
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      <p class="count-label">{filtered.length} de {pqrs.length} registros</p>
    {/if}

  <!-- FORM VIEW -->
  {:else if view === 'form'}
    <div class="form-card">
      <div class="form-grid">
        <div class="field full">
          <label>Descripción <span class="req">*</span></label>
          <textarea bind:value={form.descripcion} rows="4" placeholder="Describe detalladamente tu petición, queja o reclamo…"></textarea>
        </div>

        <div class="field">
          <label>Tipo de PQR <span class="req">*</span></label>
          <select bind:value={form.id_tipo}>
            <option value="">Selecciona un tipo</option>
            {#each tipos as t}
              <option value={t.id_tipo}>{t.nombre_tipo}</option>
            {/each}
            {#if tipos.length === 0}
              <option value="1">Petición</option>
              <option value="2">Queja</option>
              <option value="3">Reclamo</option>
            {/if}
          </select>
        </div>

        <div class="field">
          <label>Departamento <span class="req">*</span></label>
          <select bind:value={form.id_departamento}>
            <option value="">Selecciona departamento</option>
            {#each departamentos as d}
              <option value={d.id_departamento}>{d.nombre_departamento}</option>
            {/each}
            {#if departamentos.length === 0}
              <option value="1">Sistemas</option>
              <option value="2">Administración</option>
              <option value="3">Académico</option>
            {/if}
          </select>
        </div>

        <div class="field">
          <label>Prioridad <span class="req">*</span></label>
          <select bind:value={form.id_prioridad}>
            <option value="">Selecciona prioridad</option>
            {#each prioridades as p}
              <option value={p.id_prioridad}>{p.nombre_prioridad}</option>
            {/each}
            {#if prioridades.length === 0}
              <option value="1">Baja</option>
              <option value="2">Media</option>
              <option value="3">Alta</option>
              <option value="4">Urgente</option>
            {/if}
          </select>
        </div>

        {#if isAdmin}
        <div class="field">
          <label>Estado</label>
          <select bind:value={form.id_estado}>
            {#each estados as e}
              <option value={e.id_estado}>{e.nombre_estado}</option>
            {/each}
            {#if estados.length === 0}
              <option value="1">Pendiente</option>
              <option value="2">En proceso</option>
              <option value="3">Resuelto</option>
              <option value="4">Cerrado</option>
            {/if}
          </select>
        </div>
        {/if}

        <div class="field">
          <label>Fecha</label>
          <input type="datetime-local" bind:value={form.fecha} />
        </div>
      </div>

      <div class="form-actions">
        <button class="btn-secondary" on:click={() => view = 'list'}>Cancelar</button>
        <button class="btn-primary" on:click={savePqr} disabled={saving}>
          {#if saving}<span class="spinner-sm"></span>{/if}
          {selected ? 'Actualizar PQR' : 'Crear PQR'}
        </button>
      </div>
    </div>

  <!-- DETAIL VIEW -->
  {:else if view === 'detail' && selected}
    <div class="detail-card">
      <div class="detail-header">
        <span class="id-badge large">#{selected.id_pqr}</span>
        <span class="status-badge s{selected.id_estado}">{getLabelEstado(selected.id_estado)}</span>
      </div>

      <div class="detail-desc">
        <h3>Descripción</h3>
        <p>{selected.descripcion}</p>
      </div>

      <div class="detail-grid">
        <div class="detail-item">
          <span class="detail-label">Tipo</span>
          <span class="detail-value">{getLabelTipo(selected.id_tipo)}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Departamento</span>
          <span class="detail-value">{getLabelDep(selected.id_departamento)}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Prioridad</span>
          <span class="detail-value"><span class="prio p{selected.id_prioridad}">{getLabelPrio(selected.id_prioridad)}</span></span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Fecha</span>
          <span class="detail-value">{selected.fecha ? new Date(selected.fecha).toLocaleString('es-CO') : '—'}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">ID Usuario</span>
          <span class="detail-value">{selected.id_usuario}</span>
        </div>
      </div>

      <div class="detail-actions">
        <button class="btn-secondary" on:click={() => openEdit(selected)}>✎ Editar</button>
        {#if isAdmin}
          <button class="btn-danger" on:click={() => deletePqr(selected.id_pqr)}>✕ Eliminar</button>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px 48px; max-width: 1200px; position: relative; }

  .toast {
    position: fixed;
    top: 24px;
    right: 24px;
    z-index: 999;
    padding: 12px 20px;
    border-radius: var(--radius-sm);
    font-size: 14px;
    font-weight: 500;
    animation: slideIn 0.3s ease;
    max-width: 360px;
  }
  .toast.success { background: rgba(0,184,148,0.12); border: 1px solid rgba(71,255,178,0.4); color: #00a381; }
  .toast.error   { background: rgba(214,48,49,0.1);  border: 1px solid rgba(255,71,71,0.4);  color: var(--danger);  }

  @keyframes slideIn { from { opacity:0; transform: translateX(20px); } to { opacity:1; transform: translateX(0); } }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
    flex-wrap: wrap;
    gap: 16px;
  }

  h1 {
    font-family: var(--font-display);
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 4px;
  }

  .subtitle { color: var(--text-muted); font-size: 14px; }

  .header-actions { display: flex; gap: 10px; }

  .toolbar {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }

  .search-wrap {
    position: relative;
    flex: 1;
    min-width: 200px;
  }

  .search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
  }

  .search-input {
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text);
    padding: 10px 12px 10px 38px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-input:focus { border-color: var(--accent); }

  .filter-select {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text);
    padding: 10px 12px;
    font-size: 14px;
    outline: none;
    cursor: pointer;
  }

  .table-wrap {
    overflow-x: auto;
    border-radius: var(--radius);
    border: 1px solid var(--border);
  }

  table { width: 100%; border-collapse: collapse; font-size: 14px; }

  th {
    background: var(--surface);
    padding: 12px 16px;
    text-align: left;
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }

  td { padding: 14px 16px; border-bottom: 1px solid rgba(42,42,56,0.5); }
  tr:last-child td { border-bottom: none; }

  .clickable-row { cursor: pointer; transition: background 0.15s; }
  .clickable-row:hover td { background: rgba(255,255,255,0.025); }

  .id-badge {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 12px;
    font-family: monospace;
  }

  .id-badge.large { font-size: 18px; padding: 6px 14px; }

  .chip {
    background: rgba(74,111,165,0.1);
    color: #4a6fa5;
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 12px;
    white-space: nowrap;
  }

  .status-badge {
    padding: 4px 10px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    white-space: nowrap;
  }
  .s1 { background: rgba(225,112,85,0.12); color: var(--warning); }
  .s2 { background: rgba(74,111,165,0.12); color: #4a6fa5; }
  .s3 { background: rgba(0,184,148,0.12); color: #00a381; }
  .s4 { background: rgba(136,144,160,0.12); color: var(--text-muted); }

  .prio {
    font-size: 12px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
  }
  .p1 { color: #6b9; background: rgba(0,184,148,0.1); }
  .p2 { color: var(--warning); background: rgba(225,112,85,0.1); }
  .p3 { color: #f84; background: rgba(225,112,85,0.1); }
  .p4 { color: var(--danger); background: rgba(214,48,49,0.08); }

  .desc-cell { max-width: 220px; }
  .date-cell { white-space: nowrap; font-size: 13px; color: var(--text-muted); }

  .row-actions { display: flex; gap: 6px; }

  .icon-btn {
    width: 30px; height: 30px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: transparent;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    transition: all 0.15s;
    color: var(--text-muted);
  }
  .icon-btn.edit:hover { border-color: #4a6fa5; color: #4a6fa5; background: rgba(74,111,165,0.1); }
  .icon-btn.delete:hover { border-color: var(--danger); color: var(--danger); background: rgba(214,48,49,0.08); }

  .count-label {
    margin-top: 12px;
    font-size: 12px;
    color: var(--text-muted);
    text-align: right;
  }

  /* FORM */
  .form-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 32px;
    max-width: 760px;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 28px;
  }

  .field { display: flex; flex-direction: column; gap: 8px; }
  .field.full { grid-column: 1 / -1; }

  label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .req { color: var(--danger); }

  input, select, textarea {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text);
    padding: 11px 14px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
    resize: vertical;
  }
  input:focus, select:focus, textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(232,255,71,0.08);
  }

  select option { background: var(--surface2); }

  .form-actions { display: flex; gap: 12px; justify-content: flex-end; }

  /* DETAIL */
  .detail-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 32px;
    max-width: 700px;
  }

  .detail-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
  }

  .detail-desc {
    margin-bottom: 24px;
    padding: 20px;
    background: var(--surface2);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
  }

  .detail-desc h3 {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 10px;
    font-family: var(--font-display);
  }

  .detail-desc p { line-height: 1.6; font-size: 15px; }

  .detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 28px;
  }

  .detail-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .detail-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    font-weight: 600;
  }

  .detail-value { font-size: 15px; }

  .detail-actions { display: flex; gap: 12px; }

  /* BUTTONS */
  .btn-primary {
    background: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: var(--radius-sm);
    padding: 10px 20px;
    font-family: var(--font-display);
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: opacity 0.2s, transform 0.15s;
  }
  .btn-primary:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

  .btn-secondary {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.15s;
  }
  .btn-secondary:hover { border-color: var(--text-muted); }

  .btn-danger {
    background: rgba(214,48,49,0.08);
    color: var(--danger);
    border: 1px solid rgba(255,71,71,0.3);
    border-radius: var(--radius-sm);
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.15s;
  }
  .btn-danger:hover { background: rgba(214,48,49,0.15); }

  /* STATES */
  .loading-state, .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 40px;
    gap: 16px;
    color: var(--text-muted);
  }

  .empty-icon { font-size: 40px; color: var(--border); }

  .spinner-lg {
    width: 32px; height: 32px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  .spinner-sm {
    width: 14px; height: 14px;
    border: 2px solid rgba(0,0,0,0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    display: inline-block;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  @media (max-width: 768px) {
    .module { padding: 24px 16px; }
    .form-grid { grid-template-columns: 1fr; }
    .detail-grid { grid-template-columns: 1fr; }
    h1 { font-size: 22px; }
  }
</style>
