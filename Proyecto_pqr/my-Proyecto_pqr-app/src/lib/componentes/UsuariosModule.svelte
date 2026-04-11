<script>
  import { onMount } from 'svelte'
  import { api } from '../api.js'

  // --- ESTADOS (Runes) ---
  let usuarios = $state([])
  let roles = $state([])
  let loading = $state(true)
  let view = $state('list') // 'list' | 'form'
  let selected = $state(null)
  let saving = $state(false)
  let searchText = $state('')
  let toastMsg = $state('')
  let toastType = $state('success')

  function defaultForm() {
    return { nombre: '', cedula: '', carrera: '', semestre: '', cargo: '', celular: '', correo: '', id_rol: '' }
  }
  let form = $state(defaultForm())

  // --- LÓGICA DE FILTRADO ---
  let filtered = $derived(usuarios.filter(u =>
    !searchText ||
    u.nombre?.toLowerCase().includes(searchText.toLowerCase()) ||
    u.cedula?.toString().includes(searchText) ||
    u.correo?.toLowerCase().includes(searchText.toLowerCase())
  ))

  // --- CARGA DE DATOS (PROTEGIDA) ---
  onMount(async () => {
    loading = true
    try {
      // Cargamos usuarios y roles. Si uno falla, el .catch evita que el otro se rompa
      const [uData, rData] = await Promise.allSettled([
        api.getUsuarios(),
        api.getRoles()
      ])
      
      usuarios = uData.value?.resultado || uData.value || []
      roles = rData.value?.resultado || rData.value || []
      
    } catch(e) {
      console.error("Error en la carga inicial:", e)
    } finally {
      loading = false // SE EJECUTA SIEMPRE para quitar el spinner
    }
  })

  // --- NAVEGACIÓN ---
  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  
  function openEdit(u) { 
    form = { ...u }
    selected = u
    view = 'form' 
  }

  // --- ACCIONES API ---
  async function saveUsuario() {
    if (!form.nombre || !form.cedula || !form.correo) {
      showToast('⚠️ Completa nombre, cédula y correo', 'error'); return
    }
    saving = true
    try {
      const payload = { 
        ...form, 
        semestre: form.semestre ? parseInt(form.semestre) : null, 
        id_rol: form.id_rol ? parseInt(form.id_rol) : null 
      }
      
      if (selected) {
        await api.updateUsuario(selected.id_usuario, payload)
        showToast('✅ Usuario actualizado')
      } else {
        await api.createUsuario(payload)
        showToast('✅ Usuario creado exitosamente')
      }
      
      // Recarga de lista
      const res = await api.getUsuarios()
      usuarios = res.resultado || res || []
      view = 'list'
    } catch(e) { 
      showToast('❌ Error: ' + e.message, 'error') 
    } finally {
      saving = false
    }
  }

  async function deleteUsuario(id) {
    if (!confirm('🚨 ¿Estás seguro de eliminar este usuario?')) return
    try {
      await api.deleteUsuario(id)
      usuarios = usuarios.filter(u => u.id_usuario !== id)
      showToast('🗑️ Usuario eliminado')
    } catch(e) { 
      showToast('❌ Error al eliminar', 'error') 
    }
  }

  // Mapeo dinámico de Roles con protección contra errores
  function getRolLabel(id) {
    if (!Array.isArray(roles) || roles.length === 0) {
      return id == 1 ? 'ADMINISTRADOR' : id == 2 ? 'ESTUDIANTE' : `ROL ${id}`
    }
    const r = roles.find(rol => rol.id_rol == id)
    return r?.nombre || r?.nombre_rol || (id == 1 ? 'ADMINISTRADOR' : 'ESTUDIANTE')
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3500)
  }
</script>

