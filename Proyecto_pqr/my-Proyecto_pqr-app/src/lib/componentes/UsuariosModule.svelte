<script>
  import { onMount } from 'svelte'
  import { api } from '../api.js'

  // --- ESTADOS ---
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

  // --- FILTRADO ---
  let filtered = $derived(usuarios.filter(u =>
    !searchText ||
    u.nombre?.toLowerCase().includes(searchText.toLowerCase()) ||
    u.cedula?.includes(searchText) ||
    u.correo?.toLowerCase().includes(searchText.toLowerCase())
  ))

  // --- CARGA DE DATOS ---
  onMount(async () => {
    loading = true
    try {
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
      showToast('⚠️ Completa los campos obligatorios', 'error'); return
    }
    saving = true
    try {
      const payload = { ...form, id_rol: parseInt(form.id_rol), semestre: form.semestre ? parseInt(form.semestre) : null }
      if (selected) await api.updateUsuario(selected.id_usuario, payload)
      else await api.createUsuario(payload)
      
      const res = await api.getUsuarios()
      usuarios = res.resultado || res || []
      view = 'list'
      showToast('✅ Operación exitosa')
    } catch(e) { showToast('❌ Error al guardar', 'error') }
    finally { saving = false }
  }

  async function deleteUsuario(id) {
    if (!confirm('🗑️ ¿Eliminar este usuario?')) return
    try {
      await api.deleteUsuario(id)
      usuarios = usuarios.filter(u => u.id_usuario !== id)
      showToast('Usuario eliminado')
    } catch(e) { showToast('Error al eliminar', 'error') }
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
        <button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <input class="search-input" type="text" placeholder="Buscar por nombre, cédula o correo..." bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Sincronizando...</p></div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Identificación</th>
              <th>Correo</th>
              <th>Rol</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as u (u.id_usuario)}
              <tr>
                <td><span class="id-badge">#{u.id_usuario}</span></td>
                <td>
                  <div class="user-cell">
                    <div class="avatar-sm">{u.nombre?.charAt(0).toUpperCase() || '?'}</div>
                    <div class="name-info">
                      <p class="user-name">{u.nombre}</p>
                      <p class="user-sub">{u.carrera || 'CUL'}</p>
                    </div>
                  </div>
                </td>
                <td>{u.cedula}</td>
                <td>{u.correo}</td>
                <td><span class="role-badge r{u.id_rol}">{getRolLabel(u.id_rol)}</span></td>
                <td class="text-right">
                  <div class="row-actions">
                    <button class="icon-btn edit" onclick={() => openEdit(u)}>✎</button>
                    <button class="icon-btn delete" onclick={() => deleteUsuario(u.id_usuario)}>✕</button>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

  {:else}
    <div class="form-container">
        <div class="form-card">
          <div class="form-grid">
            <div class="field full"><label>Nombre Completo *</label><input type="text" bind:value={form.nombre} /></div>
            <div class="field"><label>Cédula *</label><input type="text" bind:value={form.cedula} /></div>
            <div class="field"><label>Correo *</label><input type="email" bind:value={form.correo} /></div>
            <div class="field">
                <label>Rol</label>
                <select bind:value={form.id_rol}>
                  <option value="">Seleccionar...</option>
                  <option value="1">Estudiante</option>
                  <option value="2">Docente</option>
                  <option value="3">Administrador</option>
                </select>
            </div>
            <div class="field"><label>Carrera</label><input type="text" bind:value={form.carrera} /></div>
          </div>
          <div class="form-actions">
            <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
            <button class="btn-primary" onclick={saveUsuario} disabled={saving}>Guardar</button>
          </div>
        </div>
    </div>
  {/if}
</div>

<style>
  /* Aquí pega tus estilos CSS anteriores, los que tienen los colores .r1, .r2, etc. */
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; }
  .subtitle { color: #64748b; font-size: 14px; }
  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .btn-secondary { background: #f1f5f9; color: #475569; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .role-badge { padding: 6px 12px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .r3 { background: #fee2e2; color: #991b1b; } 
  .r1 { background: #dcfce7; color: #166534; }
  .toast { position: fixed; bottom: 20px; right: 20px; background: #0f172a; color: white; padding: 12px 24px; border-radius: 12px; z-index: 100; }
  .loading-state { text-align: center; padding: 60px; color: #94a3b8; }
</style>