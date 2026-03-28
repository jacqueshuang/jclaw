<template>
  <section>
    <h2>知识包</h2>
    <p>{{ summary }}</p>
    <pre>{{ outline }}</pre>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  summary: string
  outline: string
}>()
</script>
