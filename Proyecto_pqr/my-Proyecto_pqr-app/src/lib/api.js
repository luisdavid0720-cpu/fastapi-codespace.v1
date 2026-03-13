const BASE_URL = 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`)
  return res.json()
}

// ---- USUARIOS ----
export const api = {
  // Usuarios
  getUsuarios: () => request('/get_usuarios/'),
  getUsuario: (id) => request(`/get_usuario/${id}`),
  createUsuario: (data) => request('/create_usuario', { method: 'POST', body: JSON.stringify(data) }),
  updateUsuario: (id, data) => request(`/update_usuario/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteUsuario: (id) => request(`/delete_usuario/${id}`, { method: 'DELETE' }),

  // PQRs
  getPqrs: () => request('/get_pqrs/'),
  getPqr: (id) => request(`/get_pqr/${id}`),
  createPqr: (data) => request('/create_pqr', { method: 'POST', body: JSON.stringify(data) }),
  updatePqr: (id, data) => request(`/update_pqr/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deletePqr: (id) => request(`/delete_pqr/${id}`, { method: 'DELETE' }),

  // Roles
  getRoles: () => request('/get_rols/'),

  // Estados
  getEstados: () => request('/get_estados/'),

  // Tipos PQR
  getTiposPqr: () => request('/get_tipo_pqrs/'),

  // Departamentos
  getDepartamentos: () => request('/get_departamentos/'),

  // Prioridades
  getPrioridades: () => request('/get_prioridades/'),

  // Respuestas
  getRespuestas: () => request('/get_respuestas/'),
  createRespuesta: (data) => request('/create_respuesta', { method: 'POST', body: JSON.stringify(data) }),
}
