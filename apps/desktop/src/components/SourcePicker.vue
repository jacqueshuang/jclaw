<template>
  <section>
    <label>
      文本资料标题
      <input v-model="title" aria-label="文本资料标题" />
    </label>

    <label>
      文本资料内容
      <textarea v-model="content" aria-label="文本资料内容" />
    </label>

    <button type="button" @click="addTextSource">添加文本资料</button>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  'add-text-source': [source: { source_type: 'text'; title: string; content: string }]
}>()

const title = ref('')
const content = ref('')

function addTextSource() {
  emit('add-text-source', {
    source_type: 'text',
    title: title.value,
    content: content.value,
  })
}
</script>
