<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  // Variables de estado
  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'form' | 'detail'
  let selected = $state(null)
  let saving = $state(false)
  let toastMsg = $state('')
  let toastType = $state('success')
  let searchText = $state('')
  let filterEstado = $state('')

  // Catálogos
  let tipos = $state([]), estados = $state([]), departamentos = $state([]), prioridades = $state([])
  
  // Seguridad: Rol 1 es Admin
  let isAdmin = $derived($currentUser?.id_rol === 1)

  // Estructura inicial del formulario
  function defaultForm() {
    return {
      descripcion: '',
      id_tipo: '', 
      id_departamento: '', 
    }
  }

  let form = $state(defaultForm())

  // FILTRO DE SEGURIDAD: Usuario solo ve lo suyo, Admin ve todo
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
      // Cargamos los resultados de la API
      pqrs = p.value?.resultado || []
      tipos = t.value || []
      estados = e.value || []
      departamentos = d.value || []
      prioridades = pr.value || []
    } catch(e) {
      console.error("Error al cargar datos:", e)
    }
    loading = false
  }

  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(pqr) { form = { ...pqr }; selected = pqr; view = 'form' }

  // FUNCIÓN DE GUARDADO (Paso a Paso corregido)
  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Por favor, completa los campos obligatorios (*)', 'error');
      return;
    }

    saving = true;
    try {
      // PAYLOAD IDÉNTICO AL QUE FUNCIONÓ EN TU PRUEBA DE API
      const payload = {
        "id_pqr": selected ? selected.id_pqr : 0,
        "descripcion": form.descripcion,
        "fecha": new Date().toISOString(), // Formato ISO que pide tu API
        "id_usuario": parseInt($currentUser?.id_usuario) || 1,
        "id_tipo": parseInt(form.id_tipo),
        "id_estado": 1, // Por defecto: PENDIENTE
        "id_departamento": parseInt(form.id_departamento),
        "id_prioridad": 1 // Por defecto: BAJA
      };

      let res;
      if (selected) {
        res = await api.updatePqr(selected.id_pqr, payload);
        showToast('Solicitud actualizada');
      } else {
        res = await api.createPqr(payload);
        showToast('¡PQR radicada con éxito!');
      }

      await loadAll();
      view = 'list';
    } catch (error) {
      console.error("Error técnico:", error);
      showToast('Error de conexión con el servidor', 'error');
    } finally {
      saving = false;
    }
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3500)
  }

  // Helpers para etiquetas
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
      <h1>{view === 'list' ? (isAdmin ? 'Gestión de PQRs' : 'Mis Solicitudes') : 'Radicar Nueva PQR'}</h1>
      <p class="subtitle">{view === 'list' ? 'Consulta el estado de tus trámites' : 'Describe tu solicitud detalladamente'}</p>
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
      <select class="filter-select" bind:value={filterEstado}>
        <option value="">Todos los estados</option>
        {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
      </select>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Cargando información...</p></div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Tipo</th>
              <th>Departamento</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr class="clickable-row">
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td class="desc-cell">{pqr.descripcion?.slice(0, 50)}...</td>
                <td><span class="chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td>{getLabelDep(pqr.id_departamento)}</td>
                <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                <td>{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td>
                  <button class="icon-btn" onclick={() => openEdit(pqr)}>✎</button>
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
            <label>Descripción del caso <span class="req">*</span></label>
            <textarea bind:value={form.descripcion} rows="4" placeholder="Ej: No tengo acceso al aula virtual..."></textarea>
          </div>
          <div class="field">
            <label>Tipo <span class="req">*</span></label>
            <select bind:value={form.id_tipo}>
              <option value="">Seleccionar...</option>
              {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
            </select>
          </div>
          <div class="field">
            <label>Departamento <span class="req">*</span></label>
            <select bind:value={form.id_departamento}>
              <option value="">Seleccionar departamento...</option>
              {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={savePqr} disabled={saving}>
            {saving ? 'Guardando...' : '🚀 Enviar Solicitud'}
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; max-width: 1200px; margin: 0 auto; }
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em; }
  .subtitle { color: #64748b; font-size: 15px; }

  .toolbar { display: flex; gap: 16px; margin-bottom: 24px; }
  .search-wrap { position: relative; flex: 1; }
  .search-input { width: 100%; padding: 12px 12px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.5; }
  .filter-select { padding: 12px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: white; }

  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; color: #64748b; font-weight: 800; border-bottom: 1px solid #f1f5f9; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; }

  .id-badge { background: #f1f5f9; padding: 4px 8px; border-radius: 6px; font-weight: 700; color: #475569; }
  .chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 100px; font-size: 12px; font-weight: 700; }
  .status-badge { padding: 6px 14px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; } /* PENDIENTE */

  .form-card { background: white; padding: 40px; border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); width: 100%; max-width: 700px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block; }
  textarea, select { width: 100%; padding: 14px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #f8fafc; }

  .btn-primary { background: #2563eb; color: white; border: none; padding: 14px 28px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .btn-secondary { background: #f1f5f9; border: none; padding: 14px 24px; border-radius: 12px; font-weight: 600; cursor: pointer; }
  .form-actions { margin-top: 32px; display: flex; gap: 12px; justify-content: flex-end; }

  .toast { position: fixed; top: 20px; right: 20px; padding: 12px 24px; border-radius: 12px; color: white; background: #1e293b; z-index: 1000; font-weight: 600; }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>