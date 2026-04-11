<script>
  import { onMount } from 'svelte'
  import { api } from '../api.js'

<<<<<<< HEAD
  // --- ESTADOS (Svelte 5 Runes) ---
=======
  // --- ESTADOS ---
>>>>>>> 53d3423 (cambios en usuario)
  let usuarios = $state([])
  let roles = $state([])
  let loading = $state(true)
  let view = $state('list') 
  let selected = $state(null)
  let saving = $state(false)
  let toastMsg = $state('')
<<<<<<< HEAD
  let toastType = $state('success')
  let searchText = $state('')
=======
>>>>>>> 53d3423 (cambios en usuario)

  function defaultForm() {
    return { nombre: '', cedula: '', carrera: '', semestre: '', cargo: '', celular: '', correo: '', id_rol: '' }
  }

  let form = $state(defaultForm())

<<<<<<< HEAD
  // --- LÓGICA FILTRADO ---
=======
  // --- FILTRADO ---
>>>>>>> 53d3423 (cambios en usuario)
  let filtered = $derived(usuarios.filter(u =>
    !searchText ||
    u.nombre?.toLowerCase().includes(searchText.toLowerCase()) ||
    u.cedula?.includes(searchText) ||
    u.correo?.toLowerCase().includes(searchText.toLowerCase())
  ))

<<<<<<< HEAD
=======
  // --- CARGA DE DATOS ---
>>>>>>> 53d3423 (cambios en usuario)
  onMount(async () => {
    try {
<<<<<<< HEAD
      const [uData, rData] = await Promise.allSettled([api.getUsuarios(), api.getRoles()])
      usuarios = uData.value?.resultado || []
      // Ajuste para manejar si roles viene directo o en .resultado
      roles = rData.value?.resultado || rData.value || []
    } catch(e) {
      console.error("Error al cargar datos iniciales:", e)
    } finally {
      loading = false
    }
  })

  // --- ACCIONES ---
  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  
  function openEdit(u) { 
    form = { ...u }; 
    selected = u; 
    view = 'form' 
  }

  async function saveUsuario() {
    if (!form.nombre || !form.cedula || !form.correo) {
      showToast('Nombre, cédula y correo son obligatorios', 'error'); 
      return
=======
      const [uData, rData] = await Promise.allSettled([
        api.getUsuarios(),
        api.getRoles()
      ])
      usuarios = uData.value?.resultado || uData.value || []
      roles = rData.value?.resultado || rData.value || []
    } catch(e) {
      console.error("Error cargando datos:", e)
    } finally {
      loading = false 
    }
  })

  // --- MAPEO DE ROLES (DICCIONARIO DE EMERGENCIA) ---
  function getRolLabel(id) {
    if (Array.isArray(roles) && roles.length > 0) {
      const r = roles.find(rol => rol.id_rol == id)
      if (r) return r.nombre || r.nombre_rol
    }
    const diccionario = {
      1: 'ESTUDIANTE', 2: 'DOCENTE', 3: 'ADMINISTRADOR',
      4: 'COORDINADOR', 5: 'SECRETARIA', 6: 'SOPORTE',
      7: 'DECANO', 8: 'DIRECTOR', 9: 'INVESTIGADOR',
      10: 'MONITOR', 11: 'TUTOR', 12: 'ANALISTA'
    }
    return diccionario[id] || `ROL ${id}`
  }

  // --- ACCIONES ---
  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(u) { form = { ...u }; selected = u; view = 'form' }

  async function saveUsuario() {
    if (!form.nombre || !form.cedula || !form.correo) {
      showToast('⚠️ Completa los campos obligatorios'); return
>>>>>>> 53d3423 (cambios en usuario)
    }
    saving = true
    try {
      const payload = { ...form, id_rol: parseInt(form.id_rol), semestre: form.semestre ? parseInt(form.semestre) : null }
      if (selected) await api.updateUsuario(selected.id_usuario, payload)
      else await api.createUsuario(payload)
      
<<<<<<< HEAD
      if (selected) {
        await api.updateUsuario(selected.id_usuario, payload)
        showToast('Usuario actualizado correctamente')
      } else {
        await api.createUsuario(payload)
        showToast('Nuevo usuario registrado')
      }
      
      // Recarga fresca de la lista
      const data = await api.getUsuarios()
      usuarios = data.resultado || []
      view = 'list'
    } catch(e) { 
      showToast('Error en el servidor: ' + e.message, 'error') 
    } finally {
      saving = false
    }
=======
      const res = await api.getUsuarios()
      usuarios = res.resultado || res || []
      view = 'list'
      showToast('✅ Operación exitosa')
    } catch(e) { showToast('❌ Error al guardar') }
    finally { saving = false }
