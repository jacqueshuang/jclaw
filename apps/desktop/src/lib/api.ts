export async function createTask(payload: unknown) {
  const response = await fetch('http://127.0.0.1:8000/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  return response.json()
}
