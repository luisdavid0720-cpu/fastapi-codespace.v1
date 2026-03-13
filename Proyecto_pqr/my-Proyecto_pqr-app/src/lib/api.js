const API = "http://localhost:8000"

export async function getUsuarios() {
  const res = await fetch(`${API}/usuarios`)
  return res.json()
}

export async function getPqr() {
  const res = await fetch(`${API}/pqr`)
  return res.json()
}