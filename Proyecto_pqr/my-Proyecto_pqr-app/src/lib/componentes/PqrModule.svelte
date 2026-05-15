<script>
  import { onMount } from 'svelte'
  import { currentUser } from '../../stores/auth.js'
  import { api } from '../api.js'
  import Badge     from './Badge.svelte'
  import Modal     from './Modal.svelte'
  import FormField from './FormField.svelte'
  import { goto } from '$app/navigation'

  let pqrs = $state([])
  let loading = $state(true)
  let view = $state('list')
  let selected = $state(null)
  let saving = $state(false)
  let deleting = $state(false)
  let toastMsg = $state('')
  let editForm = $state(null)
  let generando = $state(false)
  let responsable = $state(null)

  let modalEliminarAbierto = $state(false)
  let pqrAEliminar = $state(null)

  let coordForm = $state({ id_estado: '', respuesta: '', id_responsable: '' })

  // Filtros
  let searchText   = $state('')
  let filterEstado = $state('')
  let filterTipo   = $state('')
  let filterDesde  = $state('')
  let filterHasta  = $state('')

  let tipos = $state([]), estados = $state([]), departamentos = $state([])
  let prioridades = $state([]), usuarios = $state([])

  let formDescripcion    = $state('')
  let formIdTipo         = $state('')
  let formIdDepartamento = $state('')

  // Paginación
  let currentPage  = $state(1)
  const rowsPerPage = 10

  function defaultForm() {
    formDescripcion    = ''
    formIdTipo         = ''
    formIdDepartamento = ''
    return { descripcion: '', id_tipo: '', id_departamento: '' }
  }
  let form = $state(defaultForm())

  let isAdmin = $derived($currentUser?.id_rol === 3)
  let isCoord = $derived($currentUser?.id_rol === 4)
  let isUser  = $derived($currentUser?.id_rol === 1)

  let filtered = $derived(
    pqrs
      .filter(p => {
        const belongsToMe = isAdmin || isCoord || Number(p.id_usuario) === Number($currentUser?.id_usuario)
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

  // Paginación derivada
  let totalPages = $derived(Math.max(1, Math.ceil(filtered.length / rowsPerPage)))
  let paginated  = $derived(filtered.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage))

  // Resetear página cuando cambian filtros
  $effect(() => {
    searchText; filterEstado; filterTipo; filterDesde; filterHasta
    currentPage = 1
  })

  onMount(async () => {
    loading = true
    try {
      const [p, t, e, d, pr, u] = await Promise.allSettled([
        api.getPqrs(),
        api.getTiposPqr(),
        api.getEstados(),
        api.getDepartamentos(),
        api.getPrioridades(),
        api.getUsuarios()
      ])

      pqrs = p.status === 'fulfilled'
        ? (Array.isArray(p.value) ? p.value : p.value?.resultado || [])
        : []

      tipos         = t.status === 'fulfilled'  ? (t.value?.resultado  || t.value  || []) : []
      estados       = e.status === 'fulfilled'  ? (e.value?.resultado  || e.value  || []) : []
      departamentos = d.status === 'fulfilled'  ? (d.value?.resultado  || d.value  || []) : []
      prioridades   = pr.status === 'fulfilled' ? (pr.value?.resultado || pr.value || []) : []
      usuarios      = u.status === 'fulfilled'  ? (u.value?.resultado  || u.value  || []) : []

    } catch (e) {
      console.error('Error cargando datos:', e)
      showToast('❌ Error cargando datos')
    } finally {
      loading = false
    }
  })

  function openCreate() { defaultForm(); view = 'form' }
 async function openDetail(pqr) {
  selected = pqr
  responsable = null       // null = cargando
  view = 'detail'
  try {
    const res = await api.getAsignacionByPqr(pqr.id_pqr)
    const idUsuario = res?.id_usuario
    if (idUsuario) {
      const u = usuarios.find(u => u.id_usuario == idUsuario)
      responsable = u ? (u.nombre || u.correo || `#${idUsuario}`) : `#${idUsuario}`
    } else {
      responsable = false  // false = sin asignar
    }
  } catch {
    responsable = false    // false = sin asignar
  }
}

  function openEdit(pqr) {
    editForm = {
      id_pqr: pqr.id_pqr, descripcion: pqr.descripcion, fecha: pqr.fecha,
      id_usuario: pqr.id_usuario, id_tipo: pqr.id_tipo,
      id_departamento: pqr.id_departamento, id_estado: pqr.id_estado,
      id_prioridad: pqr.id_prioridad
    }
    view = 'edit'
  }

  function openGestion(pqr) {
    selected = pqr
    coordForm = { id_estado: pqr.id_estado, respuesta: '', id_responsable: '' }
    view = 'gestion'
  }

  function pedirEliminar(pqr) { pqrAEliminar = pqr; modalEliminarAbierto = true }

  async function saveEdit() {
    if (!editForm.descripcion || !editForm.id_tipo || !editForm.id_departamento) {
      showToast('⚠️ Completa todos los campos'); return
    }
    saving = true
    try {
      await api.updatePqr(editForm.id_pqr, editForm)
      const data = await api.getPqrs()
      pqrs = Array.isArray(data) ? data : data.resultado || []
      view = 'list'
      showToast('✅ PQR actualizada')
    } catch (e) { console.error(e); showToast('❌ Error al actualizar') }
    saving = false
  }

  async function deletePqr() {
    if (!pqrAEliminar) return
    deleting = true
    try {
      await api.deletePqr(pqrAEliminar.id_pqr)
      pqrs = pqrs.filter(p => p.id_pqr !== pqrAEliminar.id_pqr)
      showToast('🗑️ PQR eliminada')
      pqrAEliminar = null
    } catch (e) { console.error(e); showToast('❌ Error al eliminar') }
    deleting = false
  }

  async function savePqr() {
    if (!formDescripcion || !formIdTipo || !formIdDepartamento) {
      showToast('⚠️ Completa todos los campos'); return
    }
    saving = true
    try {
      const payload = {
        descripcion: formDescripcion, id_tipo: formIdTipo,
        id_departamento: formIdDepartamento, id_pqr: 0,
        fecha: new Date().toISOString(), id_usuario: $currentUser?.id_usuario,
        id_estado: 1, id_prioridad: 1
      }
      await api.createPqr(payload)
      const data = await api.getPqrs()
      pqrs = Array.isArray(data) ? data : data.resultado || []
      showToast('✅ PQR enviada con éxito')
      view = 'list'
    } catch (e) { console.error(e); showToast('❌ Error al enviar') }
    saving = false
  }

  async function saveGestion() {
    if (!coordForm.id_estado) { showToast('⚠️ Selecciona un estado'); return }
    saving = true
    try {
      await api.updateEstadoPqr(selected.id_pqr, coordForm.id_estado)
      if (coordForm.id_responsable) {
        await api.createAsignacion({
          id_asignacion: 0, id_pqr: Number(selected.id_pqr),
          id_departamento: Number(coordForm.id_responsable),
          fecha_asignacion: new Date().toISOString().slice(0, 10)
        })
      }
      if (coordForm.respuesta.trim()) {
        await api.createRespuesta({
          id_pqr: selected.id_pqr, id_usuario: $currentUser?.id_usuario,
          mensaje: coordForm.respuesta.trim(), fecha: new Date().toISOString()
        })
      }
      const data = await api.getPqrs()
      pqrs = Array.isArray(data) ? data : data.resultado || []
      view = 'list'
      showToast('✅ PQR gestionada correctamente')
    } catch (e) { console.error(e); showToast('❌ Error al guardar') }
    saving = false
  }

  function limpiarFiltros() {
    searchText = ''; filterEstado = ''; filterTipo = ''
    filterDesde = ''; filterHasta = ''
    currentPage = 1
  }

  async function descargarPDF() {
    if (filtered.length === 0) return
    generando = true
    try {
      const { jsPDF }         = await import('https://esm.sh/jspdf@2.5.1')
      const { default: auto } = await import('https://esm.sh/jspdf-autotable@3.8.2')
      const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' })
      const W = 297

      doc.setFillColor(15, 23, 42)
      doc.rect(0, 0, W, 28, 'F')

      try {
        const b64 = await new Promise(res => {
          const r = new FileReader()
          r.onload = () => res(r.result)
          fetch(window.location.origin + '/logo_cul.png')
            .then(r => r.blob()).then(b => r.readAsDataURL(b))
        })
        doc.addImage(b64, 'PNG', 6, 3, 20, 20)
      } catch (_) {}

      doc.setTextColor(255,255,255)
      doc.setFontSize(13); doc.setFont('helvetica','bold')
      doc.text('Corporación Universitaria Latinoamericana', 30, 11)
      doc.setFontSize(9); doc.setFont('helvetica','normal')
      doc.setTextColor(148,163,184)
      doc.text('Sistema PQRS — Gestión de Solicitudes', 30, 18)
      doc.text(`Generado: ${new Date().toLocaleString('es-CO')}`, W - 14, 18, { align: 'right' })

      doc.setTextColor(100,116,139); doc.setFontSize(7.5)
      const fl = []
      if (searchText)   fl.push(`Búsqueda: "${searchText}"`)
      if (filterEstado) fl.push(`Estado: ${getLabelEstado(filterEstado)}`)
      if (filterTipo)   fl.push(`Categoría: ${getLabelTipo(filterTipo)}`)
      doc.text(`Filtros: ${fl.length ? fl.join('  ·  ') : 'Sin filtros'}   —   Total: ${filtered.length}`, 14, 33)

      auto(doc, {
        startY: 37,
        head: [['ID','Descripción','Categoría','Usuario','Departamento','Prioridad','Estado','Fecha']],
        body: filtered.map(p => [
          `#${p.id_pqr}`, p.descripcion?.slice(0,72) || '—',
          getLabelTipo(p.id_tipo), getLabelUsuario(p.id_usuario),
          getLabelDep(p.id_departamento), getLabelPrioridad(p.id_prioridad),
          getLabelEstado(p.id_estado), new Date(p.fecha).toLocaleDateString('es-CO')
        ]),
        headStyles: { fillColor:[37,99,235], textColor:255, fontSize:8.5, fontStyle:'bold' },
        bodyStyles: { fontSize:8, textColor:[51,65,85] },
        alternateRowStyles: { fillColor:[248,250,252] },
        margin: { left:14, right:14 },
        didDrawPage: ({ pageNumber }) => {
          doc.setFontSize(7); doc.setTextColor(148,163,184)
          doc.text(`Página ${pageNumber} de ${doc.internal.getNumberOfPages()}`, W/2, 205, { align:'center' })
        }
      })
      doc.save(`pqrs_reporte_${new Date().toISOString().slice(0,10)}.pdf`)
    } catch (e) { console.error(e) }
    generando = false
  }

  function showToast(msg) { toastMsg = msg; setTimeout(() => toastMsg = '', 3000) }

  const getLabelEstado    = (id) => estados.find(e => e.id_estado == id)?.nombre || 'PENDIENTE'
  const getLabelTipo      = (id) => tipos.find(t => t.id_tipo == id)?.nombre || '—'
  const getLabelDep       = (id) => departamentos.find(d => d.id_departamento == id)?.nombre || '—'
  const getLabelPrioridad = (id) => prioridades.find(p => p.id_prioridad == id)?.nombre || '—'
  const getLabelUsuario   = (id) => {
    const u = usuarios.find(u => u.id_usuario == id)
    return u ? (u.nombre || u.correo || `#${id}`) : `#${id}`
  }
</script>

<Modal
  bind:abierto={modalEliminarAbierto}
  titulo="¿Eliminar PQR #{pqrAEliminar?.id_pqr}?"
  mensaje="Esta acción no se puede deshacer. La solicitud será eliminada permanentemente."
  txtConfirm="Sí, eliminar"
  txtCancel="Cancelar"
  peligroso={true}
  onconfirm={deletePqr}
/>

<div class="module">
  {#if toastMsg}<div class="toast">{toastMsg}</div>{/if}

  <header class="page-header">
    <div class="header-content">
      <h1>
        {#if view === 'list'}{isAdmin ? 'Gestión de PQRs' : isCoord ? 'Gestión de PQRs' : 'Mis Solicitudes'}
        {:else if view === 'detail'}Detalle del Radicado
        {:else if view === 'edit'}Editar PQR
        {:else if view === 'gestion'}Gestionar PQR #{selected?.id_pqr}
        {:else}Nueva Solicitud{/if}
      </h1>
      <p class="subtitle">
        {isAdmin || isCoord ? 'Administra todas las solicitudes del sistema' : 'Gestiona y consulta el estado de tus trámites'}
      </p>
    </div>
    <div class="header-actions">
      {#if view === 'list'}
        {#if isAdmin}
          <button class="btn-pdf" onclick={descargarPDF} disabled={generando || filtered.length === 0}>
            {#if generando}
              <span class="spinner"></span> Generando...
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
              Descargar PDF ({filtered.length})
            {/if}
          </button>
        {/if}
        {#if isUser}
          <button class="btn-create" onclick={openCreate}>＋ Crear PQR</button>
        {/if}
      {:else}
        <button class="btn-back" onclick={() => view = 'list'}>← Volver</button>
      {/if}
    </div>
  </header>

  {#if view === 'list'}
    <div class="filters-card">
      <p class="filters-title">Filtros del reporte</p>
      <div class="filters-grid">
        <FormField label="Búsqueda" tipo="text" bind:valor={searchText} placeholder="Palabra clave..." />
        {#if isAdmin || isCoord}
          <FormField
            label="Estado" tipo="select" bind:valor={filterEstado}
            opciones={[{ value: '', label: 'Todos los estados' }, ...estados.map(e => ({ value: e.id_estado, label: e.nombre }))]}
          />
          <FormField
            label="Categoría" tipo="select" bind:valor={filterTipo}
            opciones={[{ value: '', label: 'Todas las categorías' }, ...tipos.map(t => ({ value: t.id_tipo, label: t.nombre }))]}
          />
          {#if isAdmin}
            <FormField label="Desde" tipo="date" bind:valor={filterDesde} />
            <FormField label="Hasta" tipo="date" bind:valor={filterHasta} />
          {/if}
          <div class="filter-end">
            <button class="btn-clear" onclick={limpiarFiltros}>Limpiar filtros</button>
          </div>
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
      <div class="loader-wrap"><p>Cargando solicitudes...</p></div>
    {:else}
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Descripción</th><th>Categoría</th>
              {#if isAdmin || isCoord}<th>Usuario</th><th>Estado</th>{/if}
              <th>Fecha</th><th class="text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#each paginated as pqr}
              <tr>
                <td><span class="id-tag">#{pqr.id_pqr}</span></td>
                <td class="text-main">{pqr.descripcion?.slice(0,40)}</td>
                <td><span class="type-chip">{getLabelTipo(pqr.id_tipo)}</span></td>
                {#if isAdmin || isCoord}
                  <td class="text-usuario">{getLabelUsuario(pqr.id_usuario)}</td>
                  <td><Badge texto={getLabelEstado(pqr.id_estado)} id={pqr.id_estado} /></td>
                {/if}
                <td class="date-text">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
                <td class="text-center actions-cell">
                  {#if isAdmin}
                    <button class="action-btn edit-btn" onclick={() => openEdit(pqr)} title="Editar">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    </button>
                    <button class="action-btn delete-btn" onclick={() => pedirEliminar(pqr)} title="Eliminar" disabled={deleting}>
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                    </button>
                  {:else if isCoord}
                    <button class="action-btn view-btn" onclick={() => openDetail(pqr)} title="Ver detalle">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    </button>
                    <button class="action-btn coord-btn" onclick={() => openGestion(pqr)} title="Gestionar">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
                    </button>
                  {:else}
                    <button class="action-btn view-btn" onclick={() => openDetail(pqr)} title="Ver detalle">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    </button>
                  {/if}
                </td>
              </tr>
            {/each}
            {#if paginated.length === 0}
              <tr><td colspan="7" class="empty-row">No se encontraron solicitudes</td></tr>
            {/if}
          </tbody>
        </table>

        <!-- Paginación -->
        {#if totalPages > 1}
          <div class="pagination">
            <button class="page-btn" onclick={() => currentPage = 1} disabled={currentPage === 1}>««</button>
            <button class="page-btn" onclick={() => currentPage--} disabled={currentPage === 1}>‹ Anterior</button>
            <span class="page-info">Página <strong>{currentPage}</strong> de <strong>{totalPages}</strong></span>
            <button class="page-btn" onclick={() => currentPage++} disabled={currentPage === totalPages}>Siguiente ›</button>
            <button class="page-btn" onclick={() => currentPage = totalPages} disabled={currentPage === totalPages}>»»</button>
          </div>
        {/if}
      </div>
    {/if}

  {:else if view === 'detail'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="card-top">
          <div class="badge-row">
            <span class="id-large">Solicitud #{selected.id_pqr}</span>
            <Badge texto={getLabelEstado(selected.id_estado)} id={selected.id_estado} />
          </div>
          <p class="date-sub">Registrado el {new Date(selected.fecha).toLocaleString('es-CO')}</p>
        </div>
        <div class="card-body">
          <div class="info-section">
            <p class="section-label">Descripción</p>
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
            <div class="info-item">
              <span class="label">Responsable Asignado</span>
              <span class="value">
  {#if responsable === null}
    <span style="color:#94a3b8; font-size:13px;">Cargando...</span>
  {:else if responsable === false}
    Sin asignar
  {:else}
    {responsable}
  {/if}
</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  {:else if view === 'gestion'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="card-top">
          <div class="badge-row">
            <span class="id-large">Solicitud #{selected.id_pqr}</span>
            <Badge texto={getLabelEstado(selected.id_estado)} id={selected.id_estado} />
          </div>
          <p class="date-sub">{getLabelUsuario(selected.id_usuario)} — {new Date(selected.fecha).toLocaleDateString('es-CO')}</p>
        </div>
        <div class="form-padding">
          <div class="info-section" style="margin-bottom:24px;">
            <p class="section-label">Descripción de la solicitud</p>
            <div class="content-box">{selected.descripcion}</div>
          </div>
          <h3 class="section-divider">Gestión del Coordinador</h3>
          <FormField label="Cambiar estado" tipo="select" bind:valor={coordForm.id_estado}
            placeholder="Selecciona un estado..."
            opciones={estados.map(e => ({ value: e.id_estado, label: e.nombre }))} />
          <FormField label="Asignar responsable" tipo="select" bind:valor={coordForm.id_responsable}
            placeholder="Selecciona un responsable..."
            opciones={departamentos.map(d => ({ value: d.id_departamento, label: d.nombre }))} />
          <FormField label="Respuesta / Comentario" tipo="textarea" bind:valor={coordForm.respuesta}
            placeholder="Escribe una respuesta o comentario para esta solicitud..."
            hint="Campo opcional" />
          <button class="btn-send" onclick={saveGestion} disabled={saving}>
            {saving ? 'Guardando...' : '✅ Guardar gestión'}
          </button>
        </div>
      </div>
    </div>

  {:else if view === 'edit'}
    <div class="center-container">
      <div class="card animate-up">
        <div class="form-padding">
          <h2 class="card-title">Editar PQR #{editForm.id_pqr}</h2>
          <FormField label="Descripción" tipo="textarea" bind:valor={editForm.descripcion} placeholder="Descripción de la solicitud..." />
          <div class="field-group">
            <FormField label="Tipo" tipo="select" bind:valor={editForm.id_tipo} placeholder="Selecciona..."
              opciones={tipos.map(t => ({ value: t.id_tipo, label: t.nombre }))} />
            <FormField label="Departamento" tipo="select" bind:valor={editForm.id_departamento} placeholder="Selecciona..."
              opciones={departamentos.map(d => ({ value: d.id_departamento, label: d.nombre }))} />
          </div>
          <div class="field-group">
            <FormField label="Estado" tipo="select" bind:valor={editForm.id_estado}
              opciones={estados.map(e => ({ value: e.id_estado, label: e.nombre }))} />
            <FormField label="Prioridad" tipo="select" bind:valor={editForm.id_prioridad}
              opciones={prioridades.map(p => ({ value: p.id_prioridad, label: p.nombre }))} />
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
          <FormField label="¿Qué sucedió? (Descripción)" tipo="textarea" bind:valor={formDescripcion}
            placeholder="Explica detalladamente tu solicitud..." required={true} />
          <div class="field-group">
            <FormField label="Tipo" tipo="select" bind:valor={formIdTipo} placeholder="Selecciona..."
              opciones={tipos.map(t => ({ value: t.id_tipo, label: t.nombre }))} required={true} />
            <FormField label="Departamento" tipo="select" bind:valor={formIdDepartamento} placeholder="Selecciona..."
              opciones={departamentos.map(d => ({ value: d.id_departamento, label: d.nombre }))} required={true} />
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
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -1px; }
  .subtitle { color: #64748b; font-size: 15px; margin-top: 4px; }
  .header-actions { display: flex; gap: 12px; align-items: center; }
  .btn-create { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37,99,235,0.2); font-family: inherit; }
  .btn-back   { background: white; border: 1.5px solid #e2e8f0; padding: 10px 20px; border-radius: 10px; color: #475569; font-weight: 700; cursor: pointer; font-family: inherit; }
  .btn-pdf { display: flex; align-items: center; gap: 8px; background: #dc2626; color: white; border: none; padding: 12px 22px; border-radius: 12px; font-weight: 700; font-size: 14px; cursor: pointer; transition: 0.2s; white-space: nowrap; box-shadow: 0 4px 14px rgba(220,38,38,0.25); font-family: inherit; }
  .btn-pdf:hover { background: #b91c1c; transform: translateY(-1px); }
  .btn-pdf:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }
  .spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; display: inline-block; animation: spin 0.7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .filters-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
  .filters-title { font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 16px; }
  .filters-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; align-items: end; }
  .filter-end { display: flex; align-items: flex-end; }
  .btn-clear { padding: 10px 16px; border-radius: 10px; border: 1.5px solid #e2e8f0; background: white; color: #64748b; font-size: 13px; font-weight: 600; cursor: pointer; transition: 0.2s; font-family: inherit; width: 100%; }
  .btn-clear:hover { border-color: #cbd5e1; background: #f8fafc; }

  .results-bar { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
  .results-count { font-size: 13px; color: #64748b; }
  .results-count strong { color: #0f172a; font-weight: 700; }
  .no-results-hint { font-size: 12px; color: #94a3b8; }

  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 14px 16px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #f1f5f9; white-space: nowrap; }
  td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; font-size: 13px; color: #334155; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafbff; }
  .empty-row { text-align: center; color: #94a3b8; padding: 40px !important; }
  .text-main { max-width: 300px; }
  .text-usuario { font-weight: 600; color: #1e293b; }
  .date-text { color: #64748b; font-size: 12px; white-space: nowrap; }

  .pagination { display: flex; align-items: center; justify-content: center; gap: 10px; padding: 16px; border-top: 1px solid #f1f5f9; }
  .page-btn { background: white; border: 1.5px solid #e2e8f0; padding: 8px 14px; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; color: #475569; transition: 0.2s; font-family: inherit; }
  .page-btn:hover:not(:disabled) { background: #2563eb; color: white; border-color: #2563eb; }
  .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .page-info { font-size: 13px; color: #64748b; padding: 0 8px; }

  .actions-cell { display: flex; align-items: center; justify-content: center; gap: 6px; }
  .action-btn { width: 32px; height: 32px; border: none; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
  .view-btn    { background: #eff6ff; color: #2563eb; }
  .view-btn:hover    { background: #2563eb; color: white; transform: scale(1.1); }
  .edit-btn    { background: #f0fdf4; color: #16a34a; }
  .edit-btn:hover    { background: #16a34a; color: white; transform: scale(1.1); }
  .delete-btn  { background: #fef2f2; color: #dc2626; }
  .delete-btn:hover  { background: #dc2626; color: white; transform: scale(1.1); }
  .delete-btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .coord-btn   { background: #fff7ed; color: #ea580c; }
  .coord-btn:hover   { background: #ea580c; color: white; transform: scale(1.1); }

  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; font-size: 12px; }
  .type-chip { background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 11px; white-space: nowrap; }

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
  .section-divider { font-size: 14px; font-weight: 700; color: #0f172a; margin: 0 0 20px; padding-bottom: 12px; border-bottom: 1px solid #f1f5f9; }
  .section-label { font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .btn-send { width: 100%; background: #2563eb; color: white; border: none; padding: 18px; border-radius: 16px; font-weight: 800; font-size: 16px; cursor: pointer; margin-top: 10px; font-family: inherit; }
  .btn-send:disabled { opacity: 0.6; cursor: not-allowed; }

  .toast { position: fixed; bottom: 30px; right: 30px; background: #0f172a; color: white; padding: 16px 28px; border-radius: 16px; font-weight: 600; z-index: 100; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
  .animate-up { animation: slideUp 0.4s ease-out; }
  @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
  .loader-wrap { padding: 60px; text-align: center; color: #94a3b8; }

  @media (max-width: 768px) {
    .module { padding: 16px; }
    .page-header { flex-direction: column; gap: 12px; align-items: flex-start; }
    .header-actions { width: 100%; }
    h1 { font-size: 22px; }
    .filters-grid { grid-template-columns: 1fr; }
    table { min-width: 600px; }
    th, td { padding: 10px 12px; font-size: 11px; }
    .form-padding, .card-top, .card-body { padding: 24px; }
    .field-group { grid-template-columns: 1fr; }
    .info-grid { grid-template-columns: 1fr; }
    .pagination { flex-wrap: wrap; }
  }
</style>