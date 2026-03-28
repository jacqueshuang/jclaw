import { ref } from 'vue'

import { createTask } from '../lib/api'

type TextSource = {
  source_type: 'text'
  title: string
  content: string
}

type TaskPayload = {
  title: string
  user_prompt: string
  sources: TextSource[]
}

type TaskSubmission = {
  id: string
}

const latestPayload = ref<TaskPayload | null>(null)
const latestTaskId = ref<string | null>(null)

export function useTaskStore() {
  async function submitTask(payload: TaskPayload) {
    latestPayload.value = payload
    const response = await createTask(payload) as TaskSubmission
    latestTaskId.value = response.id
    return response
  }

  return {
    latestPayload,
    latestTaskId,
    submitTask,
  }
}
