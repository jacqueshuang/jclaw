import { describe, expect, it, vi } from 'vitest'

const invoke = vi.fn()
vi.mock('@tauri-apps/api/core', () => ({ invoke }))

describe('openclaw desktop api', () => {
  it('calls the install-status command', async () => {
    invoke.mockResolvedValueOnce({
      kind: 'not_installed',
      statusLabel: '未安装',
      installPath: null,
      message: '检测到本机固定安装位置不存在 OpenClaw。',
    })

    const { getOpenClawStatus } = await import('../src/lib/openclaw')
    const result = await getOpenClawStatus()

    expect(invoke).toHaveBeenCalledWith('get_openclaw_status')
    expect(result.kind).toBe('not_installed')
  })

  it('calls the online-install command', async () => {
    invoke.mockResolvedValueOnce({
      kind: 'installing',
      statusLabel: '安装中',
      installPath: null,
      message: '正在准备在线安装 OpenClaw。',
    })

    const { startOnlineInstall } = await import('../src/lib/openclaw')
    const result = await startOnlineInstall()

    expect(invoke).toHaveBeenCalledWith('start_online_install')
    expect(result.kind).toBe('installing')
  })

  it('calls the offline-install command', async () => {
    invoke.mockResolvedValueOnce({
      kind: 'installing',
      statusLabel: '安装中',
      installPath: null,
      message: '正在准备离线安装 OpenClaw。',
    })

    const { startOfflineInstall } = await import('../src/lib/openclaw')
    const result = await startOfflineInstall()

    expect(invoke).toHaveBeenCalledWith('start_offline_install')
    expect(result.kind).toBe('installing')
  })
})
