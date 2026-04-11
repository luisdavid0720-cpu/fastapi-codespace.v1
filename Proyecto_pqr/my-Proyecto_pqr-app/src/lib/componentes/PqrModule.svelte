<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  // Estados de la interfaz
  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'form'
  let selected = $state(null)
  let saving = $state(false)
  let toastMsg = $state('')
  let toastType = $state('success')

  // Filtros y Búsqueda
  let searchText = $state('')
  let filterEstado = $state('')

  // Catálogos para selects
  let tipos = $state([])
  let estados = $state([])
  let departamentos = $state([])

  // Derivados: Comprobar si es Admin (Rol ID 1)
  let isAdmin = $derived($currentUser?.id_rol === 1)

  // Estructura limpia del formulario
  function defaultForm() {
    return {
      descripcion: '',
      id_tipo: '', 
      id_departamento: '', 
    }
  }

  let form = $state(defaultForm())

  // FILTRO DE SEGURIDAD INTEGURADO: 
  // 1. Un estudiante solo ve sus PQRs (id_usuario coincidente)
  // 2. Un admin ve TODO
  // 3. Aplica búsqueda por texto y filtro por estado
  let filtered = $derived(pqrs.filter(p => {
    // Regla de Oro: Si no eres admin, solo ves lo tuyo
    const belongsToMe = isAdmin || p.id_usuario === $currentUser?.id_usuario;
    
    // Filtros de UI
    const matchText = !searchText || p.descripcion?.toLowerCase().includes(searchText.toLowerCase());
    const matchEstado = !filterEstado || p.id_estado == filterEstado;

    return belongsToMe && matchText && matchEstado;
  }))

  onMount(async () => {
    loading = true
    try {
      // Cargamos todo en paralelo para mayor velocidad
      const [pData, tData, eData, dData] = await Promise.all([
        api.getPqrs(),
        api.getTiposPqr(),
        api.getEstados(),
        api.getDepartamentos()
      ])
      
      pqrs = pData.resultado || []
      tipos = tData.resultado || tData // Manejo de diferentes formatos de API
      estados = eData.resultado || eData
      departamentos = dData.resultado || dData
    } catch (e) {
      showToast('Error al cargar datos del servidor', 'error')
    }
    loading = false
  }
)

  function openCreate() {
    form = defaultForm()
    selected = null
    view = 'form'
  }

  function openEdit(pqr) {
    form = { ...pqr } // Clonamos el objeto
    selected = pqr
    view = 'form'
  }

  async function savePqr() {
    // Validación básica
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Por favor completa los campos obligatorios', 'error');
      return;
    }

    saving = true
    try {
      // Construimos el payload exacto que pide tu API
      const payload = {
        "id_pqr": selected ? selected.id_pqr : 0, // 0 para nuevas
        "descripcion": form.descripcion,
        "fecha": selected ? selected.fecha : new Date().toISOString(), // Mantenemos fecha original si editamos
        "id_usuario": selected ? selected.id_usuario : ($currentUser?.id_usuario || 1), // Usuario actual o ID 1 de respaldo
        "id_tipo": parseInt(form.id_tipo),
        "id_estado": selected ? selected.id_estado : 1, // 1 suele ser 'Pendiente'
        "id_departamento": parseInt(form.id_departamento),
        "id_prioridad": selected ? selected.id_prioridad : 1 // 1 suele ser 'Baja'
      }

      if (selected) {
        await api.updatePqr(selected.id_pqr, payload)
        showToast('Solicitud actualizada con éxito')
      } else {
        await api.createPqr(payload)
        showToast('¡Tu PQR ha sido radicada correctamente!')
      }
      
      // Recargamos la lista y volvemos a la tabla
      const pData = await api.getPqrs()
      pqrs = pData.resultado || []
      view = 'list'
    } catch (e) {
      showToast('Error al conectar con el servidor', 'error')
    }
    saving = false
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg
    toastType = type
    setTimeout(() => toastMsg = '', 4000) // Desaparece en 4s
  }

  // Funciones helper para obtener los nombres (Labels) de los IDs
  function getLabelEstado(id) {
    return estados.find(e => e.id_estado == id)?.nombre || 'Pendiente'
  }

  function getLabelTipo(id) {
    return tipos.find(t => t.id_tipo == id)?.nombre || 'Petición'
  }

  function getLabelDepartamento(id) {
    return departamentos.find(d => d.id_departamento == id)?.nombre || 'Sistemas'
  }
</script>

