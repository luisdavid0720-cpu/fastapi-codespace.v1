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
  let form = $state(defaultForm())

  function defaultForm() {
    return { nombre: '', cedula: '', carrera: '', semestre: '', cargo: '', celular: '', correo: '', id_rol: '' }
  }

  let filtered = $derived(usuarios.filter(u =>
    !searchText ||
    u.nombre?.toLowerCase().includes(searchText.toLowerCase()) ||
    u.cedula?.includes(searchText) ||
    u.correo?.toLowerCase().includes(searchText.toLowerCase())
  ))

  onMount(async () => {
    try {
      const [uData, rData] = await Promise.allSettled([api.getUsuarios(), api.getRoles()])
      usuarios = uData.value?.resultado || []
      roles = rData.value?.resultado || []
    } catch(e) {}
    loading = false
  })

  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(u) { form = { ...u }; selected = u; view = 'form' }

  async function saveUsuario() {
    if (!form.nombre || !form.cedula || !form.correo) {
      showToast('Nombre, cédula y correo son requeridos', 'error'); return
    }
    saving = true
    try {
      const payload = { ...form, semestre: form.semestre ? parseInt(form.semestre) : null, id_rol: form.id_rol ? parseInt(form.id_rol) : null }
      if (selected) {
        await api.updateUsuario(selected.id_usuario, payload)
        usuarios = usuarios.map(u => u.id_usuario === selected.id_usuario ? { ...u, ...payload } : u)
        showToast('Usuario actualizado')
      } else {
        await api.createUsuario(payload)
        const data = await api.getUsuarios()
        usuarios = data.resultado || []
        showToast('Usuario creado')
      }
      view = 'list'
    } catch(e) { showToast('Error: ' + e.message, 'error') }
    saving = false
  }

  async function deleteUsuario(id) {
    if (!confirm('¿Eliminar este usuario?')) return
    try {
      await api.deleteUsuario(id)
      usuarios = usuarios.filter(u => u.id_usuario !== id)
      showToast('Usuario eliminado')
    } catch(e) { showToast('Error al eliminar', 'error') }
  }

  function getRolLabel(id) {
    const r = roles.find(r => r.id_rol == id)
    return r?.nombre_rol || (id === 1 ? 'Administrador' : id === 2 ? 'Usuario' : `Rol ${id}`)
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type
    setTimeout(() => toastMsg = '', 3500)
  }
</script>

