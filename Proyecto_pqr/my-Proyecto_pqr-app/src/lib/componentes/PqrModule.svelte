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

  // FILTRO DE SEGURIDAD: Usuario solo ve lo suyo (ID coincidente), Admin ve todo
  let filtered = $derived(pqrs.filter(p => {
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
    } catch(e) {
      console.error("Error al cargar datos:", e)
    }
    loading = false
  }

  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  
  // Cambiamos openEdit por openDetail para solo lectura
  function openDetail(pqr) { 
    selected = pqr; 
    view = 'detail'; 
  }

  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('Completa los campos obligatorios', 'error');
      return;
    }

    saving = true;
    try {
      const payload = {
        "id_pqr": 0,
        "descripcion": form.descripcion,
        "fecha": new Date().toISOString(),
        "id_usuario": parseInt($currentUser?.id_usuario) || 1,
        "id_tipo": parseInt(form.id_tipo),
        "id_estado": 1, 
        "id_departamento": parseInt(form.id_departamento),
        "id_prioridad": 1
      };

      const res = await api.createPqr(payload);
      if (res) {
        showToast('¡PQR radicada con éxito!');
        await loadAll();
        view = 'list';
      }
    } catch (error) {
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
      <h1>
        {#if view === 'list'}{isAdmin ? 'Gestión de PQRs' : 'Mis Solicitudes'}
        {:else if view === 'form'}Radicar Nueva PQR
        {:else}Resumen de Trámite{/if}
      </h1>
      <p class="subtitle">
        {#if view === 'list'}Consulta el historial de tus procesos institucionales
        {:else if view === 'form'}Describe tu solicitud detalladamente para darte respuesta
        {:else}Información detallada sobre tu radicado{/if}
      </p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}<button class="btn-secondary" onclick={() => view = 'list'}>← Volver a la lista</button>{/if}
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
              {#if isAdmin}<th>Estado</th>{/if}
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr class="clickable-row">
                <td><span class="id-badge">#{pqr.id_pqr}</span></td>
                <td class="desc-cell">{pqr.descripcion?.slice(0, 40)}...</td>
                <td><span class="chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                <td>{getLabelDep(pqr.id_departamento)}</td>
                {#if isAdmin}
                  <td><span class="status-badge s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                {/if}
                <td>{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td>
                  <button class="view-btn" onclick={() => openDetail(pqr)} title="Ver Resumen">👁</button>
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
            <label>Descripción detallada <span class="req">*</span></label>
            <textarea bind:value={form.descripcion} rows="5" placeholder="Explica tu caso aquí..."></textarea>
          </div>
          <div class="field">
            <label>Tipo de solicitud <span class="req">*</span></label>
            <select bind:value={form.id_tipo}>
              <option value="">Seleccionar...</option>
              {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
            </select>
          </div>
          <div class="field">
            <label>Departamento destino <span class="req">*</span></label>
            <select bind:value={form.id_departamento}>
              <option value="">Seleccionar área...</option>
              {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={savePqr} disabled={saving}>
            {saving ? 'Procesando...' : '🚀 Radicar Solicitud'}
          </button>
        </div>
      </div>
    </div>

  {:else if view === 'detail' && selected}
    <div class="form-container">
      <div class="detail-card">
        <header class="detail-header">
          <span class="id-tag">Radicado #{selected.id_pqr}</span>
          <span class="status-badge s{selected.id_estado}">{getLabelEstado(selected.id_estado)}</span>
        </header>
        
        <div class="detail-body">
          <div class="info-block">
            <label>Contenido de la PQR</label>
            <div class="text-box">{selected.descripcion}</div>
          </div>
          
          <div class="info-grid">
            <div class="info-item">
              <label>Categoría</label>
              <p>{getLabelTipo(selected.id_tipo)}</p>
            </div>
            <div class="info-item">
              <label>Área Responsable</label>
              <p>{getLabelDep(selected.id_departamento)}</p>
            </div>
            <div class="info-item">
              <label>Fecha de Envío</label>
              <p>{new Date(selected.fecha).toLocaleString('es-CO')}</p>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn-primary" onclick={() => view = 'list'}>Entendido</button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; max-width: 1200px; margin: 0 auto; }
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em; }
  .subtitle { color: #64748b; font-size: 15px; margin-top: 4px; }

  /* TABLA */
  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: #f8fafc; padding: 18px 20px; text-align: left; color: #64748b; font-weight: 800; border-bottom: 1px solid #f1f5f9; }
  td { padding: 18px 20px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  .id-badge { background: #f1f5f9; padding: 4px 8px; border-radius: 6px; font-weight: 700; color: #475569; font-size: 12px; }
  .chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 100px; font-size: 12px; font-weight: 700; }
  .status-badge { padding: 6px 14px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .s1 { background: #fef3c7; color: #92400e; } /* PENDIENTE */

  /* TOOLBAR */
  .toolbar { display: flex; gap: 16px; margin-bottom: 24px; }
  .search-wrap { position: relative; flex: 1; }
  .search-input { width: 100%; padding: 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
  .filter-select { padding: 12px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: white; cursor: pointer; }

  /* VISTA DETALLE (RESUMEN) */
  .detail-card { background: white; padding: 40px; border-radius: 28px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.08); width: 100%; max-width: 650px; border: 1px solid #e2e8f0; }
  .detail-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1.5px solid #f1f5f9; padding-bottom: 20px; }
  .id-tag { font-weight: 800; color: #0f172a; font-size: 20px; letter-spacing: -0.5px; }
  
  .info-block label, .info-item label { color: #94a3b8; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; display: block; }
  .text-box { background: #f8fafc; padding: 24px; border-radius: 16px; line-height: 1.7; color: #334155; border: 1px solid #edf2f7; font-size: 15px; }
  
  .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 24px; }
  .info-item p { font-weight: 700; color: #0f172a; margin: 0; font-size: 15px; }

  /* BOTONES */
  .view-btn { background: none; border: none; font-size: 18px; cursor: pointer; transition: transform 0.2s; padding: 5px; opacity: 0.7; }
  .view-btn:hover { transform: scale(1.2); opacity: 1; color: #2563eb; }
  .btn-primary { background: #2563eb; color: white; border: none; padding: 14px 28px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; }
  .btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); }
  .btn-secondary { background: #f1f5f9; border: none; padding: 14px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; color: #475569; }

  .form-container { display: flex; justify-content: center; padding-top: 20px; }
  .form-card { background: white; padding: 40px; border-radius: 28px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); width: 100%; max-width: 700px; border: 1px solid #e2e8f0; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block; }
  textarea, select { width: 100%; padding: 14px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #f8fafc; font-size: 14px; }
  .form-actions { margin-top: 32px; display: flex; gap: 12px; justify-content: flex-end; }

  .toast { position: fixed; top: 20px; right: 20px; padding: 14px 28px; border-radius: 12px; color: white; background: #0f172a; z-index: 1000; font-weight: 600; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>