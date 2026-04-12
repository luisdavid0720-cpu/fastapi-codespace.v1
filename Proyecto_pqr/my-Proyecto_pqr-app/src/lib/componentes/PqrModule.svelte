<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'

  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list')
  let selected = $state(null)
  let saving = $state(false)
  let deleting = $state(false)
  let toastMsg = $state('')
  let editForm = $state(null)
  let generando = $state(false)

  // ── Filtros ─────────────────────────────────────────────
  let searchText   = $state('')
  let filterEstado = $state('')
  let filterTipo   = $state('')
  let filterDesde  = $state('')
  let filterHasta  = $state('')

  let tipos = $state([]), estados = $state([]), departamentos = $state([])
  let prioridades = $state([]), usuarios = $state([])

  function defaultForm() {
    return { descripcion: '', id_tipo: '', id_departamento: '' }
  }
  let form = $state(defaultForm())

  let isAdmin = $derived($currentUser?.id_rol === 1)

  let filtered = $derived(
    pqrs
      .filter(p => {
        const belongsToMe = isAdmin || Number(p.id_usuario) === Number($currentUser?.id_usuario)
        const matchText   = !searchText   || p.descripcion?.toLowerCase().includes(searchText.toLowerCase())
        const matchEstado = !filterEstado || String(p.id_estado) === String(filterEstado)
        const matchTipo   = !filterTipo   || String(p.id_tipo)   === String(filterTipo)
        const fecha       = new Date(p.fecha)
        const matchDesde  = !filterDesde  || fecha >= new Date(filterDesde)
        const matchHasta  = !filterHasta  || fecha <= new Date(filterHasta + 'T23:59:59')
        return belongsToMe && matchText && matchEstado && matchTipo && matchDesde && matchHasta
      })
      .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
  )

  onMount(async () => {
    loading = true
    try {
      const [p, t, e, d, pr, u] = await Promise.allSettled([
        api.getPqrs(), api.getTiposPqr(), api.getEstados(),
        api.getDepartamentos(), api.getPrioridades(), api.getUsuarios()
      ])
      pqrs          = p.value?.resultado || []
      tipos         = t.value            || []
      estados       = e.value            || []
      departamentos = d.value            || []
      prioridades   = pr.value          || []
      usuarios      = u.value?.resultado || u.value || []
    } catch(e) { console.error(e) }
    loading = false
  })

  // ── Navegación ──────────────────────────────────────────
  function openCreate() { form = defaultForm(); view = 'form' }
  function openDetail(pqr) { selected = pqr; view = 'detail' }

  function openEdit(pqr) {
    editForm = {
      id_pqr: pqr.id_pqr,
      descripcion: pqr.descripcion,
      id_tipo: pqr.id_tipo,
      id_departamento: pqr.id_departamento,
      id_estado: pqr.id_estado,
      id_prioridad: pqr.id_prioridad
    }
    view = 'edit'
  }

  // ── CRUD ────────────────────────────────────────────────
  async function saveEdit() {
    if (!editForm.descripcion || !editForm.id_tipo || !editForm.id_departamento) {
      showToast('⚠️ Completa todos los campos'); return
    }
    saving = true
    try {
      await api.updatePqr(editForm.id_pqr, editForm)
      const data = await api.getPqrs()
      pqrs = data.resultado || []
      view = 'list'
      showToast('✅ PQR actualizada')
    } catch(e) { showToast('❌ Error al actualizar') }
    saving = false
  }

  async function deletePqr(pqr) {
    if (!confirm(`¿Eliminar la PQR #${pqr.id_pqr}? Esta acción no se puede deshacer.`)) return
    deleting = true
    try {
      await api.deletePqr(pqr.id_pqr)
      pqrs = pqrs.filter(p => p.id_pqr !== pqr.id_pqr)
      showToast('🗑️ PQR eliminada')
    } catch(e) { showToast('❌ Error al eliminar') }
    deleting = false
  }

  async function savePqr() {
    if (!form.descripcion || !form.id_tipo || !form.id_departamento) {
      showToast('⚠️ Completa todos los campos'); return
    }
    saving = true
    try {
      const payload = {
        ...form,
        id_pqr: 0,
        fecha: new Date().toISOString(),
        id_usuario: $currentUser?.id_usuario,
        id_estado: 1,
        id_prioridad: 1
      }
      await api.createPqr(payload)
      const data = await api.getPqrs()
      pqrs = data.resultado || []
      view = 'list'
      showToast('✅ PQR enviada con éxito')
    } catch(e) { showToast('❌ Error al enviar') }
    saving = false
  }

  // ── Filtros ─────────────────────────────────────────────
  function limpiarFiltros() {
    searchText = ''; filterEstado = ''; filterTipo = ''
    filterDesde = ''; filterHasta = ''
  }

  // ── PDF ─────────────────────────────────────────────────
  async function descargarPDF() {
    if (filtered.length === 0) return
    generando = true
    try {
      const { jsPDF }         = await import('https://esm.sh/jspdf@2.5.1')
      const { default: auto } = await import('https://esm.sh/jspdf-autotable@3.8.2')

      const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' })
      const W = 297

      // Encabezado azul
      doc.setFillColor(15, 23, 42)
      doc.rect(0, 0, W, 28, 'F')

      // Logo
      try {
        const logoUrl  = window.location.origin + '/logo_cul.png'
        const response = await fetch(logoUrl)
        const blob     = await response.blob()
        const b64      = await new Promise(res => {
          const r = new FileReader()
          r.onload = () => res(r.result)
          r.readAsDataURL(blob)
        })
        doc.addImage(b64, 'PNG', 6, 3, 20, 20)
      } catch(_) {}

      doc.setTextColor(255, 255, 255)
      doc.setFontSize(13)
      doc.setFont('helvetica', 'bold')
      doc.text('Corporación Universitaria Latinoamericana', 30, 11)
      doc.setFontSize(9)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(148, 163, 184)
      doc.text('Sistema PQRS — Gestión de Solicitudes', 30, 18)

      const ahora = new Date().toLocaleString('es-CO')
      doc.setTextColor(148, 163, 184)
      doc.setFontSize(8)
      doc.text(`Generado: ${ahora}`, W - 14, 18, { align: 'right' })

      // Resumen de filtros
      doc.setTextColor(100, 116, 139)
      doc.setFontSize(7.5)
      const fl = []
      if (searchText)   fl.push(`Búsqueda: "${searchText}"`)
      if (filterEstado) fl.push(`Estado: ${getLabelEstado(filterEstado)}`)
      if (filterTipo)   fl.push(`Categoría: ${getLabelTipo(filterTipo)}`)
      if (filterDesde)  fl.push(`Desde: ${filterDesde}`)
      if (filterHasta)  fl.push(`Hasta: ${filterHasta}`)
      const flLabel = fl.length ? fl.join('  ·  ') : 'Sin filtros'
      doc.text(`Filtros: ${flLabel}   —   Total registros: ${filtered.length}`, 14, 33)

      // Tabla
      auto(doc, {
        startY: 37,
        head: [[
          { content: 'ID',            styles: { halign: 'center', cellWidth: 12 } },
          { content: 'Descripción',   styles: { cellWidth: 55 } },
          { content: 'Categoría',     styles: { cellWidth: 26 } },
          { content: 'Usuario',       styles: { cellWidth: 38 } },
          { content: 'Departamento',  styles: { cellWidth: 32 } },
          { content: 'Prioridad',     styles: { halign: 'center', cellWidth: 22 } },
          { content: 'Estado',        styles: { halign: 'center', cellWidth: 26 } },
          { content: 'Fecha',         styles: { halign: 'center', cellWidth: 22 } },
        ]],
        body: filtered.map(p => [
          `#${p.id_pqr}`,
          p.descripcion?.slice(0, 72) || '—',
          getLabelTipo(p.id_tipo),
          getLabelUsuario(p.id_usuario),
          getLabelDep(p.id_departamento),
          getLabelPrioridad(p.id_prioridad),
          getLabelEstado(p.id_estado),
          new Date(p.fecha).toLocaleDateString('es-CO'),
        ]),
        headStyles: { fillColor: [37, 99, 235], textColor: 255, fontSize: 8.5, fontStyle: 'bold' },
        bodyStyles: { fontSize: 8, textColor: [51, 65, 85] },
        alternateRowStyles: { fillColor: [248, 250, 252] },
        columnStyles: { 0: { halign: 'center' }, 5: { halign: 'center' }, 6: { halign: 'center' }, 7: { halign: 'center' } },
        margin: { left: 14, right: 14 },
        didDrawPage: ({ pageNumber }) => {
          const total = doc.internal.getNumberOfPages()
          doc.setFontSize(7); doc.setTextColor(148, 163, 184)
          doc.text(`Página ${pageNumber} de ${total}`, W / 2, 205, { align: 'center' })
          doc.text('CUL — Sistema PQRS', 14, 205)
          doc.text(ahora, W - 14, 205, { align: 'right' })
        }
      })

      const fecha = new Date().toISOString().slice(0, 10)
      doc.save(`pqrs_reporte_${fecha}.pdf`)
    } catch(e) { console.error(e) }
    generando = false
  }

  // ── Utilidades ───────────────────────────────────────────
  function showToast(msg) { toastMsg = msg; setTimeout(() => toastMsg = '', 3000) }

  const getLabelEstado    = (id) => estados.find(e => e.id_estado == id)?.nombre             || 'PENDIENTE'
  const getLabelTipo      = (id) => tipos.find(t => t.id_tipo == id)?.nombre                  || '—'
  const getLabelDep       = (id) => departamentos.find(d => d.id_departamento == id)?.nombre   || '—'
  const getLabelPrioridad = (id) => prioridades.find(p => p.id_prioridad == id)?.nombre       || '—'
  const getLabelUsuario   = (id) => {
    const u = usuarios.find(u => u.id_usuario == id)
    return u ? (u.nombre || u.correo || `#${id}`) : `#${id}`
  }
  const prioridadColor = (id) => {
    const n = getLabelPrioridad(id)?.toLowerCase()
    if (n.includes('alta') || n.includes('urgen') || n.includes('crít') || n.includes('muy')) return 'prio-alta'
    if (n.includes('media')) return 'prio-media'
    return 'prio-baja'
  }
