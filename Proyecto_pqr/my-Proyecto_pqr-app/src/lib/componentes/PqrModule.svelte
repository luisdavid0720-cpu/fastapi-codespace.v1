<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  // --- ESTADOS ---
  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'detail' | 'form'
  let selected = $state(null)
  let saving = $state(false)
  let searchText = $state('')
  let toastMsg = $state('')

  let tipos = $state([]), estados = $state([]), departamentos = $state([])
  
  // REGLA DE ORO: Rol 1 es Admin, Rol 2 es Usuario
  let isAdmin = $derived($currentUser?.id_rol === 1)

  function defaultForm() {
    return { descripcion: '', id_tipo: '', id_departamento: '', id_estado: 1 }
  }
  let form = $state(defaultForm())

  // Filtrado: Estudiante ve lo suyo, Admin ve todo
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
      tipos = t.value?.resultado || t.value || []
      estados = e.value?.resultado || e.value || []
      departamentos = d.value?.resultado || d.value || []
    } catch(e) { console.error("Error de carga:", e) }
    loading = false
  })

  // --- NAVEGACIÓN ---
  function openCreate() { form = defaultForm(); view = 'form' }
  function openEdit(pqr) { form = { ...pqr }; selected = pqr; view = 'form' }
  function openDetail(pqr) { selected = pqr; view = 'detail' }

  // --- ACCIONES ---
  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('⚠️ Completa los campos obligatorios'); return;
    }
    saving = true
    try {
      const payload = {
        ...form,
        id_pqr: selected ? selected.id_pqr : 0,
        id_usuario: selected ? selected.id_usuario : $currentUser?.id_usuario,
        id_estado: form.id_estado || 1,
        id_prioridad: 1
      }
      if (selected) await api.updatePqr(selected.id_pqr, payload);
      else await api.createPqr(payload);
      
      const data = await api.getPqrs();
      pqrs = data.resultado || [];
      view = 'list';
      showToast('✅ Operación exitosa');
    } catch(e) { showToast('❌ Error al procesar') }
    saving = false
  }

  async function deletePqr(id) {
    // CUADRO DE SEGURIDAD
    const confirmar = confirm("🚨 ¿ESTÁS SEGURO?\nEsta acción eliminará la PQR permanentemente y no se puede deshacer.");
    if (!confirmar) return;

    try {
      await api.deletePqr(id);
      pqrs = pqrs.filter(p => p.id_pqr !== id);
      showToast('🗑️ PQR eliminada correctamente');
    } catch (e) { showToast('❌ Error al eliminar'); }
  }

  function showToast(msg) { toastMsg = msg; setTimeout(() => toastMsg = '', 3000) }

  const getLabelEstado = (id) => estados.find(e => e.id_estado == id)?.nombre || 'PENDIENTE'
  const getLabelTipo = (id) => tipos.find(t => t.id_tipo == id)?.nombre || 'Petición'
  const getLabelDep = (id) => departamentos.find(d => d.id_departamento == id)?.nombre || 'Sistemas'
</script>

