import { useEffect, useState } from 'react'
import { api } from './api'

function App() {
  const [status, setStatus] = useState('checking...')

  useEffect(() => {
    api('/api/health')
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('backend unreachable'))
  }, [])

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Shellhacks Starter</h1>
      <p>Backend status: {status}</p>
    </main>
  )
}

export default App
