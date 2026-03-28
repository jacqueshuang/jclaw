<template>
  <aside class="console-sidebar">
    <div class="console-brand">OpenClaw</div>
    <nav class="console-nav" aria-label="Primary">
      <div
        v-for="item in items"
        :key="item.label"
        class="console-nav-item"
        :class="{ 'console-nav-item--active': item.active }"
        :aria-current="item.active ? 'page' : undefined"
        data-testid="sidebar-nav-item"
      >
        {{ item.label }}
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
const items = [
  { label: '安装', active: true },
  { label: 'Skills', active: false },
  { label: 'Channel', active: false },
  { label: 'Agent', active: false },
]
</script>
