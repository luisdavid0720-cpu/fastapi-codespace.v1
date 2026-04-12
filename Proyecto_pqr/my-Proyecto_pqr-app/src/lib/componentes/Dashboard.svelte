.layout { display: flex; height: 100vh; overflow: hidden; }

.sidebar {
  width: 240px; min-width: 240px;
  background: linear-gradient(180deg, #000, #111);
  color: #fff; display: flex; flex-direction: column;
  justify-content: space-between; padding: 24px 16px; height: 100vh;
}

.brand {
  display: flex; align-items: center; gap: 10px;
  padding: 0 8px 28px; border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 20px;
}
.brand-text { font-weight: 700; font-size: 16px; letter-spacing: -0.02em; }

nav { display: flex; flex-direction: column; gap: 4px; }

.nav-item {
  display: flex; align-items: center; gap: 10px; padding: 12px;
  border-radius: 8px; border: none; background: transparent; color: #ccc;
  font-size: 14px; font-weight: 500; transition: all 0.2s ease;
  text-align: left; width: 100%; cursor: pointer;
}
.nav-item:hover  { background: rgba(255,255,255,0.05); color: #fff; }
.nav-item.active { background: #2563eb; color: #fff; }

.sidebar-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 16px; display: flex; flex-direction: column; gap: 12px;
}

.user-card { display: flex; align-items: center; gap: 10px; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 8px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #2563eb; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.user-name { font-size: 13px; font-weight: 600; color: #fff; margin: 0; }
.user-role { font-size: 11px; color: #aaa; margin: 0; }

.btn-logout {
  display: flex; align-items: center; gap: 8px; padding: 10px 12px;
  border-radius: 8px; border: 1px solid rgba(255,255,255,0.11);
  background: rgba(255,255,255,0.05); color: #ddd; cursor: pointer;
  font-size: 14px; font-family: inherit; transition: 0.2s;
}
.btn-logout:hover { background: rgba(255,255,255,0.1); }

/* 🔥 FIX PRINCIPAL */
.main { 
  flex: 1; 
  background: #f4f6f9; 
  display: flex; 
  flex-direction: column; 
  min-height: 0; 
}

.full-width-module { width: 100%; box-sizing: border-box; display: flex; flex-direction: column; }

.scrollable-content { 
  overflow-y: auto; 
  padding: 24px 24px 40px 24px; 
  flex: 1; 
}

/* 🔥 ANALÍTICA CORREGIDA */
.analitica-wrapper  { 
  flex: 1; 
  padding: 16px; 
  display: flex;
  flex-direction: column;
}

.powerbi-section {
  background: white; border-radius: 16px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  display: flex; flex-direction: column; flex: 1;
}

.section-header { 
  padding: 20px 24px; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  border-bottom: 1px solid #f0f0f0; 
  flex-shrink: 0; 
}

.header-info h3 { margin: 0; font-size: 18px; font-weight: 700; color: #111; }
.header-info p  { margin: 4px 0 0; font-size: 12.5px; color: #666; }

.live-status { 
  display: flex; align-items: center; gap: 8px; 
  font-size: 11px; font-weight: 800; color: #2563eb; 
  background: #eff6ff; padding: 6px 12px; border-radius: 20px; 
}

.pulse-dot { 
  width: 8px; height: 8px; background: #2563eb; 
  border-radius: 50%; animation: pulse 2s infinite; 
}

@keyframes pulse { 
  0%,100% { transform: scale(0.95); opacity: 0.7; } 
  50% { transform: scale(1.2); opacity: 1; } 
}

/* 🔥 IFRAME FIX */
.iframe-container { 
  flex: 1; 
  width: 100%; 
  height: 100%;
}

iframe { 
  width: 100%;
  height: 100%;
  border: none;
}

.loading-container { 
  padding: 40px; display: flex; flex-direction: column; 
  align-items: center; justify-content: center; flex: 1; gap: 15px; 
}

.spinner { 
  width: 30px; height: 30px; 
  border: 3px solid #eee; 
  border-top: 3px solid #2563eb; 
  border-radius: 50%; 
  animation: spin 1s linear infinite; 
}

@keyframes spin { to { transform: rotate(360deg); } }

.no-access { padding: 40px; color: #666; text-align: center; font-weight: 500; }

@media (max-width: 768px) {
  .layout { flex-direction: column; height: auto; overflow: visible; }
  .sidebar { width: 100%; height: auto; position: static; flex-direction: row; flex-wrap: wrap; padding: 16px; gap: 8px; }
  .main { height: auto; }

  /* 🔥 FIX MOBILE */
  .analitica-wrapper { padding: 12px; }

  .scrollable-content { padding: 12px; }
}