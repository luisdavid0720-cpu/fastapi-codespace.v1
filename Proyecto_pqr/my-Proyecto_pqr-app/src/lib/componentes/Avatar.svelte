<script>
  // nombre: string — se toman las iniciales automáticamente
  // size: 'sm' | 'md' | 'lg'
  // showName: boolean — mostrar nombre al lado
  // rol: string — se muestra debajo del nombre
  let {
    nombre   = '?',
    size     = 'md',
    showName = false,
    rol      = ''
  } = $props()

  // Colores por índice de la primera letra
  const colores = ['#2563eb','#16a34a','#dc2626','#f59e0b','#7c3aed','#0891b2']
  const iniciales = nombre
    .split(' ').slice(0,2)
    .map(p => p[0]?.toUpperCase() || '')
    .join('')

  const colorIdx = (nombre.charCodeAt(0) || 0) % colores.length
  const color = colores[colorIdx]
</script>

<div class="avatar-wrap">
  <div
    class="avatar avatar-{size}"
    style="background: {color}"
  >{iniciales}</div>

  {#if showName}
    <div class="avatar-info">
      <span class="av-nombre">{nombre}</span>
      {#if rol}<span class="av-rol">{rol}</span>{/if}
    </div>
  {/if}
</div>

<style>
  .avatar-wrap { display: inline-flex; align-items: center; gap: 10px; }

  .avatar {
    border-radius: 50%; color: white; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; letter-spacing: -0.5px;
  }
  .avatar-sm { width: 28px; height: 28px; font-size: 10px; }
  .avatar-md { width: 36px; height: 36px; font-size: 13px; }
  .avatar-lg { width: 48px; height: 48px; font-size: 17px; }

  .av-nombre { font-size: 13px; font-weight: 600; color: #1e293b; display: block; }
  .av-rol    { font-size: 11px; color: #94a3b8; display: block; }
</style>
