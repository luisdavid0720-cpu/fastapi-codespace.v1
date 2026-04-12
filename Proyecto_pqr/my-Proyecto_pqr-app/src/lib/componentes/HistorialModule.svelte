<script>
  import { onMount } from 'svelte'
  import { api } from '../api.js'

  let pqrs         = $state([])
  let tipos        = $state([])
  let estados      = $state([])
  let departamentos= $state([])
  let prioridades  = $state([])
  let usuarios     = $state([])
  let loading      = $state(true)
  let generando    = $state(false)

  let searchText   = $state('')
  let filterEstado = $state('')
  let filterTipo   = $state('')
  let filterDesde  = $state('')
  let filterHasta  = $state('')

  onMount(async () => {
    loading = true
    try {
      const [p, t, e, d, pr, u] = await Promise.allSettled([
        api.getPqrs(), api.getTiposPqr(), api.getEstados(),
        api.getDepartamentos(), api.getPrioridades(), api.getUsuarios()
      ])
      pqrs          = p.value?.resultado  || []
      tipos         = t.value             || []
      estados       = e.value             || []
      departamentos = d.value             || []
      prioridades   = pr.value            || []
      usuarios      = u.value?.resultado  || u.value || []
    } catch(e) { console.error(e) }
    loading = false
  })

  const getLabelEstado    = (id) => estados.find(e => e.id_estado == id)?.nombre            || '—'
  const getLabelTipo      = (id) => tipos.find(t => t.id_tipo == id)?.nombre                 || '—'
  const getLabelDep       = (id) => departamentos.find(d => d.id_departamento == id)?.nombre || '—'
  const getLabelPrioridad = (id) => prioridades.find(p => p.id_prioridad == id)?.nombre      || '—'
  const getLabelUsuario   = (id) => {
    const u = usuarios.find(u => u.id_usuario == id)
    return u ? (u.nombre || u.correo || `#${id}`) : `#${id}`
  }

  const prioColor = (id) => {
    const n = getLabelPrioridad(id)?.toLowerCase()
    if (n.includes('muy') || n.includes('urgen') || n.includes('crít')) return 'prio-alta'
    if (n.includes('alta')) return 'prio-alta'
    if (n.includes('media')) return 'prio-media'
    return 'prio-baja'
  }

  let filtrado = $derived(
    pqrs
      .filter(p => {
        const matchText   = !searchText   || p.descripcion?.toLowerCase().includes(searchText.toLowerCase())
        const matchEstado = !filterEstado || String(p.id_estado) === String(filterEstado)
        const matchTipo   = !filterTipo   || String(p.id_tipo)   === String(filterTipo)
        const fecha       = new Date(p.fecha)
        const matchDesde  = !filterDesde  || fecha >= new Date(filterDesde)
        const matchHasta  = !filterHasta  || fecha <= new Date(filterHasta + 'T23:59:59')
        return matchText && matchEstado && matchTipo && matchDesde && matchHasta
      })
      .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
  )

  function limpiarFiltros() {
    searchText = ''; filterEstado = ''; filterTipo = ''
    filterDesde = ''; filterHasta = ''
  }

  async function descargarPDF() {
    if (filtrado.length === 0) return
    generando = true
    try {
      const { jsPDF }         = await import('https://esm.sh/jspdf@2.5.1')
      const { default: auto } = await import('https://esm.sh/jspdf-autotable@3.8.2')

      const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' })
      const W = 297

      // ── Encabezado azul ──────────────────────────────────────────
      doc.setFillColor(15, 23, 42)
      doc.rect(0, 0, W, 28, 'F')

      // Logo (si existe como base64 en /logo_cul.png, lo cargamos)
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
      doc.text('Sistema PQRS — Historial de Solicitudes', 30, 18)

      const ahora = new Date().toLocaleString('es-CO')
      doc.setTextColor(148, 163, 184)
      doc.setFontSize(8)
      doc.text(`Generado: ${ahora}`, W - 14, 18, { align: 'right' })

      // ── Resumen de filtros ────────────────────────────────────────
      doc.setTextColor(100, 116, 139)
      doc.setFontSize(7.5)
      const fl = []
      if (searchText)   fl.push(`Búsqueda: "${searchText}"`)
      if (filterEstado) fl.push(`Estado: ${getLabelEstado(filterEstado)}`)
      if (filterTipo)   fl.push(`Categoría: ${getLabelTipo(filterTipo)}`)
      if (filterDesde)  fl.push(`Desde: ${filterDesde}`)
      if (filterHasta)  fl.push(`Hasta: ${filterHasta}`)
      const flLabel = fl.length ? fl.join('  ·  ') : 'Sin filtros'
      doc.text(`Filtros: ${flLabel}   —   Total registros: ${filtrado.length}`, 14, 33)

      // ── Tabla ─────────────────────────────────────────────────────
      auto(doc, {
        startY: 37,
        head: [[
          { content: 'ID',           styles: { halign: 'center', cellWidth: 12 } },
          { content: 'Descripción',  styles: { cellWidth: 58 } },
          { content: 'Categoría',    styles: { cellWidth: 26 } },
          { content: 'Usuario',      styles: { cellWidth: 36 } },
          { content: 'Departamento', styles: { cellWidth: 34 } },
          { content: 'Prioridad',    styles: { halign: 'center', cellWidth: 22 } },
          { content: 'Estado',       styles: { halign: 'center', cellWidth: 26 } },
          { content: 'Fecha',        styles: { halign: 'center', cellWidth: 22 } },
        ]],
        body: filtrado.map(p => [
          `#${p.id_pqr}`,
          p.descripcion?.slice(0, 75) || '—',
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
      doc.save(`historial_pqrs_${fecha}.pdf`)
    } catch(e) {
      console.error(e)
    }
    generando = false
  }
</script>

<div class="module">

  <!-- Encabezado del módulo -->
  <header class="page-header">
    <div>
      <h1>Historial de PQRs</h1>
      <p class="subtitle">Genera y descarga reportes filtrados en formato PDF</p>
    </div>
    <button class="btn-pdf" onclick={descargarPDF} disabled={generando || filtrado.length === 0}>
      {#if generando}
        <span class="spinner"></span> Generando PDF...
      {:else}
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="12" y1="18" x2="12" y2="12"/>
          <line x1="9" y1="15" x2="15" y2="15"/>
        </svg>
        Descargar PDF ({filtrado.length})
      {/if}
    </button>
  </header>

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
    </div>
  </div>

  <!-- Contador -->
  <div class="results-bar">
    <span class="results-count">
      <strong>{filtrado.length}</strong> {filtrado.length === 1 ? 'registro' : 'registros'} encontrados
    </span>
    {#if filtrado.length === 0 && !loading}
      <span class="no-results-hint">Ajusta los filtros para ver resultados</span>
    {/if}
  </div>

  <!-- Vista previa -->
  {#if loading}
    <div class="loader-wrap"><p>Cargando datos...</p></div>
  {:else}
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Descripción</th>
            <th>Categoría</th>
            <th>Usuario</th>
            <th>Departamento</th>
            <th>Prioridad</th>
            <th>Estado</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {#each filtrado as pqr}
            <tr>
              <td><span class="id-tag">#{pqr.id_pqr}</span></td>
              <td class="desc-cell">{pqr.descripcion?.slice(0, 50)}{pqr.descripcion?.length > 50 ? '...' : ''}</td>
              <td><span class="type-chip">{getLabelTipo(pqr.id_tipo)}</span></td>
              <td class="text-usuario">{getLabelUsuario(pqr.id_usuario)}</td>
              <td class="text-dep">{getLabelDep(pqr.id_departamento)}</td>
              <td><span class="prio-chip {prioColor(pqr.id_prioridad)}">{getLabelPrioridad(pqr.id_prioridad)}</span></td>
              <td><span class="status-pill s{pqr.id_estado}">{getLabelEstado(pqr.id_estado)}</span></td>
              <td class="date-text">{new Date(pqr.fecha).toLocaleDateString('es-CO')}</td>
            </tr>
          {/each}
          {#if filtrado.length === 0}
            <tr><td colspan="8" class="empty-row">No hay registros con los filtros aplicados</td></tr>
          {/if}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .module { padding: 40px; font-family: 'Inter', sans-serif; background: #fcfdfe; min-height: 100vh; }

  /* Header */
  .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; }
  h1 { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -1px; }
  .subtitle { color: #64748b; font-size: 15px; margin: 4px 0 0; }

  .btn-pdf {
    display: flex; align-items: center; gap: 8px;
    background: #dc2626; color: white; border: none;
    padding: 13px 22px; border-radius: 12px; font-weight: 700;
    font-size: 14px; cursor: pointer; transition: 0.2s; white-space: nowrap;
    box-shadow: 0 4px 14px rgba(220,38,38,0.25); font-family: inherit;
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
  .input-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: #94a3b8; pointer-events: none; }
  .input-wrap input { padding-left: 32px; }

  .filter-field input, .filter-field select {
    padding: 10px 12px; border-radius: 10px; border: 1.5px solid #e2e8f0;
    font-size: 13px; outline: none; background: #fafafa; font-family: inherit;
    color: #334155; transition: border-color 0.2s; width: 100%; box-sizing: border-box;
  }
  .filter-field input:focus, .filter-field select:focus { border-color: #2563eb; background: white; }

  .btn-clear { padding: 10px 16px; border-radius: 10px; border: 1.5px solid #e2e8f0; background: white; color: #64748b; font-size: 13px; font-weight: 600; cursor: pointer; transition: 0.2s; font-family: inherit; width: 100%; }
  .btn-clear:hover { border-color: #cbd5e1; background: #f8fafc; }

  /* Barra resultados */
  .results-bar { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
  .results-count { font-size: 13px; color: #64748b; }
  .results-count strong { color: #0f172a; font-weight: 700; }
  .no-results-hint { font-size: 12px; color: #94a3b8; }

  /* Tabla */
  .table-container { background: white; border-radius: 20px; border: 1px solid #e2e8f0; overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
  table { width: 100%; border-collapse: collapse; }
  th { background: #f8fafc; padding: 13px 16px; text-align: left; font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #f1f5f9; white-space: nowrap; }
  td { padding: 13px 16px; border-bottom: 1px solid #f1f5f9; font-size: 13px; color: #334155; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafbff; }
  .empty-row { text-align: center; color: #94a3b8; padding: 48px !important; font-size: 14px; }

  .id-tag { color: #94a3b8; font-weight: 700; font-family: monospace; font-size: 12px; }
  .desc-cell { max-width: 280px; }
  .text-usuario { font-weight: 600; color: #1e293b; }
  .text-dep { color: #475569; font-size: 12px; }
  .date-text { color: #64748b; font-size: 12px; white-space: nowrap; }

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

  .loader-wrap { padding: 60px; text-align: center; color: #94a3b8; }

  @media (max-width: 768px) {
    .module { padding: 16px; }
    .page-header { flex-direction: column; gap: 14px; align-items: flex-start; }
    .btn-pdf { width: 100%; justify-content: center; }
    .filters-grid { grid-template-columns: 1fr; }
    h1 { font-size: 22px; }
    table { min-width: 700px; }
    th, td { padding: 10px 12px; font-size: 11px; }
  }
</style>
