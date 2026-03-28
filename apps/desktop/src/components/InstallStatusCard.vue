<template>
  <section class="install-card">
    <div class="install-card__header">
      <div>
        <p class="install-card__label">Primary Action</p>
        <h2 data-testid="install-status-title">{{ title }}</h2>
        <p data-testid="install-status-message">{{ status.message }}</p>
      </div>
      <span class="install-card__badge" :class="badgeClass" data-testid="install-status-badge">{{ status.statusLabel }}</span>
    </div>

    <div class="install-card__actions" v-if="status.kind === 'not_installed'">
      <button class="install-card__primary" type="button" @click="emit('online-install')">安装</button>
      <button class="install-card__secondary" type="button" @click="emit('offline-install')">选择离线包</button>
    </div>

    <div class="install-card__actions" v-else-if="status.kind === 'installed'">
      <button class="install-card__primary" type="button" disabled>已安装</button>
    </div>

    <div class="install-card__actions" v-else>
      <button class="install-card__secondary" type="button" disabled>{{ status.statusLabel }}</button>
    </div>

    <p v-if="status.installPath" class="install-card__path" data-testid="install-status-version">安装路径：{{ status.installPath }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { OpenClawInstallStatus } from '../types/openclaw'

const props = defineProps<{
  status: OpenClawInstallStatus
}>()

const emit = defineEmits<{
  'online-install': []
  'offline-install': []
}>()

const status = computed(() => props.status)

const title = computed(() => {
  if (status.value.kind === 'installed') return 'OpenClaw 已安装'
  if (status.value.kind === 'install_failed') return 'OpenClaw 安装失败'
  if (status.value.kind === 'installing') return 'OpenClaw 安装中'
  return 'OpenClaw 尚未安装'
})

const badgeClass = computed(() => `install-card__badge--${status.value.kind}`)
</script>
