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

  let tipos = $state([]), estados = $state([]), departamentos = $state([]), prioridades = $state([])
  let isAdmin = $derived($currentUser?.id_rol === 1)

  function defaultForm() {
    return { descripcion: '', id_tipo: '', id_departamento: '', id_estado: 1, id_prioridad: 1 }
  }

  let form = $state(defaultForm())

  let filtered = $derived(pqrs.filter(p => {
    const belongsToMe = isAdmin || Number(p.id_usuario) === Number($currentUser?.id_usuario)
    const matchText = !searchText || p.descripcion?.toLowerCase().includes(searchText.toLowerCase())
    return belongsToMe && matchText
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
    } catch(e) { console.error(e) }
    loading = false
  }

  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(pqr) { selected = pqr; form = { ...pqr }; view = 'form' }
  function openDetail(pqr) { selected = pqr; view = 'detail' }

  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Campos obligatorios incompletos', 'error'); return;
    }
    saving = true;
    try {
      const payload = {
        "id_pqr": selected ? selected.id_pqr : 0,
        "descripcion": form.descripcion,
        "fecha": selected ? selected.fecha : new Date().toISOString(),
        "id_usuario": selected ? selected.id_usuario : (parseInt($currentUser?.id_usuario) || 1),
        "id_tipo": parseInt(form.id_tipo),
        "id_estado": parseInt(form.id_estado),
        "id_departamento": parseInt(form.id_departamento),
        "id_prioridad": parseInt(form.id_prioridad)
      };
      if (selected) await api.updatePqr(selected.id_pqr, payload);
      else await api.createPqr(payload);
      showToast('Operación exitosa');
      await loadAll(); view = 'list';
    } catch (e) { showToast('Error en el servidor', 'error'); }
    finally { saving = false; }
  }

  async function deletePqr(id) {
    if (!confirm('¿Eliminar definitivamente este registro?')) return;
    try {
      await api.deletePqr(id);
      showToast('Registro eliminado');
      await loadAll();
    } catch (e) { showToast('Error al eliminar', 'error'); }
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type;
    setTimeout(() => toastMsg = '', 3000);
  }

  const getLabelEstado = (id) => estados.find(e => e.id_estado == id)?.nombre || 'PENDIENTE'
  const getLabelTipo = (id) => tipos.find(t => t.id_tipo == id)?.nombre || 'Trámite'
  const getLabelDep = (id) => departamentos.find(d => d.id_departamento == id)?.nombre || 'General'
</script>

