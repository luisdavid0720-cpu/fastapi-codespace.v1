<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'detail' | 'form'
  let selected = $state(null)
  let saving = $state(false)
  let searchText = $state('')
  let toastMsg = $state('')

  // Catálogos
  let tipos = $state([]), estados = $state([]), departamentos = $state([])
  
  function defaultForm() {
    return { descripcion: '', id_tipo: '', id_departamento: '' }
  }
  let form = $state(defaultForm())

  let filtered = $derived(pqrs.filter(p => {
    const belongsToMe = Number(p.id_usuario) === Number($currentUser?.id_usuario)
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

  // Navegación
  function openCreate() { form = defaultForm(); view = 'form' }
  function openDetail(pqr) { selected = pqr; view = 'detail' }

  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Completa todos los campos'); return;
    }
    saving = true
    try {
      const payload = {
        ...form,
        id_pqr: 0,
        fecha: new Date().toISOString(),
        id_usuario: $currentUser?.id_usuario,
        id_estado: 1, // Pendiente
        id_prioridad: 1
      }
      await api.createPqr(payload)
      const data = await api.getPqrs()
      pqrs = data.resultado || []
      view = 'list'
      showToast('¡PQR enviada con éxito!')
    } catch(e) { showToast('Error al enviar') }
    saving = false
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
        {#if view === 'list'}Mis Solicitudes
        {:else if view === 'detail'}Detalle del Radicado
        {:else}Nueva Solicitud{/if}
      </h1>
      <p class="subtitle">Gestiona y consulta el estado de tus trámites institucionales</p>
    </div>
    <div class="header-actions">
      {#if view === 'list'}
        <button class="btn-create" onclick={openCreate}>＋ Crear PQR</button>
      {:else}
        <button class="btn-back" onclick={() => view = 'list'}>← Volver</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
<<<<<<< HEAD
      <div class="search-box">
        <span class="icon">🔍</span>
        <input type="text" placeholder="Buscar por palabra clave..." bind:value={searchText} />
=======
      <div class="search-container">
        <span class="search-icon">🔍</span>
        <input type="text" class="modern-input" placeholder="Buscar por palabra clave..." bind:value={searchText} />
>>>>>>> b7e1b15 (cambios en usuario)
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

  {:else if view === 'detail'}
    <div class="center-container">
<<<<<<< HEAD
      <div class="detail-card">
=======
      <div class="card animate-up">
>>>>>>> b7e1b15 (cambios en usuario)
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
            <div class="info-item">
              <span class="label">Categoría</span>
              <span class="value">{getLabelTipo(selected.id_tipo)}</span>
            </div>
            <div class="info-item">
              <span class="label">Área Destino</span>
              <span class="value">{getLabelDep(selected.id_departamento)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  {:else if view === 'form'}
    <div class="center-container">
<<<<<<< HEAD
      <div class="form-card">
        <h2>Radicar nueva PQR</h2>
        <div class="form-body">
          <div class="field">
            <label>¿Qué sucedió? (Descripción)</label>
=======
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">Radicar nueva PQR</h2>
          <div class="field">
            <label class="section-label">¿Qué sucedió? <small>(Descripción)</small></label>
>>>>>>> b7e1b15 (cambios en usuario)
            <textarea bind:value={form.descripcion} placeholder="Explica detalladamente tu solicitud..."></textarea>
          </div>
          <div class="field-group">
            <div class="field">
              <label class="section-label">Tipo</label>
              <select bind:value={form.id_tipo}>
                <option value="">Selecciona...</option>
                {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
              </select>
            </div>
            <div class="field">
              <label class="section-label">Departamento</label>
              <select bind:value={form.id_departamento}>
                <option value="">Selecciona...</option>
                {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
              </select>
            </div>
          </div>
          <button class="btn-send" onclick={savePqr} disabled={saving}>
            {saving ? 'Procesando...' : '🚀 Enviar Solicitud'}
          </button>
        </div>
<<<<<<< HEAD
        <button class="btn-send" onclick={savePqr} disabled={saving}>
          {saving ? 'Enviando...' : '🚀 Enviar Solicitud'}
        </button>
=======
>>>>>>> b7e1b15 (cambios en usuario)
      </div>
    </div>
  {/if}
</div>

<style>
  /* --- REUTILIZADOS Y MEJORADOS --- */
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
  h1 { font-size: 30px; font-weight: 800; color: #1e293b; margin: 0; }
  .subtitle { color: #94a3b8; font-size: 14px; }

  /* BOTONES */
<<<<<<< HEAD
  .btn-create { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; }
  .btn-create:hover { background: #1d4ed8; transform: translateY(-2px); }
  .btn-back { background: #f1f5f9; border: none; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; }

  /* TABLA */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 18px 20px; text-align: left; font-size: 12px; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
  .view-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: #3b82f6; transition: 0.2s; }
  .view-btn:hover { transform: scale(1.3); }

  /* CARDS (DETAIL & FORM) */
  .center-container { display: flex; justify-content: center; padding-bottom: 40px; }
  .detail-card, .form-card { 
    background: white; width: 100%; max-width: 650px; 
    border-radius: 30px; border: 1px solid #e2e8f0; 
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.08); overflow: hidden;
  }
  .form-card { padding: 40px; }
  .card-top { padding: 35px 40px; background: #f8fafc; border-bottom: 1px solid #f1f5f9; }
  .card-body { padding: 40px; }
  .content-box { background: #f8fafc; padding: 25px; border-radius: 18px; border: 1px solid #edf2f7; margin-bottom: 30px; }
  
  /* FORM ELEMENTS */
  .field { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  label { font-size: 12px; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
  textarea, select { padding: 14px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #fcfcfc; font-family: inherit; }
  .btn-send { width: 100%; background: #2563eb; color: white; border: none; padding: 16px; border-radius: 14px; font-weight: 700; cursor: pointer; margin-top: 10px; }

  /* CHIPS Y OTROS */
  .id-tag { color: #94a3b8; font-weight: 700; }
  .status-pill { padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; }
  .type-chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 12px; }
  .toast { position: fixed; bottom: 20px; right: 20px; background: #1e293b; color: white; padding: 12px 24px; border-radius: 12px; z-index: 100; }
=======
  .btn-create { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
  .btn-back { background: white; border: 1.5px solid #e2e8f0; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; }

  /* TOOLBAR & SEARCH */
  .toolbar { margin-bottom: 25px; }
  .search-container { position: relative; max-width: 400px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
  .modern-input { width: 100%; padding: 12px 12px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; font-size: 14px; outline: none; transition: 0.3s; }
  .modern-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.05); }

  /* TABLE */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 18px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #f1f5f9; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: #334155; }
  .view-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: #3b82f6; transition: 0.2s; }
  .view-btn:hover { transform: scale(1.3); }

  /* CARD SYSTEM (CORREGIDO) */
  .center-container { display: flex; justify-content: center; padding: 20px 0 60px; }
  .card { 
    background: white; width: 100%; max-width: 680px; 
    border-radius: 32px; border: 1px solid #e2e8f0; 
    box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); overflow: hidden;
  }
  
  /* PADDING PARA EL FORMULARIO */
  .form-padding { padding: 45px; }
  .card-title { font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 30px; }

  /* ESTILOS DEL DETALLE (CORREGIDO) */
  .card-top { padding: 35px 45px; background: #f8fafc; border-bottom: 1px solid #f1f5f9; }
  .card-body { padding: 45px; }
  .badge-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .id-large { font-size: 24px; font-weight: 800; color: #0f172a; }
  .date-sub { color: #94a3b8; font-size: 13px; margin: 0; }
  
  .info-section { margin-bottom: 30px; }
  .content-box { background: #f8fafc; padding: 25px; border-radius: 20px; border: 1px solid #edf2f7; line-height: 1.7; font-size: 15px; color: #334155; }

  .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .info-item { display: flex; flex-direction: column; gap: 6px; }
  .label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  .value { font-weight: 700; color: #1e293b; font-size: 15px; }

  /* FORM FIELDS */
  .field { display: flex; flex-direction: column; gap: 10px; margin-bottom: 25px; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .section-label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  textarea, select { padding: 15px; border-radius: 14px; border: 1.5px solid #e2e8f0; background: #fcfcfc; font-size: 14px; outline: none; }
  textarea { min-height: 120px; resize: none; }
  
  .btn-send { width: 100%; background: #2563eb; color: white; border: none; padding: 18px; border-radius: 16px; font-weight: 800; font-size: 16px; cursor: pointer; margin-top: 15px; }

  /* PILLS */
  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; }
  .status-pill { padding: 6px 14px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; }
  .type-chip { background: #eff6ff; color: #2563eb; padding: 5px 12px; border-radius: 8px; font-weight: 700; font-size: 12px; }

  .toast { position: fixed; bottom: 30px; right: 30px; background: #0f172a; color: white; padding: 16px 28px; border-radius: 16px; font-weight: 600; z-index: 100; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
  .animate-up { animation: slideUp 0.4s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
>>>>>>> b7e1b15 (cambios en usuario)
</style>