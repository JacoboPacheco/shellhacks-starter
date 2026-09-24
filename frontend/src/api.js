// Every backend call goes through here so auth headers and the prod API URL
// are handled in one place. In dev VITE_API_URL is empty and Vite proxies
// /api and /uploads to the backend; in prod it's the Render URL.
const BASE = import.meta.env.VITE_API_URL || ''
const TOKEN_KEY = 'token'

export const getToken = () => localStorage.getItem(TOKEN_KEY)
export const setToken = (token) => localStorage.setItem(TOKEN_KEY, token)
export const clearToken = () => localStorage.removeItem(TOKEN_KEY)

// Turns a backend-relative path like "/uploads/abc.png" into a usable src/href.
export const assetUrl = (path) => `${BASE}${path}`

export async function api(path, { method = 'GET', body, form } = {}) {
  const headers = {}
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  let payload
  if (form) {
    payload = form
  } else if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }

  const res = await fetch(`${BASE}${path}`, { method, headers, body: payload })
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    if (res.status === 401) clearToken()
    throw new Error(data?.detail || `Request failed (${res.status})`)
  }
  return data
}

export async function login(email, password) {
  const form = new URLSearchParams({ username: email, password })
  const res = await fetch(`${BASE}/api/auth/login`, { method: 'POST', body: form })
  const data = await res.json().catch(() => null)
  if (!res.ok) throw new Error(data?.detail || 'Login failed')
  setToken(data.access_token)
  return data
}

export async function signup(email, password) {
  const data = await api('/api/auth/signup', { method: 'POST', body: { email, password } })
  setToken(data.access_token)
  return data
}

export async function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  return api('/api/upload', { method: 'POST', form })
}
