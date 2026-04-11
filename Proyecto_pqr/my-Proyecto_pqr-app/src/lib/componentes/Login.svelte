<script>
  // En el futuro, aquí manejarás la lógica de autenticación
  // import { login } from '../stores/auth.js';
  
  // Para la demostración visual, simularemos la navegación
  let isLoggingIn = false;

  function simulateLogin(role) {
    isLoggingIn = true;
    // Aquí, más adelante, llamarás a tu API de FastAPI
    console.log(`Intentando iniciar sesión como: ${role}`);
    
    // Simulamos un retraso de red
    setTimeout(() => {
      isLoggingIn = false;
      alert(`Simulación: Sesión iniciada como ${role}. Serías redirigido al Dashboard.`);
      // window.location.href = '/dashboard'; // Redirección real futura
    }, 1500);
  }
</script>

<div class="login-container">
  <div class="brand-section">
    <div class="brand-content">
      <div class="logo-container">
        <svg width="60" height="60" viewBox="0 0 40 40" fill="none">
          <circle cx="20" cy="20" r="18" fill="#fff" stroke="#facc15" stroke-width="2"/>
          <path d="M12 12C12 12 14.5 9.5 20 9.5C25.5 9.5 28 12 28 12M12 28C12 28 14.5 30.5 20 30.5C25.5 30.5 28 28 28 28" stroke="#1d4ed8" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M20 9.5V30.5" stroke="#1d4ed8" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
      </div>
      
      <h1 class="brand-title">Universidad CUL</h1>
      <p class="brand-subtitle">Corporación Universitaria Latinoamericana</p>
      
      <div class="system-badge">
        <span class="badge-icon">◈</span>
        <span class="badge-text">Sistema de Gestión PQRS</span>
      </div>
    </div>
    
    <div class="decorative-blob"></div>
  </div>

  <div class="login-section">
    <div class="login-card">
      <div class="login-header">
        <h2>Bienvenido</h2>
        <p>Selecciona tu tipo de acceso para continuar</p>
      </div>

      <div class="role-selector">
        <button 
          class="role-btn admin-btn" 
          onclick={() => simulateLogin('admin')}
          disabled={isLoggingIn}
        >
          <div class="role-icon-wrapper">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <div class="role-text">
            <h3>Administrador</h3>
            <p>Acceso completo al sistema y analítica</p>
          </div>
          <div class="arrow-icon">→</div>
        </button>

        <button 
          class="role-btn user-btn" 
          onclick={() => simulateLogin('user')}
          disabled={isLoggingIn}
        >
          <div class="role-icon-wrapper">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <div class="role-text">
            <h3>Usuario</h3>
            <p>Gestión de PQRs propias</p>
          </div>
          <div class="arrow-icon">→</div>
        </button>
      </div>

      {#if isLoggingIn}
        <div class="loading-state">
          <div class="spinner"></div>
          <span>Iniciando sesión...</span>
        </div>
      {/if}
      
      <div class="login-footer">
        <p>¿Problemas para acceder? <a href="#">Contactar soporte</a></p>
      </div>
    </div>
  </div>
</div>

<style>
  /* CONFIGURACIÓN BASE DEL LAYOUT SPLIT */
  :global(body) {
    margin: 0;
    font-family: 'Inter', system-ui, sans-serif;
  }

  .login-container {
    display: flex;
    min-height: 100vh;
    width: 100%;
    background-color: #f8fafc;
  }

  /* --- LADO IZQUIERDO: BRANDING --- */
  .brand-section {
    flex: 1;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }

  .brand-content {
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 40px;
    max-width: 400px;
  }

  .logo-container {
    margin-bottom: 24px;
    display: inline-block;
    padding: 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    backdrop-filter: blur(10px);
  }

  .brand-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -1px;
    color: #f8fafc;
  }

  .brand-subtitle {
    font-size: 1rem;
    color: #94a3b8;
    margin: 0 0 32px 0;
    line-height: 1.5;
  }

  .system-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(37, 99, 235, 0.3);
    padding: 8px 16px;
    border-radius: 100px;
  }

  .badge-icon { color: #60a5fa; }
  .badge-text { font-size: 0.85rem; font-weight: 600; color: #bfdbfe; letter-spacing: 0.5px;}

  /* Detalle decorativo sutil en el fondo */
  .decorative-blob {
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(37,99,235,0.1) 0%, rgba(15,23,42,0) 70%);
    top: -100px;
    left: -100px;
    border-radius: 50%;
    z-index: 1;
  }

  /* --- LADO DERECHO: LOGIN FORM --- */
  .login-section {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    background-color: #ffffff;
  }

  .login-card {
    width: 100%;
    max-width: 440px;
  }

  .login-header {
    margin-bottom: 40px;
  }

  .login-header h2 {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
  }

  .login-header p {
    color: #64748b;
    font-size: 1rem;
    margin: 0;
  }

  /* --- BOTONES DE SELECCIÓN DE ROL --- */
  .role-selector {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .role-btn {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  }

  .role-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .role-btn:hover:not(:disabled) {
    border-color: #2563eb;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.1);
    transform: translateY(-2px);
  }

  /* Colores específicos de los iconos */
  .admin-btn .role-icon-wrapper {
    background: #eff6ff;
    color: #2563eb;
  }
  
  .user-btn .role-icon-wrapper {
    background: #f8fafc;
    color: #64748b;
  }

  .role-btn:hover .admin-btn .role-icon-wrapper { background: #2563eb; color: white; }
  .role-btn:hover .user-btn .role-icon-wrapper { background: #334155; color: white; }

  .role-icon-wrapper {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.3s ease;
  }

  .role-text { flex: 1; }

  .role-text h3 {
    margin: 0 0 4px 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
  }

  .role-text p {
    margin: 0;
    font-size: 0.85rem;
    color: #64748b;
  }

  .arrow-icon {
    color: #cbd5e1;
    font-size: 1.2rem;
    font-weight: bold;
    transition: transform 0.2s;
  }

  .role-btn:hover:not(:disabled) .arrow-icon {
    color: #2563eb;
    transform: translateX(4px);
  }

  /* --- ESTADOS DE CARGA Y FOOTER --- */
  .loading-state {
    margin-top: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: #2563eb;
    font-weight: 600;
    font-size: 0.9rem;
    background: #eff6ff;
    padding: 12px;
    border-radius: 8px;
  }

  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid #bfdbfe;
    border-top-color: #2563eb;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .login-footer {
    margin-top: 40px;
    text-align: center;
    font-size: 0.85rem;
    color: #64748b;
  }

  .login-footer a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
  }

  .login-footer a:hover { text-decoration: underline; }

  /* --- RESPONSIVIDAD --- */
  @media (max-width: 900px) {
    .login-container { flex-direction: column; }
    .brand-section { padding: 40px 20px; flex: none; }
    .decorative-blob { display: none; }
    .brand-content { padding: 0; }
    .login-section { padding: 32px 20px; align-items: flex-start; }
  }
</style>