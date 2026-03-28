<template>
  <div class="console-shell">
    <SidebarNav />
    <main class="console-main">
      <header class="console-header">
        <div>
          <p class="console-eyebrow">OpenClaw Console</p>
          <h1>OpenClaw 安装中心</h1>
          <p class="console-subtitle">检测本机 OpenClaw 状态，并进入 Skills / Channel / Agent 的统一控制台。</p>
        </div>
        <span class="console-status-badge" data-testid="console-status-badge">{{ installStatus.statusLabel }}</span>
      </header>
      <InstallStatusCard :status="installStatus" @online-install="handleOnlineInstall" @offline-install="handleOfflineInstall" />
      <ModuleSummaryGrid />
      <div class="module-stack" data-testid="module-stack">
        <SkillsPage />
        <ChannelsPage />
        <AgentsPage />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import InstallStatusCard from '../components/InstallStatusCard.vue'
import ModuleSummaryGrid from '../components/ModuleSummaryGrid.vue'
import SidebarNav from '../components/SidebarNav.vue'
import { getOpenClawStatus, startOfflineInstall, startOnlineInstall } from '../lib/openclaw'
import AgentsPage from './AgentsPage.vue'
import ChannelsPage from './ChannelsPage.vue'
import SkillsPage from './SkillsPage.vue'
import type { OpenClawInstallStatus } from '../types/openclaw'

const installStatus = ref<OpenClawInstallStatus>({
  kind: 'checking',
  statusLabel: '检测中',
  installPath: null,
  message: '正在检测本机 OpenClaw 安装状态。',
})

async function refreshInstallStatus() {
  try {
    installStatus.value = await getOpenClawStatus()
  } catch {
    installStatus.value = {
      kind: 'install_failed',
      statusLabel: '安装失败',
      installPath: null,
      message: '检测 OpenClaw 安装状态失败。',
    }
  }
}

async function handleOnlineInstall() {
  installStatus.value = {
    kind: 'installing',
    statusLabel: '安装中',
    installPath: null,
    message: '正在执行在线安装，请稍候。',
  }

  try {
    installStatus.value = await startOnlineInstall()
  } catch {
    installStatus.value = {
      kind: 'install_failed',
      statusLabel: '安装失败',
      installPath: null,
      message: '在线安装失败，请稍后重试。',
    }
  }
}

async function handleOfflineInstall() {
  installStatus.value = {
    kind: 'installing',
    statusLabel: '安装中',
    installPath: null,
    message: '正在执行离线安装，请稍候。',
  }

  try {
    installStatus.value = await startOfflineInstall()
  } catch {
    installStatus.value = {
      kind: 'install_failed',
      statusLabel: '安装失败',
      installPath: null,
      message: '离线安装失败，请稍后重试。',
    }
  }
}

onMounted(() => {
  void refreshInstallStatus()
})
</script>
