<template>
  <section>
    <h2>最终成品</h2>
    <pre>{{ contentMarkdown }}</pre>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  contentMarkdown: string
}>()
</script>
