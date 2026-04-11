<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  // Estados de la UI
  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'form' | 'detail'
  let selected = $state(null)
  let saving = $state(false)
  let toastMsg = $state('')
  let toastType = $state('success')
  let searchText = $state('')
  let filterEstado = $state('')

  // Catálogos para los Selects
  let tipos = $state([]), estados = $state([]), departamentos = $state([]), prioridades = $state([])
  
  // Seguridad: Verificamos si el usuario es Admin (Rol 1)
  let isAdmin = $derived($currentUser?.id_rol === 1)

  function defaultForm() {
    return { descripcion: '', id_tipo: '', id_departamento: '', id_estado: 1, id_prioridad: 1 }
  }

  let form = $state(defaultForm())

  // FILTRO DE SEGURIDAD SEGÚN ROL
  let filtered = $derived(pqrs.filter(p => {
    // Si es Admin ve todo, si es Usuario solo ve lo que coincida con su ID
    const belongsToMe = isAdmin || Number(p.id_usuario) === Number($currentUser?.id_usuario)
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
    } catch(e) { console.error("Error al cargar datos:", e) }
    loading = false
  }

  // --- NAVEGACIÓN ---
  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  
  function openEdit(pqr) { 
    selected = pqr; 
    form = { ...pqr }; 
    view = 'form'; 
  }

  function openDetail(pqr) { 
    selected = pqr; 
    view = 'detail'; 
  }

  // --- ACCIONES API ---
  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Completa los campos obligatorios', 'error');
      return;
    }

    saving = true;
    try {
      const payload = {
        "id_pqr": selected ? selected.id_pqr : 0,
        "descripcion": form.descripcion,
        "fecha": selected ? selected.fecha : new Date().toISOString(),
        "id_usuario": selected ? selected.id_usuario : (parseInt($currentUser?.id_usuario) || 1),
        "id_tipo": parseInt(form.id_tipo),
        "id_estado": parseInt(form.id_estado) || 1,
        "id_departamento": parseInt(form.id_departamento),
        "id_prioridad": parseInt(form.id_prioridad) || 1
      };

      if (selected) {
        await api.updatePqr(selected.id_pqr, payload);
        showToast('PQR actualizada correctamente');
      } else {
        await api.createPqr(payload);
        showToast('¡PQR radicada con éxito!');
      }

      await loadAll();
      view = 'list';
    } catch (error) {
      showToast('Error al procesar la solicitud', 'error');
    } finally { saving = false; }
  }

  async function deletePqr(id) {
    if (!confirm('¿Seguro que deseas eliminar esta PQR? Esta acción no se puede deshacer.')) return;
    try {
      await api.deletePqr(id);
      showToast('Registro eliminado', 'success');
      await loadAll();
    } catch (e) { showToast('Error al eliminar', 'error'); }
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type;
    setTimeout(() => toastMsg = '', 3500);
  }

  function getLabelEstado(id) { return estados.find(e => e.id_estado == id)?.nombre || 'PENDIENTE' }
  function getLabelTipo(id) { return tipos.find(t => t.id_tipo == id)?.nombre || 'Peticion' }
  function getLabelDep(id) { return departamentos.find(d => d.id_departamento == id)?.nombre || 'Sistemas' }
</script>

