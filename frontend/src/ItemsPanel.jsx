import { useCallback, useEffect, useState } from 'react'
import { api } from './api'
import { Badge, Button, Card, EmptyState, ErrorBanner, Field } from './ui'

// EXAMPLE FEATURE — the frontend half of backend/items.py: list, create (with
// AI-suggested tags that fall back gracefully), delete. Copy this shape for the
// walking skeleton, then delete or rename it once the real feature exists.
export default function ItemsPanel() {
  const [items, setItems] = useState(undefined) // undefined = loading
  const [error, setError] = useState(null)
  const [title, setTitle] = useState('')
  const [notes, setNotes] = useState('')
  const [busy, setBusy] = useState(false)
  const [aiOffline, setAiOffline] = useState(false)

  const load = useCallback(
    () =>
      api('/api/items')
        .then((list) => {
          setError(null)
          setItems(list)
        })
        .catch((err) => {
          setError(err)
          setItems([])
        }),
    [],
  )

  useEffect(() => {
    load()
  }, [load])

  async function onSubmit(e) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const created = await api('/api/items', { method: 'POST', body: { title, notes } })
      setAiOffline(created.fallback)
      setItems((list) => [created, ...(list || [])])
      setTitle('')
      setNotes('')
    } catch (err) {
      setError(err)
    } finally {
      setBusy(false)
    }
  }

  async function remove(id) {
    setError(null)
    try {
      await api(`/api/items/${id}`, { method: 'DELETE' })
      setItems((list) => list.filter((it) => it.id !== id))
    } catch (err) {
      setError(err)
    }
  }

  return (
    <>
      <Card title="Add an item">
        <form onSubmit={onSubmit} className="stack">
          <Field label="Title" value={title} onChange={(e) => setTitle(e.target.value)} required maxLength={120} />
          <Field
            label="Notes"
            as="textarea"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            maxLength={2000}
            hint="Tags are suggested by AI when a key is configured; otherwise the item is saved without them."
          />
          <div className="row">
            <Button type="submit" busy={busy}>
              {busy ? 'Saving…' : 'Add'}
            </Button>
            {aiOffline && <Badge tone="warn">AI offline — tags skipped</Badge>}
          </div>
        </form>
      </Card>

      <Card title="Your items">
        <ErrorBanner error={error} onRetry={load} />
        {items === undefined ? (
          <p className="muted" role="status">
            Loading…
          </p>
        ) : items.length === 0 ? (
          <EmptyState title="Nothing here yet">Add your first item above.</EmptyState>
        ) : (
          <ul className="list">
            {items.map((it) => (
              <li key={it.id}>
                <div>
                  <strong>{it.title}</strong>
                  {it.notes && <p className="muted" style={{ margin: 0 }}>{it.notes}</p>}
                  {it.tags.length > 0 && (
                    <div className="row" style={{ marginTop: '0.25rem' }}>
                      {it.tags.map((t) => (
                        <Badge key={t}>{t}</Badge>
                      ))}
                    </div>
                  )}
                </div>
                <Button variant="danger" onClick={() => remove(it.id)} aria-label={`Delete ${it.title}`}>
                  Delete
                </Button>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </>
  )
}