>>>>>>> 53d3423 (cambios en usuario)
  }

  async function deleteUsuario(id) {
    if (!confirm('¿Estás seguro de eliminar este usuario permanentemente?')) return
    try {
      await api.deleteUsuario(id)
      usuarios = usuarios.filter(u => u.id_usuario !== id)
<<<<<<< HEAD
      showToast('Usuario eliminado del sistema')
    } catch(e) { 
      showToast('No se pudo eliminar el usuario', 'error') 
    }
  }

  // Mapeo dinámico de Roles
  function getRolLabel(id) {
    const r = roles.find(r => r.id_rol == id)
    return r?.nombre || r?.nombre_rol || (id === 1 ? 'ADMIN' : id === 2 ? 'ESTUDIANTE' : `ROL ${id}`)
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3500)
  }
</script>

<div class="module">
  {#if toastMsg}
    <div class="toast {toastType}" role="alert">
      {toastType === 'success' ? '✅' : '❌'} {toastMsg}
    </div>
  {/if}

  <header class="page-header">
    <div>
      <h1>{view === 'list' ? 'Gestión de Personal' : selected ? 'Editar Perfil' : 'Registro de Usuario'}</h1>
      <p class="subtitle">{view === 'list' ? 'Directorio central de usuarios y roles' : 'Actualiza la información institucional del usuario'}</p>
=======
      showToast('🗑️ Usuario eliminado')
    } catch(e) { showToast('❌ Error al eliminar') }
  }

  function showToast(msg) { toastMsg = msg; setTimeout(() => toastMsg = '', 3000) }
</script>

