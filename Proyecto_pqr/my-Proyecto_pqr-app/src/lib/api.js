const BASE_URL = 'http://localhost:8000' // Cambia esto por la URL de tu backend en producción

export const api = {
  // Usuarios
  getUsuarios: () => fetch(`${BASE_URL}/get_usuarios/`).then(r => r.json()),
  getUsuario: (id) => fetch(`${BASE_URL}/get_usuario/${id}`).then(r => r.json()),
  createUsuario: (data) => fetch(`${BASE_URL}/create_usuario`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(r => r.json()),
  updateUsuario: (id, data) => fetch(`${BASE_URL}/update_usuario/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(r => r.json()),
  deleteUsuario: (id) => fetch(`${BASE_URL}/delete_usuario/${id}`, {
    method: 'DELETE'
  }).then(r => r.json()),

  // Roles
  getRoles: () => fetch(`${BASE_URL}/get_roles/`).then(r => r.json()),

  // PQRs
  getPqrs: () => fetch(`${BASE_URL}/get_pqrs/`).then(r => r.json()),
  createPqr: (data) => fetch(`${BASE_URL}/create_pqr`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(r => r.json()),
}