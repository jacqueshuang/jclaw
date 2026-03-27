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

const latestPayload = ref<TaskPayload | null>(null)

export function useTaskStore() {
  async function submitTask(payload: TaskPayload) {
    latestPayload.value = payload
    return createTask(payload)
  }

  return {
    latestPayload,
    submitTask,
  }
}
