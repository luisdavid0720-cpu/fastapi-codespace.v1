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

  // --- CARGA DE DATOS (CORREGIDA PARA EVITAR EL BLOQUEO) ---
  onMount(async () => {
    loading = true;
    try {
      // Intentamos cargar usuarios
      const uData = await api.getUsuarios().catch(e => {
        console.error("Error en Usuarios:", e);
        return { resultado: [] };
      });
      usuarios = uData?.resultado || uData || [];

      // Intentamos cargar roles (Si da 404, el catch evita que se rompa la app)
      const rData = await api.getRoles().catch(e => {
        console.warn("La ruta de roles falló (404), se usarán nombres genéricos.");
        return []; 
      });
      roles = Array.isArray(rData) ? rData : (rData?.resultado || []);

    } catch(e) {
      console.error("Error general en el montaje:", e);
    } finally {
      loading = false; // ESTO QUITA EL SPINNER "Sincronizando..."
    }
  });

  // --- FUNCIONES DE APOYO ---
  function getRolLabel(id) {
    // Verificación de seguridad para evitar el error ".find is not a function"
    if (!Array.isArray(roles) || roles.length === 0) {
      return id === 1 ? 'Administrador' : id === 2 ? 'Usuario' : `Rol ${id}`;
    }
    const r = roles.find(rol => rol.id_rol == id);
    return r?.nombre || r?.nombre_rol || (id === 1 ? 'Administrador' : 'Usuario');
  }

  function openCreate() { form = defaultForm(); selected = null; view = 'form' }
  function openEdit(u) { form = { ...u }; selected = u; view = 'form' }

  async function saveUsuario() {
    if (!form.nombre || !form.cedula || !form.correo) {
      showToast('Campos obligatorios faltantes', 'error'); return;
    }
    saving = true;
    try {
      const payload = { ...form, semestre: parseInt(form.semestre), id_rol: parseInt(form.id_rol) };
      if (selected) await api.updateUsuario(selected.id_usuario, payload);
      else await api.createUsuario(payload);
      
      const data = await api.getUsuarios();
      usuarios = data.resultado || data || [];
      showToast('Operación exitosa');
      view = 'list';
    } catch(e) { showToast('Error al guardar', 'error'); }
    finally { saving = false; }
  }

  function showToast(msg, type = 'success') {
    toastMsg = msg; toastType = type;
    setTimeout(() => toastMsg = '', 3500);
  }
</script>

<div class="module">
  {#if toastMsg}<div class="toast {toastType}">{toastMsg}</div>{/if}

  <header class="page-header">
    <div class="header-info">
      <h1>{view === 'list' ? 'Gestión de Personal' : 'Formulario de Usuario'}</h1>
      <p class="subtitle">Directorio central de usuarios y roles del sistema</p>
    </div>
    <div class="header-actions">
      {#if view !== 'list'}
        <button class="btn-secondary" onclick={() => view = 'list'}>← Volver</button>
      {:else}
        <button class="btn-primary" onclick={openCreate}>＋ Registrar Usuario</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="toolbar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input class="search-input" type="text" placeholder="Buscar por nombre, cédula o correo institucional…" bind:value={searchText} />
      </div>
    </div>

    {#if loading}
      <div class="loading-state"><span class="spinner-lg"></span><p>Sincronizando con la base de datos…</p></div>
    {:else}
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Perfil / Usuario</th>
              <th>Identificación</th>
              <th>Correo</th>
              <th>Rol Institucional</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as u (u.id_usuario)}
              <tr>
                <td><span class="id-badge">#{u.id_usuario}</span></td>
                <td>
                  <div class="user-cell">
                    <div class="avatar-sm">{u.nombre?.charAt(0)?.toUpperCase() || '?'}</div>
                    <div class="name-info">
                      <p class="user-name">{u.nombre}</p>
                      <p class="user-sub">{u.carrera || 'Administrativo'}</p>
                    </div>
                  </div>
                </td>
                <td class="mono-cell">{u.cedula}</td>
                <td class="email-text">{u.correo}</td>
                <td><span class="role-badge r{u.id_rol}">{getRolLabel(u.id_rol)}</span></td>
                <td>
                  <div class="row-actions">
                    <button class="icon-btn edit" onclick={() => openEdit(u)}>✎</button>
                    <button class="icon-btn delete">✕</button>
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
              {#each roles as r}<option value={r.id_rol}>{r.nombre_rol || r.nombre}</option>{/each}
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
  .module { padding: 24px 40px; width: 100%; box-sizing: border-box; }
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; width: 100%; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; }
  .subtitle { color: #64748b; font-size: 14px; }

  .toolbar { margin-bottom: 24px; }
  .search-wrap { position: relative; max-width: 450px; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); opacity: 0.4; }
  .search-input { width: 100%; padding: 12px 42px; border-radius: 12px; border: 1.5px solid #e2e8f0; outline: none; background: white; }

  .table-wrap { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 16px 20px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
  td { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }

  .user-cell { display: flex; align-items: center; gap: 12px; }
  .avatar-sm { width: 36px; height: 36px; border-radius: 10px; background: #eff6ff; color: #2563eb; display: flex; align-items: center; justify-content: center; font-weight: 800; border: 1px solid #dbeafe; }
  .user-name { font-weight: 700; color: #1e293b; margin: 0; }
  .user-sub { font-size: 11px; color: #94a3b8; }
  
  .role-badge { padding: 6px 12px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .r1 { background: #fee2e2; color: #991b1b; } /* Admin */
  .r2 { background: #dcfce7; color: #166534; } /* Estudiante */

  .row-actions { display: flex; gap: 8px; justify-content: flex-end; }
  .icon-btn { border: 1px solid #e2e8f0; background: white; padding: 6px; border-radius: 8px; cursor: pointer; }
  .edit { color: #fbb03b; }
  .delete { color: #ef4444; }

  .btn-primary { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  .btn-secondary { background: #f1f5f9; color: #475569; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; }

  .form-container { display: flex; justify-content: center; }
  .form-card { background: white; padding: 32px; border-radius: 24px; border: 1px solid #e2e8f0; width: 100%; max-width: 700px; }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 12px; font-weight: 800; color: #475569; margin-bottom: 8px; display: block; }
  input, select, textarea { width: 100%; padding: 12px; border-radius: 10px; border: 1.5px solid #e2e8f0; }

  .toast { position: fixed; top: 20px; right: 20px; padding: 16px 24px; border-radius: 12px; color: white; background: #1e293b; z-index: 1000; }
  .spinner-lg { width: 40px; height: 40px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: block; margin: 40px auto; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .text-right { text-align: right; }
</style>