import { invoke } from '@tauri-apps/api/core'

import type { ConsoleSummary, OpenClawInstallStatus } from '../types/openclaw'

export function getOpenClawStatus() {
  return invoke<OpenClawInstallStatus>('get_openclaw_status')
}

export function getConsoleSummary() {
  return invoke<ConsoleSummary>('get_console_summary')
}

export function startOnlineInstall() {
  return invoke<OpenClawInstallStatus>('start_online_install')
}

export function startOfflineInstall() {
  return invoke<OpenClawInstallStatus>('start_offline_install')
}
