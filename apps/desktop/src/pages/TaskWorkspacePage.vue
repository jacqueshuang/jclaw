<template>
  <main class="task-workspace">
    <TaskComposer @submit="submitTask" />
    <p v-if="submitError" role="status">{{ submitError }}</p>

    <TaskTimeline v-if="taskStatus" :status="taskStatus" />
    <KnowledgePackPanel
      v-if="knowledgePack"
      :summary="knowledgePack.summary"
      :outline="knowledgePack.outline"
    />
    <DeliverablePanel
      v-if="deliverable"
      :content-markdown="deliverable.content_markdown"
    />
  </main>
</template>

<script setup lang="ts">
import { computed, getCurrentInstance, onMounted, ref } from 'vue'

import DeliverablePanel from '../components/DeliverablePanel.vue'
import KnowledgePackPanel from '../components/KnowledgePackPanel.vue'
import TaskComposer from '../components/TaskComposer.vue'
import TaskTimeline from '../components/TaskTimeline.vue'
import { useTaskStore } from '../stores/task'

const taskStore = useTaskStore()
const submitError = ref<string | null>(null)
const taskDetail = ref<{
  status: string
  knowledge_pack: { summary: string; outline: string } | null
  deliverable: { content_markdown: string; content_type: string } | null
} | null>(null)
const instance = getCurrentInstance()

const taskStatus = computed(() => taskDetail.value?.status ?? null)
const knowledgePack = computed(() => taskDetail.value?.knowledge_pack ?? null)
const deliverable = computed(() => taskDetail.value?.deliverable ?? null)

onMounted(async () => {
  const apiClient = instance?.proxy?.$api as { getTask?: (taskId: string) => Promise<typeof taskDetail.value> } | undefined
  if (!apiClient?.getTask) {
    return
  }

  taskDetail.value = await apiClient.getTask('latest')
})

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