</script>

<div class="module">
  {#if toastMsg}<div class="toast">{toastMsg}</div>{/if}

  <header class="page-header">
    <div class="header-content">
      <h1>
        {#if view === 'list'}
          {isAdmin ? 'Gestión de PQRs' : 'Mis Solicitudes'}
        {:else if view === 'detail'}
          Detalle del Radicado
        {:else if view === 'edit'}
          Editar PQR
        {:else}
          Nueva Solicitud
        {/if}
      </h1>
      <p class="subtitle">
        {isAdmin ? 'Administra todas las solicitudes del sistema' : 'Gestiona y consulta el estado de tus trámites'}
      </p>
    </div>
    <div class="header-actions">
      {#if view === 'list'}
        {#if isAdmin}
          <button class="btn-pdf" onclick={descargarPDF} disabled={generando || filtered.length === 0}>
            {#if generando}
              <span class="spinner"></span> Generando...
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="12" y1="18" x2="12" y2="12"/>
                <line x1="9" y1="15" x2="15" y2="15"/>
              </svg>
              Descargar PDF ({filtered.length})
            {/if}
          </button>
        {/if}
        {#if !isAdmin}
          <button class="btn-create" onclick={openCreate}>＋ Crear PQR</button>
        {/if}
      {:else}
        <button class="btn-back" onclick={() => view = 'list'}>← Volver</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <!-- Filtros -->
    <div class="filters-card">
      <p class="filters-title">Filtros del reporte</p>
      <div class="filters-grid">
        <div class="filter-field">
          <label>Búsqueda</label>
          <div class="input-wrap">
            <svg class="input-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" placeholder="Palabra clave..." bind:value={searchText} />
          </div>
        </div>
        {#if isAdmin}
          <div class="filter-field">
            <label>Estado</label>
            <select bind:value={filterEstado}>
              <option value="">Todos los estados</option>
              {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
            </select>
          </div>
          <div class="filter-field">
            <label>Categoría</label>
            <select bind:value={filterTipo}>
              <option value="">Todas las categorías</option>
              {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
            </select>
          </div>
          <div class="filter-field">
            <label>Desde</label>
            <input type="date" bind:value={filterDesde} />
          </div>
          <div class="filter-field">
            <label>Hasta</label>
            <input type="date" bind:value={filterHasta} />
          </div>
          <div class="filter-field align-end">
            <button class="btn-clear" onclick={limpiarFiltros}>Limpiar filtros</button>
          </div>
        {:else}
          <!-- Usuarios no admin ven búsqueda y resultados -->
        {/if}
      </div>
    </div>

    <div class="results-bar">
      <span class="results-count">
        <strong>{filtered.length}</strong> {filtered.length === 1 ? 'solicitud encontrada' : 'solicitudes encontradas'}
      </span>
      {#if filtered.length === 0 && !loading}
        <span class="no-results-hint">Ajusta los filtros para ver resultados</span>
      {/if}
    </div>

    {#if loading}
      <div class="loader-wrap"><p>Sincronizando...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Descripción</th>
              <th>Categoría</th>
              {#if isAdmin}
                <th>Usuario</th>
                <th>Departamento</th>
                <th>Prioridad</th>
                <th>Estado</th>
              {/if}
              <th>Fecha</th>
              <th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each filtered as pqr}
              <tr>
                <td><span class="id-tag">#{pqr.id_pqr}</span></td>
                <td class="text-main">{pqr.descripcion?.slice(0, 40)}...</td>
                <td><span class="type-chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                {#if isAdmin}
                  <td class="text-usuario">{getLabelUsuario(pqr.id_usuario)}</td>
                  <td class="text-dep">{getLabelDep(pqr.id_departamento)}</td>
                  <td><span class="prio-chip {prioridadColor(pqr.id_prioridad)}">{getLabelPrioridad(pqr.id_prioridad)}</span></td>
                  <td><span class="status-pill s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
                {/if}
                <td class="date-text">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td class="text-center actions-cell">
                  {#if isAdmin}
                    <button class="action-btn edit-btn" onclick={() => openEdit(pqr)} title="Editar">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                    </button>
                    <button class="action-btn delete-btn" onclick={() => deletePqr(pqr)} title="Eliminar" disabled={deleting}>
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                        <path d="M10 11v6M14 11v6"/>
                        <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                      </svg>
                    </button>
                  {:else}
                    <button class="action-btn view-btn" onclick={() => openDetail(pqr)} title="Ver detalle">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                  {/if}
                </td>
              </tr>
            {/each}
            {#if filtered.length === 0}
              <tr>
                <td colspan={isAdmin ? 9 : 5} class="empty-row">No se encontraron solicitudes</td>
              </tr>
            {/if}
          </tbody>
        </table>
      </div>
    {/if}

  {:else if view === 'detail'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="card-top">
          <div class="badge-row">
            <span class="id-large">Solicitud #{selected.id_pqr}</span>
            <span class="status-pill s{selected.id_estado}">{getLabelEstado(selected.id_estado)}</span>
          </div>
          <p class="date-sub">Registrado el {new Date(selected.fecha).toLocaleString('es-CO')}</p>
        </div>
        <div class="card-body">
          <div class="info-section">
            <label class="section-label">Descripción</label>
            <div class="content-box">{selected.descripcion}</div>
          </div>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Categoría</span>
              <span class="value">{getLabelTipo(selected.id_tipo)}</span>
            </div>
            <div class="info-item">
              <span class="label">Área Destino</span>
              <span class="value">{getLabelDep(selected.id_departamento)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  {:else if view === 'edit'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">Editar PQR #{editForm.id_pqr}</h2>
          <div class="field">
            <label class="section-label">Descripción</label>
            <textarea bind:value={editForm.descripcion} placeholder="Descripción de la solicitud..."></textarea>
          </div>
          <div class="field-group">
            <div class="field">
              <label class="section-label">Tipo</label>
              <select bind:value={editForm.id_tipo}>
                <option value="">Selecciona...</option>
                {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
              </select>
            </div>
            <div class="field">
              <label class="section-label">Departamento</label>
              <select bind:value={editForm.id_departamento}>
                <option value="">Selecciona...</option>
                {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
              </select>
            </div>
          </div>
          <div class="field-group">
            <div class="field">
              <label class="section-label">Estado</label>
              <select bind:value={editForm.id_estado}>
                {#each estados as e}<option value={e.id_estado}>{e.nombre}</option>{/each}
              </select>
            </div>
            <div class="field">
              <label class="section-label">Prioridad</label>
              <select bind:value={editForm.id_prioridad}>
                {#each prioridades as p}<option value={p.id_prioridad}>{p.nombre}</option>{/each}
              </select>
            </div>
          </div>
          <button class="btn-send" onclick={saveEdit} disabled={saving}>
            {saving ? 'Guardando...' : '💾 Guardar cambios'}
          </button>
        </div>
      </div>
    </div>

  {:else if view === 'form'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">Radicar nueva PQR</h2>
          <div class="field">
            <label class="section-label">¿Qué sucedió? <small>(Descripción)</small></label>
            <textarea bind:value={form.descripcion} placeholder="Explica detalladamente tu solicitud..."></textarea>
          </div>
          <div class="field-group">
            <div class="field">
              <label class="section-label">Tipo</label>
              <select bind:value={form.id_tipo}>
                <option value="">Selecciona...</option>
                {#each tipos as t}<option value={t.id_tipo}>{t.nombre}</option>{/each}
              </select>
            </div>
            <div class="field">
              <label class="section-label">Departamento</label>
              <select bind:value={form.id_departamento}>
                <option value="">Selecciona...</option>
                {#each departamentos as d}<option value={d.id_departamento}>{d.nombre}</option>{/each}
              </select>
            </div>
          </div>
          <button class="btn-send" onclick={savePqr} disabled={saving}>
            {saving ? 'Procesando...' : '🚀 Enviar Solicitud'}
          </button>
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
  .subtitle { color: #64748b; font-size: 15px; margin-top: 4px; }
  .header-actions { display: flex; gap: 12px; align-items: center; }

  .btn-create { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37,99,235,0.2); }
  .btn-back   { background: white; border: 1.5px solid #e2e8f0; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; }
  .btn-pdf {
    display: flex; align-items: center; gap: 8px;
    background: #dc2626; color: white; border: none;
    padding: 12px 22px; border-radius: 12px; font-weight: 700;
    font-size: 14px; cursor: pointer; transition: 0.2s; white-space: nowrap;
    box-shadow: 0 4px 14px rgba(220,38,38,0.25);
  }
  .btn-pdf:hover    { background: #b91c1c; transform: translateY(-1px); }
  .btn-pdf:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }
  .spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; display: inline-block; animation: spin 0.7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Filtros */
  .filters-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
  .filters-title { font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 16px; }
  .filters-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; align-items: end; }

  .filter-field { display: flex; flex-direction: column; gap: 6px; }
  .filter-field label { font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.4px; }
  .filter-field.align-end { justify-content: flex-end; }

  .input-wrap { position: relative; }
  .input-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; pointer-events: none; }
  .input-wrap input { padding-left: 36px !important; }

  .filter-field input, .filter-field select {
    padding: 10px 12px; border-radius: 10px; border: 1.5px solid #e2e8f0;
    font-size: 13px; outline: none; background: #fafafa; font-family: inherit;
    color: #334155; transition: border-color 0.2s; width: 100%; box-sizing: border-box;
  }
  .filter-field input:focus, .filter-field select:focus { border-color: #2563eb; background: white; }

  .btn-clear { padding: 10px 16px; border-radius: 10px; border: 1.5px solid #e2e8f0; background: white; color: #64748b; font-size: 13px; font-weight: 600; cursor: pointer; transition: 0.2s; font-family: inherit; width: 100%; }
  .btn-clear:hover { border-color: #cbd5e1; background: #f8fafc; }

  /* Resultados */
  .results-bar { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
  .results-count { font-size: 13px; color: #64748b; }
  .results-count strong { color: #0f172a; font-weight: 700; }
  .no-results-hint { font-size: 12px; color: #94a3b8; }

  /* Tabla */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 14px 16px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #f1f5f9; white-space: nowrap; }
  td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; font-size: 13px; color: #334155; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafbff; }
  .empty-row { text-align: center; color: #94a3b8; padding: 40px !important; }
  .text-main { max-width: 300px; }
  .text-usuario { font-weight: 600; color: #1e293b; }
  .text-dep { color: #475569; font-size: 12px; }
  .date-text { color: #64748b; font-size: 12px; white-space: nowrap; }

  /* Acciones */
  .actions-cell { display: flex; align-items: center; justify-content: center; gap: 6px; }
  .action-btn { width: 32px; height: 32px; border: none; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
  .view-btn   { background: #eff6ff; color: #2563eb; }
  .view-btn:hover   { background: #2563eb; color: white; transform: scale(1.1); }
  .edit-btn   { background: #f0fdf4; color: #16a34a; }
  .edit-btn:hover   { background: #16a34a; color: white; transform: scale(1.1); }
  .delete-btn { background: #fef2f2; color: #dc2626; }
  .delete-btn:hover { background: #dc2626; color: white; transform: scale(1.1); }
  .delete-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  /* Pills */
  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; font-size: 12px; }
  .type-chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 11px; white-space: nowrap; }
  .status-pill { padding: 5px 12px; border-radius: 100px; font-size: 10px; font-weight: 800; text-transform: uppercase; white-space: nowrap; }
  .s1 { background: #fef3c7; color: #92400e; }
  .s2 { background: #dbeafe; color: #1e40af; }
  .s3 { background: #d1fae5; color: #065f46; }
  .s4 { background: #e0e7ff; color: #3730a3; }
  .prio-chip { padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; white-space: nowrap; }
  .prio-alta  { background: #fef2f2; color: #dc2626; }
  .prio-media { background: #fff7ed; color: #c2410c; }
  .prio-baja  { background: #f0fdf4; color: #16a34a; }

  /* Card / form */
  .center-container { display: flex; justify-content: center; padding: 20px 0 60px; }
  .card { background: white; width: 100%; max-width: 680px; border-radius: 32px; border: 1px solid #e2e8f0; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.1); overflow: hidden; }
  .form-padding { padding: 45px; }
  .card-title { font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 30px; }
  .card-top { padding: 35px 45px; background: #f8fafc; border-bottom: 1px solid #f1f5f9; }
  .card-body { padding: 45px; }
  .badge-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .id-large { font-size: 24px; font-weight: 800; color: #0f172a; }
  .date-sub { color: #94a3b8; font-size: 13px; margin: 0; }
  .info-section { margin-bottom: 30px; }
  .content-box { background: #f8fafc; padding: 25px; border-radius: 20px; border: 1px solid #edf2f7; line-height: 1.7; font-size: 15px; color: #334155; }
  .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .info-item { display: flex; flex-direction: column; gap: 6px; }
  .label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  .value { font-weight: 700; color: #1e293b; font-size: 15px; }

  .field { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .section-label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  textarea, select { padding: 15px; border-radius: 14px; border: 1.5px solid #e2e8f0; background: #fcfcfc; font-size: 14px; outline: none; font-family: inherit; width: 100%; box-sizing: border-box; }
  textarea { min-height: 120px; resize: none; }
  .btn-send { width: 100%; background: #2563eb; color: white; border: none; padding: 18px; border-radius: 16px; font-weight: 800; font-size: 16px; cursor: pointer; margin-top: 10px; font-family: inherit; }

  .toast { position: fixed; bottom: 30px; right: 30px; background: #0f172a; color: white; padding: 16px 28px; border-radius: 16px; font-weight: 600; z-index: 100; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
  .animate-up { animation: slideUp 0.4s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
  .loader-wrap { padding: 60px; text-align: center; color: #94a3b8; }

  @media (max-width: 768px) {
    .module { padding: 16px; }
    .page-header { flex-direction: column; gap: 12px; align-items: flex-start; }
    .header-actions { width: 100%; }
    .btn-pdf, .btn-create { flex: 1; justify-content: center; }
    h1 { font-size: 22px; }
    .filters-grid { grid-template-columns: 1fr; }
    table { min-width: 700px; }
    th, td { padding: 10px 12px; font-size: 11px; }
    .form-padding, .card-top, .card-body { padding: 24px; }
    .field-group { grid-template-columns: 1fr; }
    .info-grid { grid-template-columns: 1fr; }
  }
</style>