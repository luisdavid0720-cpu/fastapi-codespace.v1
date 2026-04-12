<script>
  let { children } = $props()

  import { currentUser } from '../stores/auth.js';
  import Login from '../lib/componentes/Login.svelte';
  import Dashboard from '../lib/componentes/Dashboard.svelte';
  import Footer from '../lib/componentes/Footer.svelte';

  let page = $state('home')
</script>

<div class="app">
  {#if $currentUser}
    <div class="content">
      <Dashboard bind:page />
      {@render children()}
    </div>
    <Footer />
  {:else}
    <Login />
  {/if}
</div>

<style>
  :global(*) {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  :global(:root) {
    --bg: #eef0f4;
    --text: #1a1a2e;
    --font-body: 'DM Sans', sans-serif;
  }

  :global(body) {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    min-height: 100vh;
  }

  /* 🔥 Layout correcto */
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
</style>