<div class="module">
  {#if toastMsg}
    <div class="toast {toastType}">{toastMsg}</div>
  {/if}

  <header class="page-header">
    <div class="title-group">
      <h1>{view === 'list' ? (isAdmin ? 'Administración de PQRs' : 'Mis Solicitudes') : 'Detalle de Solicitud'}</h1>
      <p class="subtitle">Gestión centralizada de requerimientos institucionales</p>
    </div>
    {#if view === 'list'}
      <button class="btn-primary" onclick={openCreate}>+ Nueva Solicitud</button>
    {/if}
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-container">
        <span class="search-icon">🔍</span>
        <input class="search-input" type="text" placeholder="Buscar por descripción o palabra clave..." bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loading-box"><span class="loader"></span><p>Sincronizando datos...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th width="80">ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              <th>Departamento</th>
              {#if isAdmin}<th>Estado</th>{/if}
              <th>Fecha</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr>
                <td><span class="id-tag">#{pqr.id_pqr}</span></td>
                <td class="desc-text" title={pqr.descripcion}>{pqr.descripcion?.slice(0, 50)}...</td>
                <td><span class="type-badge">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td class="dep-text">{getLabelDep(pqr.id_departamento)}</td>
                {#if isAdmin}
                  <td><span class="status-pill s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                {/if}
                <td class="date-text">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td class="actions-cell">
                  {#if isAdmin}
                    <button class="btn-icon edit" onclick={() => openEdit(pqr)} title="Corregir">✎</button>
                    <button class="btn-icon delete" onclick={() => deletePqr(pqr.id_pqr)} title="Eliminar">✕</button>
                  {:else}
                    <button class="btn-icon view" onclick={() => openDetail(pqr)} title="Ver Resumen">👁</button>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else}
    <div class="form-wrapper">
        <div class="card">
            <button class="btn-back" onclick={() => view = 'list'}>← Volver a la lista</button>
            <div class="card-content">
                {#if view === 'form'}
                    <h2>{selected ? 'Editar Registro' : 'Nueva PQR'}</h2>
                    <div class="form-grid">
                        <div class="f-full"><label>Descripción</label><textarea bind:value={form.descripcion}></textarea></div>
                        <div><label>Tipo</label><select bind:value={form.id_tipo}>{#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}</select></div>
                        <div><label>Departamento</label><select bind:value={form.id_departamento}>{#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}</select></div>
                        {#if isAdmin}
                            <div><label>Estado</label><select bind:value={form.id_estado}>{#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}</select></div>
                        {/if}
                    </div>
                    <button class="btn-save" onclick={savePqr}>{saving ? 'Guardando...' : 'Guardar Datos'}</button>
                {:else}
                    <div class="detail-view">
                        <h3>Radicado #{selected.id_pqr}</h3>
                        <p class="detail-desc">{selected.descripcion}</p>
                        <div class="detail-info">
                            <p><b>Tipo:</b> {getLabelTipo(selected.id_tipo)}</p>
                            <p><b>Área:</b> {getLabelDep(selected.id_departamento)}</p>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fdfdfd; min-height: 100vh; }
  
  /* HEADER */
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 35px; }
  h1 { font-size: 30px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -1px; }
  .subtitle { color: #94a3b8; font-size: 14px; margin-top: 5px; }

  /* TOOLBAR & BUSCADOR PRO */
  .toolbar { margin-bottom: 25px; }
  .search-container { position: relative; max-width: 450px; }
  .search-input { 
    width: 100%; padding: 14px 14px 14px 45px; border-radius: 14px; border: 1.5px solid #e2e8f0;
    background: white; font-size: 14px; transition: 0.3s; outline: none; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  }
  .search-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1); }
  .search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); font-size: 18px; opacity: 0.4; }

  /* TABLA PROFESIONAL */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.04); }
  table { width: 100%; border-collapse: collapse; text-align: left; }
  th { background: #f8fafc; padding: 18px 20px; font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: #334155; vertical-align: middle; }
  
  .id-tag { font-weight: 800; color: #94a3b8; font-size: 13px; }
  .desc-text { font-weight: 500; color: #1e293b; max-width: 300px; }
  .type-badge { background: #eff6ff; color: #2563eb; padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; }
  .dep-text { color: #64748b; font-weight: 500; }
  .date-text { color: #94a3b8; font-family: monospace; }

  /* ESTADOS DINÁMICOS */
  .status-pill { padding: 6px 12px; border-radius: 100px; font-size: 11px; font-weight: 800; display: inline-block; }
  .s1 { background: #fef3c7; color: #92400e; } /* Pendiente - Amarillo */
  .s2 { background: #dcfce7; color: #166534; } /* Resuelto - Verde */
  .s3 { background: #dbeafe; color: #1e40af; } /* En Proceso - Azul */

  /* ACCIONES CON ESPACIADO */
  .actions-cell { display: flex; gap: 15px; justify-content: center; min-width: 100px; }
  .btn-icon { background: none; border: none; font-size: 20px; cursor: pointer; transition: 0.2s; padding: 5px; }
  .btn-icon:hover { transform: scale(1.25); }
  .edit { color: #fbb03b; }
  .delete { color: #ef4444; }
  .view { color: #3b82f6; }

  /* BOTONES */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.3s; }
  .btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
  
  /* TOAST */
  .toast { position: fixed; bottom: 30px; right: 30px; padding: 16px 28px; border-radius: 16px; background: #1e293b; color: white; font-weight: 600; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2); z-index: 1000; }
  .toast.error { background: #be123c; }

  /* FORM & CARD */
  .form-wrapper { display: flex; justify-content: center; padding: 20px; }
  .card { background: white; width: 100%; max-width: 700px; padding: 40px; border-radius: 24px; border: 1px solid #e2e8f0; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.08); }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 25px 0; }
  .f-full { grid-column: 1 / -1; }
  textarea, select { width: 100%; padding: 12px; border-radius: 10px; border: 1.5px solid #e2e8f0; background: #f8fafc; }
  .btn-save { width: 100%; background: #0f172a; color: white; padding: 15px; border-radius: 12px; border: none; font-weight: 700; cursor: pointer; }
  .btn-back { background: none; border: none; color: #64748b; font-weight: 700; cursor: pointer; margin-bottom: 20px; }
</style>