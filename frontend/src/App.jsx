import { useEffect, useState } from 'react'
import { api } from './api'
import useAuth from './useAuth'

function App() {
  // Keep this call: with VITE_DEMO_EMAIL/VITE_DEMO_PASSWORD set (frontend/.env) it signs
  // in as the seeded demo account on load, so per-user features need no login screen.
  const { user } = useAuth()
  const [status, setStatus] = useState('checking...')

  useEffect(() => {
    api('/api/health')
      .then((data) => setStatus(data.status))
      .catch((err) => setStatus(`backend unreachable — ${err.message}`))
  }, [])

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Shellhacks Starter</h1>
      <p>Backend status: {status}</p>
      {user && <p>Signed in as {user.email}</p>}
    </main>
  )
}

export default App
