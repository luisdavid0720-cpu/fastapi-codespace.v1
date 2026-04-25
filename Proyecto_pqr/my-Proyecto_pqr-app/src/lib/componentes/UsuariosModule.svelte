<script>
  import { onMount } from 'svelte'
  import { api } from '../api.js'
  import Avatar    from './Avatar.svelte'
  import Badge     from './Badge.svelte'
  import FormField from './FormField.svelte'
  import Modal     from './Modal.svelte'
 
  let usuarios  = $state([])
  let roles     = $state([])
  let loading   = $state(true)
  let view      = $state('list')
  let selected  = $state(null)
  let saving    = $state(false)
  let toastMsg  = $state('')
  let toastType = $state('success')
  let searchText = $state('')
  let sortCol    = $state('id_usuario')
  let sortAsc    = $state(true)
  let currentPage = $state(1)
  const rowsPerPage = 10
 
  // Modal de confirmación para eliminar
  let modalEliminarAbierto = $state(false)
  let usuarioAEliminar = $state(null)
 
  // Variables reactivas para FormField
  let formNombre   = $state('')
  let formCedula   = $state('')
  let formCorreo   = $state('')
  let formIdRol    = $state('')
  let formCarrera  = $state('')
  let formCelular  = $state('')
  let formSemestre = $state('')
 
  function defaultForm() {
    formNombre   = ''
    formCedula   = ''
    formCorreo   = ''
    formIdRol    = ''
    formCarrera  = ''
    formCelular  = ''
    formSemestre = ''
  }
 
  let filtered = $derived(usuarios.filter(u =>
    !searchText ||
    u.nombre?.toLowerCase().includes(searchText.toLowerCase()) ||
    u.cedula?.includes(searchText) ||
    u.correo?.toLowerCase().includes(searchText.toLowerCase())
  ))
 
  let sorted = $derived([...filtered].sort((a, b) => {
    const va = a[sortCol] ?? ''
    const vb = b[sortCol] ?? ''
    if (va < vb) return sortAsc ? -1 : 1
    if (va > vb) return sortAsc ? 1 : -1
    return 0
  }))
 
  let totalPages = $derived(Math.max(1, Math.ceil(sorted.length / rowsPerPage)))
  let rows = $derived(sorted.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage))
 
  function setSort(col) {
    if (sortCol === col) sortAsc = !sortAsc
    else { sortCol = col; sortAsc = true }
    currentPage = 1
  }
 
  function sortIcon(col) {
    if (sortCol !== col) return '↕'
    return sortAsc ? '↑' : '↓'
  }
 
  onMount(async () => {
    loading = true
    try {
      const [uData, rData] = await Promise.allSettled([api.getUsuarios(), api.getRoles()])
      usuarios = uData.value?.resultado || uData.value || []
      roles    = rData.value?.resultado || rData.value || []
    } catch(e) { console.error(e) }
    finally { loading = false }
  })
 
  function getRolLabel(id) {
    if (Array.isArray(roles) && roles.length > 0) {
      const r = roles.find(rol => rol.id_rol == id)
      if (r) return r.nombre || r.nombre_rol
    }
    const dic = { 1:'Estudiante', 2:'Docente', 3:'Administrador', 4:'Coordinador', 5:'Secretaria', 6:'Soporte', 7:'Decano', 8:'Director', 9:'Investigador', 10:'Monitor', 11:'Tutor', 12:'Analista' }
    return dic[id] || `Rol ${id}`
  }
 
  // Mapea id_rol a color Badge: 1=s3(verde), 2=s2(azul), 3=s4(rojo), 4=s1(amarillo), resto=s5
  function getRolBadgeId(id) {
    const map = { 1: 3, 2: 2, 3: 4, 4: 1, 5: 5 }
    return map[id] || 5
  }
 
  function openCreate() { 
    selected = null;
    defaultForm(); 
    view = 'form'
  }

  function volverALista() {
    selected = null;
    defaultForm();
    view = 'list'
  }


  function openEdit(u) {
    selected    = u
    formNombre  = u.nombre   || ''
    formCedula  = u.cedula   || ''
    formCorreo  = u.correo   || ''
    formIdRol   = u.id_rol   || ''
    formCarrera = u.carrera  || ''
    formCelular = u.celular  || ''
    formSemestre = u.semestre || ''
    view = 'form'
  }
 
  async function saveUsuario() {
    if (!formNombre || !formCedula || !formCorreo) {
      showToast('⚠️ Completa los campos obligatorios', 'error'); return
    }
    saving = true
    try {
      const payload = {
        nombre: formNombre, cedula: formCedula, correo: formCorreo,
        id_rol: parseInt(formIdRol), carrera: formCarrera,
        celular: formCelular,
        semestre: formSemestre ? parseInt(formSemestre) : null
      }
      if (selected) await api.updateUsuario(selected.id_usuario, payload)
      else          await api.createUsuario(payload)
      const res = await api.getUsuarios()
      usuarios = res.resultado || res || []
      view = 'list'
      showToast('✅ Operación exitosa')
    } catch(e) { showToast('❌ Error al guardar', 'error') }
    finally { saving = false }
  }
 
  function pedirEliminar(u) {
    usuarioAEliminar = u
    modalEliminarAbierto = true
  }
 
  async function deleteUsuario() {
    if (!usuarioAEliminar) return
    try {
      await api.deleteUsuario(usuarioAEliminar.id_usuario)
      usuarios = usuarios.filter(u => u.id_usuario !== usuarioAEliminar.id_usuario)
      showToast('🗑️ Usuario eliminado')
      usuarioAEliminar = null
    } catch(e) { showToast('❌ Error al eliminar', 'error') }
  }
 
  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3000)
  }
