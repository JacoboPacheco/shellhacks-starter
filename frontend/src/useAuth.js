import { useCallback, useEffect, useState } from 'react'
import { api, clearToken, getToken, login as apiLogin, signup as apiSignup } from './api'

// Current user + auth actions. `user` is null when logged out, undefined while checking.
export default function useAuth() {
  const [user, setUser] = useState(getToken() ? undefined : null)

  // Always resolves; never updates state synchronously (keeps the effect below lint-clean).
  const refresh = useCallback(
    () =>
      (getToken() ? api('/api/auth/me') : Promise.resolve(null))
        .then((u) => setUser(u))
        .catch(() => setUser(null)),
    []
  )

  useEffect(() => {
    refresh()
    const expired = () => setUser(null)
    window.addEventListener('auth:expired', expired)
    return () => window.removeEventListener('auth:expired', expired)
  }, [refresh])

  const login = async (email, password) => {
    await apiLogin(email, password)
    await refresh()
  }

  const signup = async (email, password) => {
    await apiSignup(email, password)
    await refresh()
  }

  const logout = () => {
    clearToken()
    setUser(null)
  }

  return { user, loading: user === undefined, login, signup, logout }
}
