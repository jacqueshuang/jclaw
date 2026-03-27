<template>
  <main class="task-workspace">
    <TaskComposer @submit="submitTask" />
    <p v-if="submitError" role="status">{{ submitError }}</p>
    <p v-if="detailLoading" role="status">任务详情加载中...</p>
    <p v-else-if="detailError" role="alert">{{ detailError }}</p>

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
import { computed, onMounted, ref } from 'vue'

import DeliverablePanel from '../components/DeliverablePanel.vue'
import KnowledgePackPanel from '../components/KnowledgePackPanel.vue'
import TaskComposer from '../components/TaskComposer.vue'
import TaskTimeline from '../components/TaskTimeline.vue'
import { getTask } from '../lib/api'
import { useTaskStore } from '../stores/task'

const taskStore = useTaskStore()
const submitError = ref<string | null>(null)
const detailLoading = ref(false)
const detailError = ref<string | null>(null)
const taskDetail = ref<{
  status: string
  knowledge_pack: { summary: string; outline: string } | null
  deliverable: { content_markdown: string; content_type: string } | null
} | null>(null)

const taskStatus = computed(() => taskDetail.value?.status ?? null)
const knowledgePack = computed(() => taskDetail.value?.knowledge_pack ?? null)
const deliverable = computed(() => taskDetail.value?.deliverable ?? null)

onMounted(async () => {
  detailLoading.value = true
  detailError.value = null

  try {
    taskDetail.value = await getTask('latest')
  }
  catch {
    detailError.value = '任务详情加载失败，请稍后重试。'
  }
  finally {
    detailLoading.value = false
  }
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