<div class="module">
  {#if toastMsg}<div class="toast">{toastMsg}</div>{/if}

  <header class="page-header">
    <div class="header-info">
      <h1>{view === 'list' ? 'Gestión de Personal' : (selected ? 'Editar Usuario' : 'Nuevo Usuario')}</h1>
      <p class="subtitle">Directorio institucional de usuarios y roles</p>
>>>>>>> 53d3423 (cambios en usuario)
    </div>
    <div class="header-actions">
      {#if view !== 'list'}
        <button class="btn-secondary" onclick={() => view = 'list'}>← Cancelar</button>
      {:else}
<<<<<<< HEAD
        <button class="btn-primary" onclick={openCreate}>＋ Registrar Usuario</button>
=======
        <button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>
>>>>>>> 53d3423 (cambios en usuario)
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
<<<<<<< HEAD
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" type="text" placeholder="Buscar por nombre, cédula o correo institucional…" bind:value={searchText} />
=======
        <span class="search-icon">🔍</span>
        <input type="text" class="modern-input" placeholder="Buscar por nombre, cédula o correo..." bind:value={searchText} />
>>>>>>> 53d3423 (cambios en usuario)
      </div>
    </div>

    {#if loading}
<<<<<<< HEAD
      <div class="loading-state"><span class="spinner-lg"></span><p>Sincronizando con la base de datos…</p></div>
    {:else if filtered.length === 0}
      <div class="empty-state">
        <div class="empty-icon">👥</div>
        <p>No se encontraron resultados para "{searchText}"</p>
        <button class="btn-primary" onclick={() => searchText = ''}>Limpiar búsqueda</button>
      </div>
=======
      <div class="loading-state"><span class="spinner"></span><p>Sincronizando...</p></div>
>>>>>>> 53d3423 (cambios en usuario)
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Identificación</th>
<<<<<<< HEAD
              <th>Contacto</th>
              <th>Rol Institucional</th>
=======
              <th>Correo</th>
              <th>Rol</th>
>>>>>>> 53d3423 (cambios en usuario)
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as u (u.id_usuario)}
              <tr>
                <td><span class="id-badge">#{u.id_usuario}</span></td>
                <td>
                  <div class="user-cell">
                    <div class="avatar">{u.nombre?.charAt(0).toUpperCase() || '?'}</div>
                    <div class="name-info">
                      <p class="user-name">{u.nombre}</p>
<<<<<<< HEAD
                      <p class="user-sub">{u.carrera || 'Administrativo'}{u.semestre ? ` • Semestre ${u.semestre}` : ''}</p>
=======
                      <p class="user-sub">{u.carrera || 'CUL'}</p>
>>>>>>> 53d3423 (cambios en usuario)
                    </div>
                  </div>
                </td>
                <td class="mono-cell">{u.cedula}</td>
                <td class="email-cell">
                  <span class="email-text">{u.correo}</span>
                  <span class="phone-sub">{u.celular || 'Sin teléfono'}</span>
                </td>
                <td>
                  <span class="role-badge r{u.id_rol}">
                    {getRolLabel(u.id_rol)}
                  </span>
                </td>
                <td>
                  <div class="row-actions">
<<<<<<< HEAD
                    <button class="icon-btn edit" onclick={() => openEdit(u)} title="Editar información">✎</button>
                    <button class="icon-btn delete" onclick={() => deleteUsuario(u.id_usuario)} title="Eliminar cuenta">✕</button>
=======
                    <button class="icon-btn edit" onclick={() => openEdit(u)}>✎</button>
                    <button class="icon-btn delete" onclick={() => deleteUsuario(u.id_usuario)}>✕</button>
>>>>>>> 53d3423 (cambios en usuario)
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
<<<<<<< HEAD
      <footer class="table-footer">
        <p>Mostrando <b>{filtered.length}</b> usuarios registrados</p>
      </footer>
=======
>>>>>>> 53d3423 (cambios en usuario)
    {/if}

  {:else}
    <div class="form-container">
<<<<<<< HEAD
        <div class="form-card">
          <div class="form-grid">
            <div class="field full"><label>Nombre Completo institucional *</label><input type="text" bind:value={form.nombre} /></div>
            <div class="field"><label>Número de Identificación *</label><input type="text" bind:value={form.cedula} /></div>
            <div class="field"><label>Correo Electrónico *</label><input type="email" bind:value={form.correo} /></div>
            <div class="field"><label>Teléfono Móvil</label><input type="text" bind:value={form.celular} /></div>
            <div class="field">
                <label>Rol en el Sistema</label>
                <select bind:value={form.id_rol}>
                  <option value="">Seleccionar rol...</option>
                  {#each roles as r}<option value={r.id_rol}>{r.nombre_rol || r.nombre}</option>{/each}
                </select>
            </div>
            <div class="field"><label>Programa / Carrera</label><input type="text" bind:value={form.carrera} /></div>
            <div class="field"><label>Semestre Actual</label><input type="number" bind:value={form.semestre} min="1" max="12" /></div>
            <div class="field full"><label>Cargo o Dependencia</label><input type="text" bind:value={form.cargo} placeholder="Ej: Docente, Coordinador, Estudiante" /></div>
          </div>
          <div class="form-actions">
            <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
            <button class="btn-primary" onclick={saveUsuario} disabled={saving}>
              {saving ? 'Guardando...' : (selected ? 'Guardar Cambios' : 'Crear Usuario')}
            </button>
          </div>
        </div>
=======
      <div class="card animate-up">
        <h2 class="card-title">{selected ? 'Actualizar Información' : 'Registro de Usuario'}</h2>
        <div class="form-grid">
          <div class="field full"><label>Nombre Completo</label><input type="text" bind:value={form.nombre} /></div>
          <div class="field"><label>Cédula</label><input type="text" bind:value={form.cedula} /></div>
          <div class="field"><label>Correo Institucional</label><input type="email" bind:value={form.correo} /></div>
          <div class="field">
            <label>Rol</label>
            <select bind:value={form.id_rol}>
              <option value="">Seleccionar...</option>
              <option value="1">Estudiante</option>
              <option value="2">Docente</option>
              <option value="3">Administrador</option>
              <option value="4">Coordinador</option>
              <option value="5">Secretaria</option>
              <option value="6">Soporte</option>
            </select>
          </div>
          <div class="field"><label>Carrera</label><input type="text" bind:value={form.carrera} /></div>
        </div>
        <div class="form-actions">
          <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
          <button class="btn-primary" onclick={saveUsuario} disabled={saving}>{saving ? 'Procesando...' : 'Guardar Datos'}</button>
        </div>
      </div>
>>>>>>> 53d3423 (cambios en usuario)
    </div>
  {/if}
</div>

<style>
<<<<<<< HEAD
  /* --- LAYOUT & THEME --- */
  .module { padding: 40px; max-width: 1250px; margin: 0 auto; }
  
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em; }
  .subtitle { color: #64748b; font-size: 14px; margin-top: 4px; }

  /* --- TOOLBAR --- */
  .toolbar { margin-bottom: 24px; }
  .search-wrap { position: relative; max-width: 450px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
  .search-input { width: 100%; padding: 12px 14px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: white; font-size: 14px; transition: 0.2s; outline: none; }
  .search-input:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.08); }

  /* --- TABLA --- */
  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; vertical-align: middle; }
  
  .user-cell { display: flex; align-items: center; gap: 12px; }
  .avatar-sm { width: 38px; height: 38px; border-radius: 12px; background: #eff6ff; color: #2563eb; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 15px; border: 1px solid #dbeafe; }
  .name-info { display: flex; flex-direction: column; }
  .user-name { font-weight: 700; color: #1e293b; margin: 0; }
  .user-sub { font-size: 11px; color: #94a3b8; margin: 2px 0 0; }
  
  .id-badge { background: #f1f5f9; color: #475569; padding: 4px 8px; border-radius: 6px; font-weight: 700; font-size: 12px; font-family: 'JetBrains Mono', monospace; }
  .mono-cell { font-family: monospace; color: #64748b; font-weight: 600; }
  
  .email-cell { display: flex; flex-direction: column; }
  .email-text { color: #2563eb; font-weight: 500; font-size: 13px; }
  .phone-sub { font-size: 11px; color: #94a3b8; margin-top: 2px; }

  /* --- BADGES --- */
  .role-badge { padding: 6px 12px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; }
  .r1 { background: #fee2e2; color: #991b1b; } /* Admin - Rojo suave */
  .r2 { background: #dcfce7; color: #166534; } /* Estudiante - Verde suave */
  .role-badge:not(.r1):not(.r2) { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

  /* --- ACCIONES --- */
  .row-actions { display: flex; gap: 8px; }
  .icon-btn { width: 34px; height: 34px; border-radius: 10px; border: 1px solid #e2e8f0; background: white; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; }
  .icon-btn.edit { color: #fbb03b; }
  .icon-btn.edit:hover { background: #fffbeb; border-color: #fbb03b; }
  .icon-btn.delete { color: #ef4444; }
  .icon-btn.delete:hover { background: #fef2f2; border-color: #ef4444; }

  /* --- FORMULARIO --- */
  .form-container { display: flex; justify-content: center; }
  .form-card { background: white; padding: 40px; border-radius: 24px; border: 1px solid #e2e8f0; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05); width: 100%; max-width: 800px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 12px; font-weight: 800; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; display: block; }
  input, select { width: 100%; padding: 12px 16px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #f8fafc; color: #1e293b; font-size: 14px; outline: none; }
  input:focus, select:focus { border-color: #2563eb; background: white; }

  /* --- BOTONES --- */
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; }
  .btn-primary:hover:not(:disabled) { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
  .btn-secondary { background: #f1f5f9; color: #475569; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }

  /* --- UTILS --- */
  .table-footer { margin-top: 16px; text-align: right; font-size: 13px; color: #64748b; }
  .toast { position: fixed; top: 20px; right: 20px; padding: 16px 24px; border-radius: 16px; color: white; background: #1e293b; z-index: 1000; font-weight: 600; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
  .toast.error { background: #ef4444; }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .module { padding: 16px; }
  .page-header { flex-direction: column; gap: 12px; }
  h1 { font-size: 22px; }
  th, td { padding: 10px 12px; font-size: 12px; }
  .form-grid { grid-template-columns: 1fr; }
  .form-card { padding: 20px; }
}

=======
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; }
  .subtitle { color: #64748b; font-size: 14px; }

  /* TOOLBAR */
  .toolbar { margin-bottom: 25px; }
  .search-wrap { position: relative; max-width: 400px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
  .modern-input { width: 100%; padding: 12px 12px 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; }

  /* TABLE */
  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; color: #334155; }
  
  .user-cell { display: flex; align-items: center; gap: 12px; }
  .avatar { width: 36px; height: 36px; border-radius: 10px; background: #eff6ff; color: #2563eb; display: flex; align-items: center; justify-content: center; font-weight: 800; border: 1px solid #dbeafe; }
  .user-name { font-weight: 700; color: #1e293b; margin: 0; }
  .user-sub { font-size: 11px; color: #94a3b8; }

  /* ROLES (IDs coinciden con tu DB) */
  .role-badge { padding: 6px 12px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .r3 { background: #fee2e2; color: #991b1b; } /* Admin */
  .r1 { background: #dcfce7; color: #166534; } /* Estudiante */
  .r2 { background: #dbeafe; color: #1e40af; } /* Docente */
  .role-badge:not(.r1):not(.r2):not(.r3) { background: #f1f5f9; color: #475569; }

  .row-actions { display: flex; gap: 10px; justify-content: flex-end; }
  .icon-btn { background: none; border: none; font-size: 18px; cursor: pointer; transition: 0.2s; }
  .edit { color: #fbb03b; }
  .delete { color: #ef4444; }

  /* FORM */
  .center-container { display: flex; justify-content: center; padding: 20px 0; }
  .card { background: white; width: 100%; max-width: 650px; padding: 40px; border-radius: 30px; border: 1px solid #e2e8f0; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
  .field { display: flex; flex-direction: column; gap: 8px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
  input, select { padding: 12px; border-radius: 10px; border: 1.5px solid #e2e8f0; outline: none; }
  .form-actions { margin-top: 30px; display: flex; gap: 12px; justify-content: flex-end; }

  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .btn-secondary { background: #f1f5f9; color: #475569; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .toast { position: fixed; bottom: 20px; right: 20px; background: #0f172a; color: white; padding: 12px 24px; border-radius: 12px; z-index: 100; }
  .spinner { width: 30px; height: 30px; border: 3px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .animate-up { animation: slideUp 0.3s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
>>>>>>> 53d3423 (cambios en usuario)
</style>