<div class="module">
  {#if toastMsg}<div class="toast {toastType}">{toastMsg}</div>{/if}

  <header class="page-header">
    <div class="header-info">
      <h1>{view === 'list' ? 'Gestión de Personal' : (selected ? 'Editar Usuario' : 'Nuevo Registro')}</h1>
      <p class="subtitle">Directorio de usuarios y roles del sistema</p>
    </div>
    <div class="header-actions">
      {#if view === 'list'}
        <button class="btn-primary" onclick={openCreate}>＋ Registrar Usuario</button>
      {:else}
        <button class="btn-secondary" onclick={() => view = 'list'}>← Volver a la lista</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input class="search-input" type="text" placeholder="Buscar por nombre, cédula o correo..." bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Sincronizando con el servidor...</p></div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Perfil / Usuario</th>
              <th>Identificación</th>
              <th>Correo Institucional</th>
              <th>Rol</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as u (u.id_usuario)}
              <tr>
                <td><span class="id-tag">#{u.id_usuario}</span></td>
                <td>
                  <div class="user-cell">
                    <div class="avatar-sm">{u.nombre?.charAt(0)?.toUpperCase() || '?'}</div>
                    <div class="name-info">
                      <p class="user-name">{u.nombre}</p>
                      <p class="user-sub">{u.carrera || 'CUL - Administrativo'}</p>
                    </div>
                  </div>
                </td>
                <td class="mono">{u.cedula}</td>
                <td class="email">{u.correo}</td>
                <td><span class="role-badge r{u.id_rol}">{getRolLabel(u.id_rol)}</span></td>
                <td class="text-right">
                  <div class="row-actions">
                    <button class="icon-btn edit" onclick={() => openEdit(u)} title="Editar">✎</button>
                    <button class="icon-btn delete" onclick={() => deleteUsuario(u.id_usuario)} title="Eliminar">✕</button>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      <p class="table-count">Mostrando {filtered.length} de {usuarios.length} registros</p>
    {/if}

  {:else}
    <div class="form-container">
      <div class="form-card animate-up">
        <h2 class="form-title">{selected ? 'Actualizar Información' : 'Datos del Nuevo Usuario'}</h2>
        <div class="form-grid">
          <div class="field full"><label>Nombre Completo *</label><input type="text" bind:value={form.nombre} /></div>
          <div class="field"><label>Cédula / ID *</label><input type="text" bind:value={form.cedula} /></div>
          <div class="field"><label>Correo Electrónico *</label><input type="email" bind:value={form.correo} /></div>
          <div class="field"><label>Celular</label><input type="text" bind:value={form.celular} /></div>
          <div class="field">
            <label>Rol Asignado</label>
            <select bind:value={form.id_rol}>
              <option value="">Seleccionar...</option>
              {#each roles as r}<option value={r.id_rol}>{r.nombre || r.nombre_rol}</option>{/each}
              {#if roles.length === 0}
                <option value="1">Administrador</option>
                <option value="2">Estudiante</option>
              {/if}
            </select>
          </div>
          <div class="field"><label>Carrera / Programa</label><input type="text" bind:value={form.carrera} /></div>
          <div class="field"><label>Semestre</label><input type="number" bind:value={form.semestre} min="1" max="12" /></div>
          <div class="field full"><label>Cargo Institucional</label><input type="text" bind:value={form.cargo} placeholder="Docente, Analista, etc." /></div>
        </div>
        <div class="form-actions-row">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={saveUsuario} disabled={saving}>
            {saving ? 'Procesando...' : (selected ? 'Guardar Cambios' : 'Registrar en Sistema')}
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -1px; }
  .subtitle { color: #64748b; font-size: 14px; }

  /* TOOLBAR */
  .toolbar { margin-bottom: 25px; }
  .search-wrap { position: relative; max-width: 450px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
  .search-input { width: 100%; padding: 12px 12px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; background: white; transition: 0.3s; }
  .search-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.05); }

  /* TABLA */
  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; letter-spacing: 0.5px; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: #334155; }
  
  .user-cell { display: flex; align-items: center; gap: 12px; }
  .avatar-sm { width: 36px; height: 36px; border-radius: 10px; background: #eff6ff; color: #2563eb; display: flex; align-items: center; justify-content: center; font-weight: 800; border: 1px solid #dbeafe; }
  .user-name { font-weight: 700; color: #1e293b; margin: 0; }
  .user-sub { font-size: 11px; color: #94a3b8; }
  
  /* ROLES */
  .role-badge { padding: 6px 12px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .r1 { background: #fee2e2; color: #991b1b; } 
  .r2 { background: #dcfce7; color: #166534; }
  .role-badge:not(.r1):not(.r2) { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

  /* ACCIONES */
  .row-actions { display: flex; gap: 10px; justify-content: flex-end; }
  .icon-btn { background: none; border: 1.5px solid #e2e8f0; font-size: 16px; cursor: pointer; transition: 0.2s; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }
  .edit { color: #fbb03b; }
  .edit:hover { background: #fef3c7; border-color: #fbb03b; }
  .delete { color: #ef4444; }
  .delete:hover { background: #fee2e2; border-color: #ef4444; }

  /* FORM CARDS */
  .form-container { display: flex; justify-content: center; padding-top: 20px; }
  .form-card { background: white; padding: 45px; border-radius: 32px; border: 1px solid #e2e8f0; width: 100%; max-width: 750px; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); }
  .form-title { font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 30px; border-bottom: 2.5px solid #f1f5f9; padding-bottom: 15px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .field { display: flex; flex-direction: column; gap: 8px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  input, select { padding: 13px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #fcfcfc; font-size: 14px; outline: none; }
  input:focus, select:focus { border-color: #2563eb; background: white; }
  .form-actions-row { margin-top: 35px; display: flex; gap: 15px; justify-content: flex-end; }

  /* BOTONES */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
  .btn-primary:hover:not(:disabled) { transform: translateY(-2px); background: #1d4ed8; }
  .btn-secondary { background: #f1f5f9; color: #475569; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }

  /* UTILS */
  .toast { position: fixed; bottom: 30px; right: 30px; padding: 16px 28px; border-radius: 16px; color: white; background: #0f172a; font-weight: 600; z-index: 1000; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
  .toast.error { background: #ef4444; }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .text-right { text-align: right; }
  .table-count { text-align: right; font-size: 12px; color: #94a3b8; margin-top: 15px; }
  .animate-up { animation: slideUp 0.4s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
</style>