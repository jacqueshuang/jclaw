const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000'
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL).replace(/\/$/, '')

export async function createTask(payload: unknown) {
  const response = await fetch(`${API_BASE_URL}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Create task request failed: ${response.status} ${response.statusText}`)
  }

  return response.json()
}

export async function getTask(taskId: string) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`)

  if (!response.ok) {
    throw new Error(`Get task request failed: ${response.status} ${response.statusText}`)
  }

  return response.json()
}
