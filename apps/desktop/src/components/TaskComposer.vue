<template>
  <form @submit.prevent="submit">
    <label>
      任务标题
      <input v-model="title" aria-label="任务标题" />
    </label>

    <label>
      任务目标
      <textarea v-model="userPrompt" aria-label="任务目标" />
    </label>

    <SourcePicker @add-text-source="addTextSource" />

    <button type="submit">提交任务</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import SourcePicker from './SourcePicker.vue'

const emit = defineEmits<{
  submit: [payload: { title: string; user_prompt: string; sources: Array<{ source_type: 'text'; title: string; content: string }> }]
}>()

const title = ref('')
const userPrompt = ref('')
const sources = ref<Array<{ source_type: 'text'; title: string; content: string }>>([])

function addTextSource(source: { source_type: 'text'; title: string; content: string }) {
  sources.value = [...sources.value, source]
}

function submit() {
  emit('submit', {
    title: title.value,
    user_prompt: userPrompt.value,
    sources: sources.value,
  })
}
</script>
