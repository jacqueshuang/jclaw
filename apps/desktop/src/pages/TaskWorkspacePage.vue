<template>
  <main class="task-workspace">
    <TaskComposer @submit="submitTask" />
  </main>
</template>

<script setup lang="ts">
import TaskComposer from '../components/TaskComposer.vue'
import { useTaskStore } from '../stores/task'

const taskStore = useTaskStore()

function submitTask(payload: { title: string; user_prompt: string; sources: Array<{ source_type: 'text'; title: string; content: string }> }) {
  taskStore.submitTask(payload)
}
</script>
