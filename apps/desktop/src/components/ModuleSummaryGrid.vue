<template>
  <section class="summary-grid" aria-label="Module summary">
    <article
      v-for="card in cards"
      :key="card.label"
      class="summary-card"
      data-testid="module-summary-card"
    >
      <p class="summary-card__label">{{ card.label }}</p>
      <h2>{{ card.value }}</h2>
      <p>{{ card.description }}</p>
    </article>
  </section>
</template>

<script setup lang="ts">
const cards = [
  {
    label: 'Skills',
    value: '未配置',
    description: '安装完成后可加载技能市场与本地技能包。',
  },
  {
    label: 'Channel',
    value: '未接入',
    description: '后续可管理聊天渠道接入状态。',
  },
  {
    label: 'Agent',
    value: '0 个实例',
    description: '未来可统一管理 Agent 模板与运行状态。',
  },
]
</script>