<div class="module">
  {#if toastMsg}<div class="toast">{toastMsg}</div>{/if}

  <header class="page-header">
    <div class="header-content">
      <h1>
        {#if view === 'list'}{isAdmin ? 'Administración de PQRs' : 'Mis Solicitudes'}
        {:else if view === 'detail'}Detalle del Radicado
        {:else}{selected ? 'Editar PQR' : 'Nueva Solicitud'}{/if}
      </h1>
      <p class="subtitle">Gestión centralizada de trámites institucionales</p>
    </div>
    <div class="header-actions">
      {#if view === 'list' && !isAdmin}
        <button class="btn-primary" onclick={openCreate}>＋ Crear PQR</button>
      {:else if view !== 'list'}
        <button class="btn-back" onclick={() => view = 'list'}>← Volver</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" class="modern-input" placeholder="Buscar por palabra clave..." bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loader-wrap"><span class="spinner"></span><p>Sincronizando con la base de datos...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Categoría</th>
              {#if isAdmin}<th>Estado</th>{/if}
              <th>Fecha</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr>
                <td><span class="id-tag">#{pqr.id_pqr}</span></td>
                <td class="text-main">{pqr.descripcion?.slice(0, 40)}...</td>
                <td><span class="type-chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                {#if isAdmin}
                  <td><span class="status-pill s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                {/if}
                <td class="date-text">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td class="text-center">
                  <div class="actions-group">
                    {#if isAdmin}
                      <button class="icon-btn edit" onclick={() => openEdit(pqr)} title="Editar">✎</button>
                      <button class="icon-btn delete" onclick={() => deletePqr(pqr.id_pqr)} title="Borrar">✕</button>
                    {:else}
                      <button class="icon-btn view" onclick={() => openDetail(pqr)} title="Ver Detalle">👁</button>
                    {/if}
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else if view === 'detail'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="card-top">
          <div class="badge-row">
            <span class="id-large">Solicitud #{selected.id_pqr}</span>
            <span class="status-pill s{selected.id_estado}">{getLabelEstado(selected.id_estado)}</span>
          </div>
          <p class="date-sub">Registrado el {new Date(selected.fecha).toLocaleString('es-CO')}</p>
        </div>
        <div class="card-body">
          <div class="info-section">
            <label class="section-label">Descripción</label>
            <div class="content-box">{selected.descripcion}</div>
          </div>
          <div class="info-grid">
            <div class="info-item"><span class="label">Categoría</span><span class="value">{getLabelTipo(selected.id_tipo)}</span></div>
            <div class="info-item"><span class="label">Área</span><span class="value">{getLabelDep(selected.id_departamento)}</span></div>
          </div>
        </div>
      </div>
    </div>

  {:else if view === 'form'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">{selected ? 'Editar Registro' : 'Nueva Solicitud'}</h2>
          <div class="field full"><label class="section-label">Descripción *</label><textarea bind:value={form.descripcion}></textarea></div>
          <div class="field-group">
            <div class="field"><label class="section-label">Tipo</label><select bind:value={form.id_tipo}>{#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}</select></div>
            <div class="field"><label class="section-label">Departamento</label><select bind:value={form.id_departamento}>{#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}</select></div>
          </div>
          {#if isAdmin}
            <div class="field"><label class="section-label">Estado Administrativo</label><select bind:value={form.id_estado}>{#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}</select></div>
          {/if}
          <div class="form-actions-row">
            <button class="btn-send" onclick={savePqr}>{saving ? 'Guardando...' : 'Confirmar Datos'}</button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 30px 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; width: 100%; }
  h1 { font-size: 28px; font-weight: 800; color: #0f172a; margin: 0; }
  .subtitle { color: #64748b; font-size: 14px; }

  /* TOOLBAR */
  .toolbar { margin-bottom: 25px; }
  .search-wrap { position: relative; max-width: 400px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
  .modern-input { width: 100%; padding: 12px 12px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; }

  /* TABLA */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
  
  .actions-group { display: flex; gap: 12px; justify-content: center; }
  .icon-btn { background: none; border: none; font-size: 18px; cursor: pointer; transition: 0.2s; }
  .icon-btn:hover { transform: scale(1.2); }
  .edit { color: #fbb03b; }
  .delete { color: #ef4444; }
  .view { color: #2563eb; }

  /* CARDS */
  .center-container { display: flex; justify-content: center; padding: 20px 0; }
  .card { background: white; width: 100%; max-width: 650px; border-radius: 30px; border: 1px solid #e2e8f0; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); overflow: hidden; }
  .form-padding { padding: 40px; }
  .card-top { padding: 30px 40px; background: #f8fafc; border-bottom: 1px solid #f1f5f9; }
  .card-body { padding: 40px; }
  .content-box { background: #f8fafc; padding: 20px; border-radius: 15px; border: 1px solid #edf2f7; line-height: 1.6; }
  .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
  .label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
  .value { font-weight: 700; color: #1e293b; display: block; }

  /* FORM */
  .field { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .section-label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
  textarea, select { padding: 12px; border-radius: 10px; border: 1.5px solid #e2e8f0; font-family: inherit; }
  textarea { min-height: 100px; resize: none; }

  /* BUTTONS */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .btn-send { width: 100%; background: #2563eb; color: white; border: none; padding: 16px; border-radius: 14px; font-weight: 700; cursor: pointer; margin-top: 10px; }
  .btn-back { background: #f1f5f9; color: #475569; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 700; cursor: pointer; }

  /* PILLS */
  .status-pill { padding: 5px 12px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; }
  .type-chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 11px; }
  .id-tag { color: #94a3b8; font-weight: 700; }

  .toast { position: fixed; bottom: 20px; right: 20px; background: #0f172a; color: white; padding: 12px 24px; border-radius: 12px; z-index: 100; }
  .spinner { width: 30px; height: 30px; border: 3px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 20px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .animate-up { animation: slideUp 0.3s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>