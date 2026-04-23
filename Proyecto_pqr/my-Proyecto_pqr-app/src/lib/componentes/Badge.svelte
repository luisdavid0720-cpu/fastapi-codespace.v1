<script>
  // tipo: 'estado' | 'prioridad'
  // valor: nombre del estado o prioridad (ej: 'Pendiente', 'Alta')
  // id_estado: número (1=Pendiente, 2=En proceso, 3=Resuelto, 4=Rechazado)
  let { texto = '', id = null } = $props()

  const colorPorId = {
    1: 's1', 2: 's2', 3: 's3', 4: 's4', 5: 's5'
  }

  function getClase(texto, id) {
    if (id) return colorPorId[id] || 's1'
    const t = texto?.toLowerCase() || ''
    if (t.includes('pendiente'))   return 's1'
    if (t.includes('proceso'))     return 's2'
    if (t.includes('resuelto'))    return 's3'
    if (t.includes('rechazado'))   return 's4'
    if (t.includes('alta') || t.includes('urgente')) return 'prio-alta'
    if (t.includes('media'))       return 'prio-media'
    if (t.includes('baja'))        return 'prio-baja'
    return 's1'
  }
</script>

<span class="badge {getClase(texto, id)}">{texto}</span>

<style>
  .badge {
    display: inline-block; padding: 4px 12px; border-radius: 100px;
    font-size: 10px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.3px; white-space: nowrap;
  }
  .s1 { background: #fef3c7; color: #92400e; }
  .s2 { background: #dbeafe; color: #1e40af; }
  .s3 { background: #d1fae5; color: #065f46; }
  .s4 { background: #fee2e2; color: #991b1b; }
  .s5 { background: #e0e7ff; color: #3730a3; }
  .prio-alta  { background: #fef2f2; color: #dc2626; }
  .prio-media { background: #fff7ed; color: #c2410c; }
  .prio-baja  { background: #f0fdf4; color: #16a34a; }
</style>
