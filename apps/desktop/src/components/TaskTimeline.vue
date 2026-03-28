<template>
  <aside>
    <h2>任务状态</h2>
    <p>{{ status }}</p>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  status: string
}>()
</script>
