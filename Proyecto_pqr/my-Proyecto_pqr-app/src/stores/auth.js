import { writable } from 'svelte/store'

const isBrowser = typeof window !== 'undefined'

const stored = isBrowser ? localStorage.getItem('pqr_user') : null

export const currentUser = writable(stored ? JSON.parse(stored) : null)

currentUser.subscribe(val => {
  if (isBrowser) {
    if (val) {
      localStorage.setItem('pqr_user', JSON.stringify(val))
    } else {
      localStorage.removeItem('pqr_user')
    }
  }
})

export function login(rol) {
  if (rol === 'admin') {
    currentUser.set({
      id_usuario: 1,
      nombre: 'Administrador',
      correo: 'admin@cul.edu.co',
      id_rol: 3
    })
  }

  else if (rol === 'Director de Programa') {
    currentUser.set({
      id_usuario: 2,
      nombre: 'Director de Programa',
      correo: 'coord@cul.edu.co',
      id_rol: 4
    })
  }

  else {
    currentUser.set({
      id_usuario: 3,
      nombre: 'Estudiante',
      correo: 'user@cul.edu.co',
      id_rol: 1
    })
  }
}

export function logout() {
  currentUser.set(null)
}