<div class="module">
  {#if toastMsg}<div class="toast {toastType}" role="alert">{toastMsg}</div>{/if}

  <div class="page-header">
    <div>
      <h1>{view === 'list' ? 'Gestión de Usuarios' : selected ? 'Editar Usuario' : 'Nuevo Usuario'}</h1>
      <p class="subtitle">{view === 'list' ? 'CRUD completo de usuarios del sistema' : 'Completa la información del usuario'}</p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}
        <button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>
      {:else}
        <button class="btn-primary" onclick={openCreate}>＋ Nuevo Usuario</button>
      {/if}
    </div>
  </div>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" type="text" placeholder="Buscar por nombre, cédula o correo…" bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Cargando usuarios…</p></div>
    {:else if filtered.length === 0}
      <div class="empty-state">
        <div class="empty-icon">◉</div>
        <p>No hay usuarios {searchText ? 'que coincidan' : 'registrados'}</p>
        <button class="btn-primary" onclick={openCreate}>Crear usuario</button>
      </div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Nombre</th><th>Cédula</th><th>Correo</th><th>Cargo</th><th>Rol</th><th>Acciones</th></tr></thead>
          <tbody>
            {#each filtered as u (u.id_usuario)}
              <tr>
                <td><span class="id-badge">#{u.id_usuario}</span></td>
                <td>
                  <div class="user-cell">
                    <div class="avatar-sm">{u.nombre?.charAt(0)?.toUpperCase() || '?'}</div>
                    <div>
                      <p class="user-name">{u.nombre}</p>
                      {#if u.carrera}<p class="user-sub">{u.carrera}{u.semestre ? ` — Sem. ${u.semestre}` : ''}</p>{/if}
                    </div>
                  </div>
                </td>
                <td class="mono">{u.cedula}</td>
                <td class="email-cell">{u.correo}</td>
                <td>{u.cargo || '—'}</td>
                <td><span class="role-badge r{u.id_rol}">{getRolLabel(u.id_rol)}</span></td>
                <td>
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
      <p class="count-label">{filtered.length} de {usuarios.length} usuarios</p>
    {/if}

  {:else}
    <div class="form-card">
      <div class="form-grid">
        <div class="field"><label>Nombre completo *</label><input type="text" bind:value={form.nombre} placeholder="Nombre del usuario" /></div>
        <div class="field"><label>Cédula *</label><input type="text" bind:value={form.cedula} placeholder="Número de cédula" /></div>
        <div class="field"><label>Correo *</label><input type="email" bind:value={form.correo} placeholder="correo@ejemplo.com" /></div>
        <div class="field"><label>Celular</label><input type="text" bind:value={form.celular} placeholder="Número de celular" /></div>
        <div class="field"><label>Carrera</label><input type="text" bind:value={form.carrera} placeholder="Carrera o programa" /></div>
        <div class="field"><label>Semestre</label><input type="number" bind:value={form.semestre} placeholder="Semestre actual" min="1" max="12" /></div>
        <div class="field"><label>Cargo</label><input type="text" bind:value={form.cargo} placeholder="Cargo en la institución" /></div>
        <div class="field">
          <label>Rol</label>
          <select bind:value={form.id_rol}>
            <option value="">Sin rol asignado</option>
            {#each roles as r}<option value={r.id_rol}>{r.nombre_rol}</option>{/each}
            {#if roles.length === 0}<option value="1">Administrador</option><option value="2">Usuario</option>{/if}
          </select>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn-secondary" onclick={() => view = 'list'}>Cancelar</button>
        <button class="btn-primary" onclick={saveUsuario} disabled={saving}>
          {#if saving}<span class="spinner-sm"></span>{/if}
          {selected ? 'Actualizar' : 'Crear Usuario'}
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px 48px; max-width: 1200px; position: relative; }
  .toast { position: fixed; top: 24px; right: 24px; z-index: 999; padding: 12px 20px; border-radius: var(--radius-sm); font-size: 14px; font-weight: 500; animation: slideIn 0.3s ease; max-width: 360px; }
  .toast.success { background: rgba(0,184,148,0.12); border: 1px solid rgba(71,255,178,0.4); color: #00a381; }
  .toast.error { background: rgba(214,48,49,0.1); border: 1px solid rgba(255,71,71,0.4); color: var(--danger); }
  @keyframes slideIn { from { opacity:0; transform: translateX(20px); } to { opacity:1; transform:translateX(0); } }
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; flex-wrap: wrap; gap: 16px; }
  h1 { font-family: var(--font-display); font-size: 30px; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 4px; }
  .subtitle { color: var(--text-muted); font-size: 14px; }
  .header-actions { display: flex; gap: 10px; }
  .toolbar { display: flex; gap: 12px; margin-bottom: 20px; }
  .search-wrap { position: relative; flex: 1; max-width: 420px; }
  .search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
  .search-input { width: 100%; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); color: var(--text); padding: 10px 12px 10px 38px; font-size: 14px; outline: none; transition: border-color 0.2s; }
  .search-input:focus { border-color: var(--accent); }
  .table-wrap { overflow-x: auto; border-radius: var(--radius); border: 1px solid var(--border); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { background: var(--surface); padding: 12px 16px; text-align: left; font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; border-bottom: 1px solid var(--border); white-space: nowrap; }
  td { padding: 14px 16px; border-bottom: 1px solid rgba(42,42,56,0.5); }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: rgba(255,255,255,0.02); }
  .id-badge { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 3px 8px; font-size: 12px; font-family: monospace; }
  .user-cell { display: flex; align-items: center; gap: 10px; }
  .avatar-sm { width: 32px; height: 32px; border-radius: 50%; background: rgba(45,45,58,0.1); color: var(--accent); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-weight: 700; font-size: 14px; flex-shrink: 0; }
  .user-name { font-size: 14px; font-weight: 500; }
  .user-sub { font-size: 11px; color: var(--text-muted); }
  .mono { font-family: monospace; font-size: 13px; }
  .email-cell { font-size: 13px; color: #4a6fa5; }
  .role-badge { padding: 4px 10px; border-radius: 100px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
  .r1 { background: rgba(45,45,58,0.08); color: var(--accent); }
  .r2 { background: rgba(74,111,165,0.1); color: #4a6fa5; }
  .row-actions { display: flex; gap: 6px; }
  .icon-btn { width: 30px; height: 30px; border-radius: 6px; border: 1px solid var(--border); background: transparent; display: flex; align-items: center; justify-content: center; font-size: 14px; transition: all 0.15s; color: var(--text-muted); }
  .icon-btn.edit:hover { border-color: #4a6fa5; color: #4a6fa5; background: rgba(74,111,165,0.1); }
  .icon-btn.delete:hover { border-color: var(--danger); color: var(--danger); background: rgba(214,48,49,0.08); }
  .count-label { margin-top: 12px; font-size: 12px; color: var(--text-muted); text-align: right; }
  .form-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; max-width: 760px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }
  .field { display: flex; flex-direction: column; gap: 8px; }
  label { font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
  input, select { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius-sm); color: var(--text); padding: 11px 14px; font-size: 14px; outline: none; transition: border-color 0.2s; }
  input:focus, select:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(232,255,71,0.08); }
  select option { background: var(--surface2); }
  .form-actions { display: flex; gap: 12px; justify-content: flex-end; }
  .btn-primary { background: var(--accent); color: #ffffff; border: none; border-radius: var(--radius-sm); padding: 10px 20px; font-family: var(--font-display); font-size: 14px; font-weight: 700; display: flex; align-items: center; gap: 6px; transition: opacity 0.2s, transform 0.15s; }
  .btn-primary:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-secondary { background: transparent; color: var(--text); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 10px 18px; font-size: 14px; font-weight: 500; transition: all 0.15s; }
  .btn-secondary:hover { border-color: var(--text-muted); }
  .loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 40px; gap: 16px; color: var(--text-muted); }
  .empty-icon { font-size: 40px; color: var(--border); }
  .spinner-lg { width: 32px; height: 32px; border: 3px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.7s linear infinite; }
  .spinner-sm { width: 14px; height: 14px; border: 2px solid rgba(0,0,0,0.3); border-top-color: #ffffff; border-radius: 50%; animation: spin 0.7s linear infinite; display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }
  @media (max-width: 768px) { .module { padding: 24px 16px; } .form-grid { grid-template-columns: 1fr; } h1 { font-size: 22px; } }
</style>