</script>
 
<!-- Modal de confirmación para eliminar usuario -->
<Modal
  bind:abierto={modalEliminarAbierto}
  titulo="¿Eliminar usuario?"
  mensaje="Se eliminará a {usuarioAEliminar?.nombre}. Esta acción no se puede deshacer."
  txtConfirm="Sí, eliminar"
  txtCancel="Cancelar"
  peligroso={true}
  onconfirm={deleteUsuario}
/>
 
<div class="module">
  {#if toastMsg}<div class="toast {toastType}">{toastMsg}</div>{/if}
 
  <header class="page-header">
    <div class="header-info">
      <h1>{view === 'list' ? 'Gestión de Personal' : (selected ? 'Editar Usuario' : 'Nuevo Usuario')}</h1>
      <p class="subtitle">Directorio institucional de usuarios y roles</p>
    </div>
    <div class="header-actions">
      {#if view === 'list'}
        <button class="btn-primary" onclick={openCreate}>＋ Registrar Usuario</button>
      {:else}
        <button class="btn-back" onclick={volverALista}>← Volver</button>      {/if}
    </div>
  </header>
 
  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-container">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <input class="modern-input" type="text" placeholder="Buscar por nombre, cédula o correo..."
          bind:value={searchText} oninput={() => currentPage = 1} />
      </div>
    </div>
 
    <div class="results-count">
      {sorted.length} {sorted.length === 1 ? 'usuario encontrado' : 'usuarios encontrados'}
    </div>
 
    {#if loading}
      <div class="loader-wrap"><p>Sincronizando...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th onclick={() => setSort('id_usuario')} class="sortable">ID {sortIcon('id_usuario')}</th>
              <th onclick={() => setSort('nombre')} class="sortable">Usuario {sortIcon('nombre')}</th>
              <th onclick={() => setSort('cedula')} class="sortable">Identificación {sortIcon('cedula')}</th>
              <th onclick={() => setSort('correo')} class="sortable">Correo {sortIcon('correo')}</th>
              <th onclick={() => setSort('id_rol')} class="sortable">Rol {sortIcon('id_rol')}</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each rows as u (u.id_usuario)}
              <tr>
                <td><span class="id-tag">#{u.id_usuario}</span></td>
                <td>
                  <!-- Avatar reemplaza el div.avatar + div.user-info manuales -->
                  <Avatar
                    nombre={u.nombre}
                    size="md"
                    showName={true}
                    rol={u.carrera || 'CUL'}
                  />
                </td>
                <td class="mono">{u.cedula}</td>
                <td class="text-muted">{u.correo}</td>
                <td>
                  <!-- Badge reemplaza el span.role-badge manual -->
                  <Badge texto={getRolLabel(u.id_rol)} id={getRolBadgeId(u.id_rol)} />
                </td>
                <td class="text-center actions-cell">
                  <button class="action-btn edit-btn" onclick={() => openEdit(u)} title="Editar">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                  </button>
                  <!-- Modal reemplaza el confirm() del navegador -->
                  <button class="action-btn delete-btn" onclick={() => pedirEliminar(u)} title="Eliminar">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                      <path d="M10 11v6M14 11v6"/>
                      <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                    </svg>
                  </button>
                </td>
              </tr>
            {/each}
            {#if rows.length === 0}
              <tr><td colspan="6" class="empty-row">No se encontraron usuarios</td></tr>
            {/if}
          </tbody>
        </table>
 
        <div class="pagination">
          <button class="page-btn" onclick={() => currentPage = 1} disabled={currentPage === 1}>««</button>
          <button class="page-btn" onclick={() => currentPage--} disabled={currentPage === 1}>‹ Anterior</button>
          <span class="page-info">Página <strong>{currentPage}</strong> de <strong>{totalPages}</strong></span>
          <button class="page-btn" onclick={() => currentPage++} disabled={currentPage === totalPages}>Siguiente ›</button>
          <button class="page-btn" onclick={() => currentPage = totalPages} disabled={currentPage === totalPages}>»»</button>
        </div>
      </div>
    {/if}
 
  {:else}
    <div class="center-container">
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">{selected ? `Editando a ${selected.nombre}` : 'Registrar nuevo usuario'}</h2>
 
          <!-- FormField reemplaza todos los input/select manuales -->
          <FormField
            label="Nombre Completo"
            tipo="text"
            bind:valor={formNombre}
            placeholder="Ej: Juan Pérez García"
            required={true}
          />
 
          <div class="field-group">
            <FormField
              label="Cédula"
              tipo="text"
              bind:valor={formCedula}
              placeholder="100000001"
              required={true}
            />
            <FormField
              label="Correo"
              tipo="email"
              bind:valor={formCorreo}
              placeholder="usuario@cul.edu.co"
              required={true}
            />
          </div>
 
          <div class="field-group">
            <FormField
              label="Rol"
              tipo="select"
              bind:valor={formIdRol}
              placeholder="Seleccionar..."
              opciones={roles.map(r => ({ value: r.id_rol, label: r.nombre || r.nombre_rol }))}
            />
            <FormField
              label="Carrera"
              tipo="text"
              bind:valor={formCarrera}
              placeholder="Ej: Ingeniería de Sistemas"
            />
          </div>
 
          <div class="field-group">
            <FormField
              label="Celular"
              tipo="text"
              bind:valor={formCelular}
              placeholder="3001234567"
            />
            <FormField
              label="Semestre"
              tipo="number"
              bind:valor={formSemestre}
              placeholder="1 – 10"
            />
          </div>
 
          <div class="form-actions">
            <button class="btn-cancel" onclick={volverALista}>Cancelar</button>
            <button class="btn-send" onclick={saveUsuario} disabled={saving}>
              {saving ? 'Guardando...' : (selected ? '💾 Guardar cambios' : '➕ Registrar usuario')}
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
 
<style>
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }
 
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -1px; }
  .subtitle { color: #64748b; font-size: 15px; margin: 4px 0 0; }
 
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37,99,235,0.2); font-family: inherit; }
  .btn-primary:hover { background: #1d4ed8; }
  .btn-back { background: white; border: 1.5px solid #e2e8f0; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; font-family: inherit; }
 
  .toolbar { margin-bottom: 12px; }
  .search-container { position: relative; max-width: 400px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
  .modern-input { width: 100%; padding: 11px 12px 11px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; font-size: 14px; outline: none; transition: 0.3s; background: white; font-family: inherit; box-sizing: border-box; }
  .modern-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,0.05); }
 
  .results-count { font-size: 13px; color: #94a3b8; font-weight: 500; margin-bottom: 16px; }
 
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 14px 16px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #f1f5f9; white-space: nowrap; }
  th.sortable { cursor: pointer; user-select: none; }
  th.sortable:hover { background: #f1f5f9; color: #2563eb; }
  td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; font-size: 13px; color: #334155; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafbff; }
  .empty-row { text-align: center; color: #94a3b8; padding: 40px !important; }
 
  .pagination { display: flex; align-items: center; justify-content: center; gap: 10px; padding: 16px; border-top: 1px solid #f1f5f9; }
  .page-btn { background: white; border: 1.5px solid #e2e8f0; padding: 8px 14px; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; color: #475569; transition: 0.2s; font-family: inherit; }
  .page-btn:hover:not(:disabled) { background: #2563eb; color: white; border-color: #2563eb; }
  .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .page-info { font-size: 13px; color: #64748b; padding: 0 8px; }
 
  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; font-size: 12px; }
  .mono { font-family: monospace; font-size: 13px; }
  .text-muted { color: #64748b; font-size: 12px; }
 
  .actions-cell { display: flex; align-items: center; justify-content: center; gap: 6px; }
  .action-btn { width: 32px; height: 32px; border: none; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
  .edit-btn   { background: #f0fdf4; color: #16a34a; }
  .edit-btn:hover   { background: #16a34a; color: white; transform: scale(1.1); }
  .delete-btn { background: #fef2f2; color: #dc2626; }
  .delete-btn:hover { background: #dc2626; color: white; transform: scale(1.1); }
 
  .center-container { display: flex; justify-content: center; padding: 20px 0 60px; }
  .card { background: white; width: 100%; max-width: 680px; border-radius: 32px; border: 1px solid #e2e8f0; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); overflow: hidden; }
  .form-padding { padding: 45px; }
  .card-title { font-size: 22px; font-weight: 800; color: #0f172a; margin: 0 0 28px; }
 
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 4px; }
 
  .form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 8px; }
  .btn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 14px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; font-family: inherit; font-size: 14px; }
  .btn-send { background: #2563eb; color: white; border: none; padding: 14px 28px; border-radius: 12px; font-weight: 700; cursor: pointer; font-family: inherit; font-size: 14px; transition: 0.2s; }
  .btn-send:hover { background: #1d4ed8; }
  .btn-send:disabled { opacity: 0.6; cursor: not-allowed; }
 
  .toast { position: fixed; bottom: 30px; right: 30px; background: #0f172a; color: white; padding: 16px 28px; border-radius: 16px; font-weight: 600; z-index: 100; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
  .toast.error { background: #dc2626; }
  .loader-wrap { padding: 60px; text-align: center; color: #94a3b8; }
  .animate-up { animation: slideUp 0.4s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
 
  @media (max-width: 768px) {
    .module { padding: 16px; }
    .page-header { flex-direction: column; gap: 12px; }
    h1 { font-size: 22px; }
    .search-container { max-width: 100%; }
    table { min-width: 650px; }
    th, td { padding: 10px 12px; font-size: 11px; }
    .form-padding { padding: 24px; }
    .field-group { grid-template-columns: 1fr; }
    .form-actions { flex-direction: column; }
    .pagination { flex-wrap: wrap; }
  }
</style>