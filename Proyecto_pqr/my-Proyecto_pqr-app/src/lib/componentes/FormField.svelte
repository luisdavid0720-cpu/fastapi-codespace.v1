<script>
  // tipo: 'text' | 'email' | 'password' | 'date' | 'select' | 'textarea' | 'number'
  let {
    label    = '',
    tipo     = 'text',
    valor    = $bindable(''),
    opciones = [],         // para tipo='select': [{value, label}]
    placeholder = '',
    error    = '',
    hint     = '',
    required = false,
    disabled = false
  } = $props()
</script>

<div class="field">
  {#if label}
    <label class="field-label">
      {label}
      {#if required}<span class="req">*</span>{/if}
    </label>
  {/if}

  {#if tipo === 'select'}
    <select class="field-input {error ? 'has-error' : ''}" bind:value={valor} {disabled}>
      <option value="">{placeholder || 'Selecciona...'}</option>
      {#each opciones as op}
        <option value={op.value}>{op.label}</option>
      {/each}
    </select>

  {:else if tipo === 'textarea'}
    <textarea
      class="field-input field-textarea {error ? 'has-error' : ''}"
      bind:value={valor}
      {placeholder} {disabled}
    ></textarea>

  {:else}
    <input
      class="field-input {error ? 'has-error' : ''}"
      type={tipo}
      bind:value={valor}
      {placeholder} {disabled}
    />
  {/if}

  {#if error}
    <span class="field-error">⚠ {error}</span>
  {:else if hint}
    <span class="field-hint">{hint}</span>
  {/if}
</div>

<style>
  .field { display: flex; flex-direction: column; gap: 7px; }

  .field-label {
    font-size: 11px; font-weight: 800; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.5px;
  }
  .req { color: #dc2626; margin-left: 2px; }

  .field-input {
    padding: 12px 14px; border-radius: 12px;
    border: 1.5px solid #e2e8f0; background: #fcfcfc;
    font-size: 14px; font-family: inherit; color: #334155;
    outline: none; transition: border-color 0.2s, box-shadow 0.2s;
    width: 100%; box-sizing: border-box;
  }
  .field-input:focus { border-color: #2563eb; background: white; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
  .field-input.has-error { border-color: #dc2626; box-shadow: 0 0 0 3px rgba(220,38,38,0.1); }
  .field-input:disabled { opacity: 0.6; cursor: not-allowed; }

  .field-textarea { min-height: 110px; resize: none; }

  .field-error { font-size: 12px; color: #dc2626; font-weight: 500; }
  .field-hint  { font-size: 12px; color: #94a3b8; }
</style>
