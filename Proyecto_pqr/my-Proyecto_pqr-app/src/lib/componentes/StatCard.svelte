<script>
  // color: 'blue' | 'green' | 'yellow' | 'red'
  let {
    label  = '',
    valor  = 0,
    delta  = '',
    subida = true,
    color  = 'blue'
  } = $props()
</script>
 
<div class="stat-card color-{color}">
  <p class="stat-label">{label}</p>
  <p class="stat-valor">{valor}</p>
  {#if delta}
    <p class="stat-delta {subida ? 'up' : 'down'}">
      {subida ? '↑' : '↓'} {delta}
    </p>
  {/if}
</div>
 
<style>
  .stat-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 22px; position: relative; overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  }
  .stat-card::after {
    content: ''; position: absolute; bottom: -16px; right: -16px;
    width: 70px; height: 70px; border-radius: 50%; opacity: 0.08;
  }
  .color-blue::after  { background: #2563eb; }
  .color-green::after { background: #16a34a; }
  .color-yellow::after{ background: #f59e0b; }
  .color-red::after   { background: #dc2626; }
 
  .stat-label {
    font-size: 11px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.5px; margin: 0 0 6px; color: #94a3b8;
  }
  .stat-valor { font-size: 2rem; font-weight: 800; margin: 0; letter-spacing: -1px; }
  .color-blue  .stat-valor { color: #2563eb; }
  .color-green .stat-valor { color: #16a34a; }
  .color-yellow .stat-valor { color: #f59e0b; }
  .color-red   .stat-valor { color: #dc2626; }
 
  .stat-delta { font-size: 12px; margin: 4px 0 0; font-weight: 500; }
  .up   { color: #16a34a; }
  .down { color: #dc2626; }
</style>