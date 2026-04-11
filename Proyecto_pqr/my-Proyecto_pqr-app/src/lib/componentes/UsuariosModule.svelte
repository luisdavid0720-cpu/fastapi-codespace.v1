<script>
  import { onMount } from 'svelte'
  import { api } from '../api.js'
 
  let usuarios = $state([])
  let roles = $state([])
  let loading = $state(true)
  let view = $state('list')
  let selected = $state(null)
  let saving = $state(false)
  let toastMsg = $state('')
  let toastType = $state('success')
  let searchText = $state('')
 
  function defaultForm() {
    return { nombre: '', cedula: '', carrera: '', semestre: '', cargo: '', celular: '', correo: '', id_rol: '' }
  }
 
  let form = $state(defaultForm())
 
  let filtered = $derived(usuarios.filter(u =>
    !searchText ||
    u.nombre?.toLowerCase().includes(searchText.toLowerCase()) ||
    u.cedula?.includes(searchText) ||
    u.correo?.toLowerCase().includes(searchText.toLowerCase())
  ))
 
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
 
  function getInitials(nombre) {
    if (!nombre) return '?'
    const parts = nombre.trim().split(' ')
    return parts.length >= 2
      ? (parts[0][0] + parts[1][0]).toUpperCase()
      : parts[0][0].toUpperCase()
  }
 
  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(u)   { form = { ...u };    selected = u;    view = 'form' }
 
  async function saveUsuario() {
    if (!form.nombre || !form.cedula || !form.correo) {
      showToast('⚠️ Completa los campos obligatorios', 'error'); return
    }
    saving = true
    try {
      const payload = { ...form, id_rol: parseInt(form.id_rol), semestre: form.semestre ? parseInt(form.semestre) : null }
      if (selected) await api.updateUsuario(selected.id_usuario, payload)
      else          await api.createUsuario(payload)
      const res = await api.getUsuarios()
      usuarios = res.resultado || res || []
      view = 'list'
      showToast('✅ Operación exitosa')
    } catch(e) { showToast('❌ Error al guardar', 'error') }
    finally { saving = false }
  }
 
  async function deleteUsuario(id) {
    if (!confirm('¿Eliminar este usuario? Esta acción no se puede deshacer.')) return
    try {
      await api.deleteUsuario(id)
      usuarios = usuarios.filter(u => u.id_usuario !== id)
      showToast('🗑️ Usuario eliminado')
    } catch(e) { showToast('❌ Error al eliminar', 'error') }
  }
 
  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3000)
  }
