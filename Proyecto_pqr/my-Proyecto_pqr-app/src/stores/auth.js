import { writable } from 'svelte/store'

// 1. Verificamos si estamos en el navegador para evitar errores
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

export function logout() {
  currentUser.set(null)
}