<div class="module">
  {#if toastMsg}
    <div class="toast {toastType}">{toastMsg}</div>
  {/if}

  <header class="page-header">
    <div>
      <h1>{view === 'list' ? (isAdmin ? 'Administración de PQRs' : 'Mis Trámites') : (view === 'form' ? 'Formulario PQR' : 'Resumen de Solicitud')}</h1>
      <p class="subtitle">{view === 'list' ? 'Gestión centralizada de solicitudes institucionales' : 'Detalles del registro en sistema'}</p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}<button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>{/if}
      {#if view === 'list'}<button class="btn-primary" onclick={openCreate}>＋ Nueva Solicitud</button>{/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input class="search-input" type="text" placeholder="Buscar por descripción..." bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Consultando Base de Datos...</p></div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              <th>Departamento</th>
              {#if isAdmin}<th>Estado</th>{/if}
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr>
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td>{pqr.descripcion?.slice(0, 35)}...</td>
                <td><span class="chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td>{getLabelDep(pqr.id_departamento)}</td>
                {#if isAdmin}
                  <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                {/if}
                <td>{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td class="actions-cell">
                  {#if isAdmin}
                    <button class="icon-btn edit-btn" onclick={() => openEdit(pqr)} title="Editar">✎</button>
                    <button class="icon-btn delete-btn" onclick={() => deletePqr(pqr.id_pqr)} title="Eliminar">✕</button>
                  {:else}
                    <button class="view-btn" onclick={() => openDetail(pqr)} title="Ver Detalle">👁</button>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else if view === 'form'}
    <div class="container-center">
      <div class="form-card">
        <h2>{selected ? 'Actualizar Información' : 'Nueva Solicitud'}</h2>
        <div class="form-grid">
          <div class="field full">
            <label>Descripción <span class="req">*</span></label>
            <textarea bind:value={form.descripcion} rows="4"></textarea>
          </div>
          <div class="field">
            <label>Tipo</label>
            <select bind:value={form.id_tipo}>
              {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
            </select>
          </div>
          <div class="field">
            <label>Departamento</label>
            <select bind:value={form.id_departamento}>
              {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
            </select>
          </div>
          {#if isAdmin}
            <div class="field">
              <label>Estado Administrativo</label>
              <select bind:value={form.id_estado}>
                {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
              </select>
            </div>
          {/if}
        </div>
        <div class="form-actions">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={savePqr}>{saving ? 'Guardando...' : 'Guardar Cambios'}</button>
        </div>
      </div>
    </div>

  {:else if view === 'detail'}
    <div class="container-center">
      <div class="detail-card">
        <div class="detail-header">
          <h3>Resumen de Trámite #{selected.id_pqr}</h3>
          <span class="chip">{getLabelTipo(selected.id_tipo)}</span>
        </div>
        <div class="text-box">{selected.descripcion}</div>
        <div class="detail-footer">
          <p><b>Departamento:</b> {getLabelDep(selected.id_departamento)}</p>
          <p><b>Fecha:</b> {new Date(selected.fecha).toLocaleString()}</p>
        </div>
        <button class="btn-primary full-w" onclick={() => view = 'list'}>Volver a mis trámites</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 30px; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
  h1 { font-size: 28px; color: #0f172a; margin: 0; }
  .subtitle { color: #64748b; font-size: 14px; }

  /* TABLA */
  .table-wrap { background: white; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px; text-align: left; font-size: 13px; color: #64748b; }
  td { padding: 16px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
  
  .actions-cell { display: flex; gap: 10px; }
  .icon-btn { border: none; background: none; cursor: pointer; font-size: 18px; padding: 5px; transition: 0.2s; }
  
  /* Lápiz Amarillo */
  .edit-btn { color: #fbb03b; }
  .edit-btn:hover { transform: scale(1.2); }
  
  /* X Roja */
  .delete-btn { color: #ef4444; }
  .delete-btn:hover { transform: scale(1.2); }
  
  /* Ojo Azul */
  .view-btn { border: none; background: none; cursor: pointer; color: #2563eb; font-size: 18px; }

  .status-badge { padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; background: #fef3c7; color: #92400e; }
  .id-badge { font-weight: 800; color: #94a3b8; }
  .chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }

  /* CARDS */
  .container-center { display: flex; justify-content: center; padding: 20px; }
  .form-card, .detail-card { background: white; padding: 32px; border-radius: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); width: 100%; max-width: 600px; border: 1px solid #e2e8f0; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
  .field.full { grid-column: 1 / -1; }
  .text-box { background: #f8fafc; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid #e2e8f0; line-height: 1.6; }
  
  label { font-size: 13px; font-weight: 700; color: #475569; margin-bottom: 6px; display: block; }
  textarea, select { width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; background: #fcfcfc; }

  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 10px; font-weight: 700; cursor: pointer; }
  .btn-secondary { background: #f1f5f9; border: none; padding: 12px 24px; border-radius: 10px; color: #475569; font-weight: 600; cursor: pointer; }
  .full-w { width: 100%; margin-top: 20px; }

  .toast { position: fixed; bottom: 20px; right: 20px; padding: 15px 25px; border-radius: 12px; color: white; background: #0f172a; z-index: 1000; }
</style>