</script>
 
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
        <button class="btn-back" onclick={() => view = 'list'}>← Volver</button>
      {/if}
    </div>
  </header>
 
  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-container">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <input class="modern-input" type="text" placeholder="Buscar por nombre, cédula o correo..." bind:value={searchText} />
      </div>
    </div>
 
    <div class="results-count">
      {filtered.length} {filtered.length === 1 ? 'usuario encontrado' : 'usuarios encontrados'}
    </div>
 
    {#if loading}
      <div class="loader-wrap"><p>Sincronizando...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Identificación</th>
              <th>Correo</th>
              <th>Rol</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as u (u.id_usuario)}
              <tr>
                <td><span class="id-tag">#{u.id_usuario}</span></td>
                <td>
                  <div class="user-cell">
                    <div class="avatar">{getInitials(u.nombre)}</div>
                    <div class="user-info">
                      <span class="user-name">{u.nombre}</span>
                      <span class="user-sub">{u.carrera || 'CUL'}</span>
                    </div>
                  </div>
                </td>
                <td class="mono">{u.cedula}</td>
                <td class="text-muted">{u.correo}</td>
                <td><span class="role-badge r{u.id_rol}">{getRolLabel(u.id_rol)}</span></td>
                <td class="text-center actions-cell">
                  <button class="action-btn edit-btn" onclick={() => openEdit(u)} title="Editar">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                  </button>
                  <button class="action-btn delete-btn" onclick={() => deleteUsuario(u.id_usuario)} title="Eliminar">
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
            {#if filtered.length === 0}
              <tr><td colspan="6" class="empty-row">No se encontraron usuarios</td></tr>
            {/if}
          </tbody>
        </table>
      </div>
    {/if}
 
  {:else}
    <div class="center-container">
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">{selected ? `Editando a ${selected.nombre}` : 'Registrar nuevo usuario'}</h2>
 
          <div class="field full">
            <label class="section-label">Nombre Completo *</label>
            <input type="text" bind:value={form.nombre} placeholder="Ej: Juan Pérez García" />
          </div>
 
          <div class="field-group">
            <div class="field">
              <label class="section-label">Cédula *</label>
              <input type="text" bind:value={form.cedula} placeholder="100000001" />
            </div>
            <div class="field">
              <label class="section-label">Correo *</label>
              <input type="email" bind:value={form.correo} placeholder="usuario@cul.edu.co" />
            </div>
          </div>
 
          <div class="field-group">
            <div class="field">
              <label class="section-label">Rol</label>
              <select bind:value={form.id_rol}>
                <option value="">Seleccionar...</option>
                {#each roles as r}
                  <option value={r.id_rol}>{r.nombre || r.nombre_rol}</option>
                {/each}
              </select>
            </div>
            <div class="field">
              <label class="section-label">Carrera</label>
              <input type="text" bind:value={form.carrera} placeholder="Ej: Ingeniería de Sistemas" />
            </div>
          </div>
 
          <div class="field-group">
            <div class="field">
              <label class="section-label">Celular</label>
              <input type="text" bind:value={form.celular} placeholder="3001234567" />
            </div>
            <div class="field">
              <label class="section-label">Semestre</label>
              <input type="number" bind:value={form.semestre} placeholder="1 – 10" min="1" max="10" />
            </div>
          </div>
 
          <div class="form-actions">
            <button class="btn-cancel" onclick={() => view = 'list'}>Cancelar</button>
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
 
  /* Header */
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -1px; }
  .subtitle { color: #64748b; font-size: 15px; margin: 4px 0 0; }
 
  /* Botones header */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37,99,235,0.2); font-family: inherit; }
  .btn-primary:hover { background: #1d4ed8; }
  .btn-back { background: white; border: 1.5px solid #e2e8f0; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; font-family: inherit; }
 
  /* Toolbar */
  .toolbar { margin-bottom: 12px; }
  .search-container { position: relative; max-width: 400px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
  .modern-input { width: 100%; padding: 11px 12px 11px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; font-size: 14px; outline: none; transition: 0.3s; background: white; font-family: inherit; box-sizing: border-box; }
  .modern-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,0.05); }
 
  .results-count { font-size: 13px; color: #94a3b8; font-weight: 500; margin-bottom: 16px; }
 
  /* Tabla */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 14px 16px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #f1f5f9; white-space: nowrap; }
  td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; font-size: 13px; color: #334155; }
  tr:last-child td { border-bottom: none; }
  .empty-row { text-align: center; color: #94a3b8; padding: 40px !important; }
 
  /* Celda usuario */
  .user-cell { display: flex; align-items: center; gap: 12px; }
  .avatar { width: 38px; height: 38px; border-radius: 10px; background: #eff6ff; color: #2563eb; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .user-info { display: flex; flex-direction: column; gap: 2px; }
  .user-name { font-weight: 600; color: #0f172a; font-size: 13px; }
  .user-sub { font-size: 11px; color: #94a3b8; }
  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; font-size: 12px; }
  .mono { font-family: monospace; font-size: 13px; }
  .text-muted { color: #64748b; font-size: 12px; }
 
  /* Role badges */
  .role-badge { padding: 5px 12px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; white-space: nowrap; }
  .r1 { background: #dcfce7; color: #166534; }
  .r2 { background: #dbeafe; color: #1e40af; }
  .r3 { background: #fee2e2; color: #991b1b; }
  .r4 { background: #fef3c7; color: #92400e; }
  .r5 { background: #f3e8ff; color: #6b21a8; }
  .r6 { background: #f1f5f9; color: #475569; }
  .r7 { background: #fff7ed; color: #c2410c; }
  .r8 { background: #ecfdf5; color: #065f46; }
 
  /* Botones acción */
  .actions-cell { display: flex; align-items: center; justify-content: center; gap: 6px; }
  .action-btn { width: 32px; height: 32px; border: none; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
  .edit-btn   { background: #f0fdf4; color: #16a34a; }
  .edit-btn:hover   { background: #16a34a; color: white; transform: scale(1.1); }
  .delete-btn { background: #fef2f2; color: #dc2626; }
  .delete-btn:hover { background: #dc2626; color: white; transform: scale(1.1); }
 
  /* Formulario */
  .center-container { display: flex; justify-content: center; padding: 20px 0 60px; }
  .card { background: white; width: 100%; max-width: 680px; border-radius: 32px; border: 1px solid #e2e8f0; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); overflow: hidden; }
  .form-padding { padding: 45px; }
  .card-title { font-size: 22px; font-weight: 800; color: #0f172a; margin: 0 0 28px; }
 
  .field { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
  .field.full { grid-column: 1 / -1; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .section-label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
 
  .field input, .field select {
    padding: 12px 16px; border-radius: 12px; border: 1.5px solid #e2e8f0;
    background: #fcfcfc; font-size: 14px; outline: none; font-family: inherit;
    transition: border-color 0.2s;
  }
  .field input:focus, .field select:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,0.05); }
 
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
  }
</style>