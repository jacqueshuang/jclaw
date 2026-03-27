<template>
  <main class="task-workspace">
    <TaskComposer @submit="submitTask" />
    <p v-if="submitError" role="status">{{ submitError }}</p>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import TaskComposer from '../components/TaskComposer.vue'
import { useTaskStore } from '../stores/task'

const taskStore = useTaskStore()
const submitError = ref<string | null>(null)

async function submitTask(payload: { title: string; user_prompt: string; sources: Array<{ source_type: 'text'; title: string; content: string }> }) {
  submitError.value = null
  try {
    await taskStore.submitTask(payload)
  }
  catch {
    submitError.value = '任务提交失败，请稍后重试。'
  }
}
</script>
