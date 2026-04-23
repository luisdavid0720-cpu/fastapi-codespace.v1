<script>
  let {
    abierto    = $bindable(false),
    titulo     = '¿Estás seguro?',
    mensaje    = '',
    txtConfirm = 'Confirmar',
    txtCancel  = 'Cancelar',
    peligroso  = false,
    onconfirm  = () => {},
    children
  } = $props()

  function cerrar() { abierto = false }
  function confirmar() { onconfirm(); cerrar() }
</script>

{#if abierto}
  <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
  <div class="overlay" onclick={(e) => { if(e.target === e.currentTarget) cerrar() }}>
    <div class="modal">
      <button class="close-btn" onclick={cerrar}>✕</button>

      <h3 class="modal-title">{titulo}</h3>

      {#if mensaje}
        <p class="modal-msg">{mensaje}</p>
      {:else}
        {@render children?.()}
      {/if}

      <div class="modal-footer">
        <button class="btn-cancel" onclick={cerrar}>{txtCancel}</button>
        <button
          class="btn-confirm {peligroso ? 'peligroso' : ''}"
          onclick={confirmar}
        >{txtConfirm}</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.55);
    display: flex; align-items: center; justify-content: center;
    z-index: 9999; backdrop-filter: blur(3px);
    animation: fadeIn 0.15s ease;
  }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

  .modal {
    background: white; border-radius: 24px; padding: 36px;
    max-width: 440px; width: calc(100% - 32px); position: relative;
    box-shadow: 0 30px 60px rgba(0,0,0,0.18);
    animation: slideUp 0.2s ease;
  }
  @keyframes slideUp { from { transform: translateY(12px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

  .close-btn {
    position: absolute; top: 16px; right: 16px;
    background: #f1f5f9; border: none; color: #94a3b8;
    width: 28px; height: 28px; border-radius: 8px;
    cursor: pointer; font-size: 13px; transition: 0.2s;
  }
  .close-btn:hover { background: #e2e8f0; color: #475569; }

  .modal-title { font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 10px; }
  .modal-msg   { color: #64748b; font-size: 14px; line-height: 1.6; margin: 0 0 28px; }

  .modal-footer { display: flex; gap: 10px; justify-content: flex-end; margin-top: 28px; }

  .btn-cancel {
    padding: 10px 22px; border-radius: 10px; border: 1.5px solid #e2e8f0;
    background: white; color: #64748b; font-family: inherit;
    font-size: 14px; font-weight: 600; cursor: pointer; transition: 0.2s;
  }
  .btn-cancel:hover { background: #f8fafc; }

  .btn-confirm {
    padding: 10px 22px; border-radius: 10px; border: none;
    background: #2563eb; color: white; font-family: inherit;
    font-size: 14px; font-weight: 700; cursor: pointer; transition: 0.2s;
  }
  .btn-confirm:hover { background: #1d4ed8; }
  .btn-confirm.peligroso { background: #dc2626; }
  .btn-confirm.peligroso:hover { background: #b91c1c; }
</style>
