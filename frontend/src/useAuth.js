import { useCallback, useEffect, useState } from 'react'
import { api, clearToken, getToken, login as apiLogin, signup as apiSignup } from './api'

// Current user + auth actions. `user` is null when logged out, undefined while checking.
export default function useAuth() {
  const [user, setUser] = useState(getToken() ? undefined : null)

  const refresh = useCallback(async () => {
    if (!getToken()) return setUser(null)
    try {
      setUser(await api('/api/auth/me'))
    } catch {
      setUser(null)
    }
  }, [])

  useEffect(() => {
    refresh()
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
