<script>
  // tipo: 'card' | 'tabla' | 'perfil' | 'linea'
  // cantidad: cuántas filas mostrar (para tipo='tabla')
  let { tipo = 'card', cantidad = 3 } = $props()
</script>
 
{#if tipo === 'card'}
  <div class="sk-card">
    <div class="sk-row">
      <div class="sk sk-line" style="width:70px"></div>
      <div class="sk sk-line" style="width:90px;border-radius:999px"></div>
    </div>
    <div class="sk sk-line" style="width:100%;margin-top:12px"></div>
    <div class="sk sk-line" style="width:75%"></div>
    <div class="sk-row" style="margin-top:14px">
      <div class="sk sk-line" style="width:80px"></div>
      <div class="sk sk-line" style="width:70px"></div>
    </div>
  </div>
 
{:else if tipo === 'tabla'}
  {#each Array.from({ length: cantidad }) as _}
    <div class="sk-fila">
      <div class="sk sk-line" style="width:50px"></div>
      <div class="sk sk-line" style="width:200px"></div>
      <div class="sk sk-line" style="width:80px;border-radius:999px"></div>
      <div class="sk sk-line" style="width:60px"></div>
    </div>
  {/each}
 
{:else if tipo === 'perfil'}
  <div class="sk-perfil">
    <div class="sk sk-circle"></div>
    <div style="flex:1">
      <div class="sk sk-title" style="width:55%"></div>
      <div class="sk sk-line" style="width:80%"></div>
      <div class="sk sk-line" style="width:60%"></div>
    </div>
  </div>
 
{:else}
  <div class="sk sk-line" style="width:100%"></div>
{/if}
 
<style>
  @keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position:  400px 0; }
  }
 
  .sk {
    background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
    background-size: 800px 100%;
    animation: shimmer 1.4s infinite linear;
    border-radius: 6px;
  }
  .sk-line   { height: 14px; margin-bottom: 8px; }
  .sk-title  { height: 20px; margin-bottom: 10px; }
  .sk-circle { width: 42px; height: 42px; border-radius: 50%; flex-shrink: 0; }
 
  .sk-card {
    background: white; border: 1px solid #e2e8f0;
    border-radius: 16px; padding: 20px;
  }
  .sk-row { display: flex; gap: 10px; align-items: center; }
  .sk-fila { display: flex; gap: 20px; align-items: center; padding: 14px 0; border-bottom: 1px solid #f1f5f9; }
  .sk-perfil { display: flex; gap: 14px; align-items: flex-start; background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; }
</style>