<div class="module">
  {#if toastMsg}
    <div class="toast {toastType}" role="alert">
      {toastType === 'success' ? '✅' : '❌'} {toastMsg}
    </div>
  {/if}

  <header class="page-header">
    <div class="title-area">
      <h1>{view === 'list' ? (isAdmin ? 'Panel de Gestión PQRs' : 'Mis Solicitudes') : 'Radicar Nueva PQR'}</h1>
      <p class="subtitle">{view === 'list' ? 'Consulta el estado y evolución de tus trámites' : 'Describe tu caso detalladamente para recibir respuesta'}</p>
    </div>
    <div class="action-area">
      {#if view !== 'list'}
        <button class="btn-secondary" onclick={() => view = 'list'}>← Cancelar y Volver</button>
      {/if}
      {#if view === 'list' && !isAdmin}
        <button class="btn-primary" onclick={openCreate}>＋ Nueva Solicitud</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar card">
      <div class="search-group">
        <span class="search-icon">🔍</span>
        <input class="search-input" type="text" placeholder="Buscar por descripción..." bind:value={searchText} />
      </div>
      <div class="filter-group">
        <select class="filter-select" bind:value={filterEstado}>
          <option value="">Todos los estados</option>
          {#each estados as e}
            <option value={e.id_estado}>{e.nombre}</option>
          {/each}
        </select>
      </div>
    </div>

    {#if loading}
      <div class="loading-state">
        <span class="spinner-lg"></span>
        <p>Cargando información del servidor...</p>
      </div>
    {:else}
      <div class="table-wrap card">
        <table>
          <thead>
            <tr>
              <th width="80">ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              <th>Departamento</th>
              <th>Estado</th>
              <th>Fecha Radicación</th>
              <th width="80">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr class="clickable-row">
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td class="desc-cell" title={pqr.descripcion}>
                    {pqr.descripcion?.slice(0, 50)}{pqr.descripcion?.length > 50 ? '...' : ''}
                </td>
                <td><span class="type-pill t{pqr.id_tipo}">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td><span class="dep-text">{getLabelDepartamento(pqr.id_departamento)}</span></td>
                <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                <td class="date-cell">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td>
                  <button class="icon-btn edit-btn" onclick={() => openEdit(pqr)} title="Ver/Editar detalle">
                    ✎
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
        {#if filtered.length === 0}
            <div class="empty-table">
                <p>No se encontraron registros {searchText ? 'para tu búsqueda' : ''}.</p>
            </div>
        {/if}
      </div>
    {/if}

  {:else if view === 'form'}
    <div class="form-container container-sm">
      <div class="form-card card">
        <h2 class="form-title">{selected ? 'Detalle de la Solicitud' : 'Formulario de Radicación'}</h2>
        <div class="form-grid">
          <div class="field full-width">
            <label for="desc">Descripción detallada del caso <span class="req">*</span></label>
            <textarea id="desc" bind:value={form.descripcion} rows="6" placeholder="Ej: No tengo acceso a la plataforma virtual de inglés, me sale error de credenciales..."></textarea>
          </div>
          <div class="field">
            <label for="tipo">Tipo de Solicitud <span class="req">*</span></label>
            <select id="tipo" bind:value={form.id_tipo}>
              <option value="">Seleccionar...</option>
              {#each tipos as t}
                <option value={t.id_tipo}>{t.nombre}</option>
              {/each}
            </select>
          </div>
          <div class="field">
            <label for="dep">Departamento Destino <span class="req">*</span></label>
            <select id="dep" bind:value={form.id_departamento}>
              <option value="">Seleccionar área...</option>
              {#each departamentos as d}
                <option value={d.id_departamento}>{d.nombre}</option>
              {/each}
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={savePqr} disabled={saving}>
            {#if saving}<span class="spinner-sm"></span>{/if}
            {selected ? 'Actualizar Cambios' : '🚀 Radicar Solicitud'}
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  /* --- REGLAS GLOBALES Y VARIABLES --- */
  :root {
    --primary: #2563eb; /* Azul moderno */
    --primary-hover: #1d4ed8;
    --bg: #f8fafc; /* Gris muy suave Notion-like */
    --text: #1f2937;
    --text-muted: #6b7280;
    --border: #e5e7eb;
    --card-bg: #ffffff;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    --radius: 16px;
  }

  /* --- LAYOUT DEL MÓDULO --- */
  .module {
    padding: 40px;
    max-width: 1400px;
    margin: 0 auto;
    font-family: 'Inter', system-ui, sans-serif; /* Fuente limpia moderna */
    color: var(--text);
  }

  /* --- CABECERA DE PÁGINA --- */
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }
  h1 { font-size: 32px; font-weight: 800; color: #111827; margin: 0; letter-spacing: -0.03em; }
  .subtitle { color: var(--text-muted); font-size: 15px; margin: 4px 0 0; }

  /* --- COMPONENTES GENÉRICOS --- */
  .card {
    background: var(--card-bg);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
  }

  .container-sm { max-width: 800px; margin: 0 auto; }

  /* --- TOOLBAR (BUSCADOR Y FILTROS) --- */
  .toolbar {
    display: flex;
    gap: 16px;
    padding: 16px;
    margin-bottom: 24px;
    align-items: center;
  }
  .search-group { position: relative; flex: 1; }
  .search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
  .search-input {
    width: 100%;
    padding: 12px 12px 12px 40px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: #fdfdfd;
    transition: all 0.2s;
  }
  .search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); outline: none; }
  .filter-select { padding: 12px; border-radius: 12px; border: 1px solid var(--border); background: #fdfdfd; cursor: pointer; }

  /* --- TABLA RENOVADA --- */
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f9fafb; padding: 16px 20px; text-align: left; color: var(--text-muted); font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border); }
  td { padding: 16px 20px; border-bottom: 1px solid #f3f4f6; transition: background 0.2s; }
  .clickable-row:hover td { background: #f9fafb; cursor: pointer; }

  .id-badge { background: #f3f4f6; color: #4b5563; font-weight: 700; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-family: monospace; }
  .desc-cell { color: #374151; font-weight: 500; }
  .dep-text { color: var(--text-muted); font-weight: 600; }
  .date-cell { color: var(--text-muted); }
  .empty-table { text-align: center; padding: 40px; color: var(--text-muted); }

  /* --- ESTILOS DE PILLS/ETIQUETAS (DINÁMICOS) --- */
  .type-pill { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; background: #eff6ff; color: #2563eb; }
  /* Puedes añadir colores específicos por ID de tipo ej: .t1 { bg:..., color:... } */

  .status-badge { padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; }
  .s1 { background: #fef3c7; color: #92400e; } /* Pendiente: Amarillo Notion */
  .s2 { background: #dcfce7; color: #166534; } /* Resuelto: Verde Notion */
  .s3 { background: #dbeafe; color: #1e40af; } /* En Proceso: Azul Notion */
  .s4 { background: #fee2e2; color: #991b1b; } /* Rechazado: Rojo Notion */

  /* --- FORMULARIO Y INPUTS --- */
  .form-container { margin-top: 20px; }
  .form-card { padding: 40px; }
  .form-title { font-size: 24px; font-weight: 800; margin-bottom: 32px; border-bottom: 2px solid var(--border); padding-bottom: 16px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .field { display: flex; flex-direction: column; gap: 8px; }
  .field.full-width { grid-column: 1 / -1; }
  label { font-size: 14px; font-weight: 600; color: #374151; }
  .req { color: #ef4444; }
  textarea, select { width: 100%; padding: 14px; border-radius: 12px; border: 1px solid var(--border); background: #fdfdfd; transition: 0.2s; }
  textarea:focus, select:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); outline: none; }
  textarea { resize: vertical; line-height: 1.6; }

  /* --- BOTONES --- */
  button { border: none; cursor: pointer; transition: all 0.2s; font-weight: 600; font-family: inherit; }
  .btn-primary { background: var(--primary); color: white; padding: 14px 28px; border-radius: 12px; font-size: 15px; box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2); }
  .btn-primary:hover:not(:disabled) { background: var(--primary-hover); transform: translateY(-1px); box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3); }
  .btn-primary:disabled { opacity: 0.7; cursor: not-allowed; }
  .btn-secondary { background: #f3f4f6; color: #4b5563; padding: 14px 24px; border-radius: 12px; font-size: 15px; }
  .btn-secondary:hover { background: #e5e7eb; }
  .form-actions { margin-top: 40px; display: flex; gap: 12px; justify-content: flex-end; border-top: 1px solid var(--border); padding-top: 24px; }

  /* --- ICONOS DE ACCIONES --- */
  .icon-btn { background: none; font-size: 18px; padding: 6px; border-radius: 8px; opacity: 0.6; }
  .icon-btn:hover { background: #f3f4f6; opacity: 1; }
  .edit-btn { color: var(--primary); }

  /* --- UTILS (Spinners, Toasts, etc) --- */
  .toast { position: fixed; top: 20px; right: 20px; padding: 16px 24px; border-radius: 12px; color: white; font-weight: 600; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); z-index: 1000; animation: slideIn 0.3s ease; }
  .toast.success { background: #059669; }
  .toast.error { background: #dc2626; }
  @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }

  .loading-state { text-align: center; padding: 60px; color: var(--text-muted); }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f3f4f6; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 0 auto 16px; }
  .spinner-sm { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; display: inline-block; margin-right: 8px; vertical-align: middle; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* --- RESPONSIVE BÁSICO --- */
  @media (max-width: 768px) {
    .module { padding: 20px; }
    .page-header { flex-direction: column; align-items: flex-start; gap: 16px; }
    .toolbar { flex-direction: column; }
    .form-grid { grid-template-columns: 1fr; }
    .form-card { padding: 20px; }
  }
</style>