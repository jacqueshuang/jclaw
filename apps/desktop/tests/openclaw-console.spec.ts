import { beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'

import App from '../src/App.vue'
import InstallStatusCard from '../src/components/InstallStatusCard.vue'

const openclawApi = vi.hoisted(() => ({
  getOpenClawStatus: vi.fn(),
  startOnlineInstall: vi.fn(),
  startOfflineInstall: vi.fn(),
}))

vi.mock('../src/lib/openclaw', () => ({
  getOpenClawStatus: openclawApi.getOpenClawStatus,
  startOnlineInstall: openclawApi.startOnlineInstall,
  startOfflineInstall: openclawApi.startOfflineInstall,
}))

const notInstalledStatus = {
  kind: 'not_installed' as const,
  statusLabel: '未安装',
  installPath: null,
  message: '检测到本机固定安装位置不存在 OpenClaw。',
}

const installedStatus = {
  kind: 'installed' as const,
  statusLabel: '已安装',
  installPath: '/Applications/OpenClaw/openclaw',
  message: '已检测到本机 OpenClaw 安装文件。',
}

describe('OpenClaw console shell', () => {
  beforeEach(() => {
    openclawApi.getOpenClawStatus.mockResolvedValue(notInstalledStatus)
    openclawApi.startOnlineInstall.mockReset()
    openclawApi.startOfflineInstall.mockReset()
  })

  it('renders console navigation and install heading', async () => {
    const wrapper = mount(App)
    await flushPromises()

    expect(wrapper.get('h1').text()).toBe('OpenClaw 安装中心')

    const navItems = wrapper.findAll('[data-testid="sidebar-nav-item"]')
    expect(navItems.map((item) => item.text())).toEqual(['安装', 'Skills', 'Channel', 'Agent'])
    expect(navItems[0]?.classes()).toContain('console-nav-item--active')

    expect(wrapper.get('[data-testid="console-status-badge"]').text()).toBe('未安装')
    expect(wrapper.findAll('[data-testid="module-summary-card"]')).toHaveLength(3)
  })

  it('renders skeleton module pages for skills, channel, and agent', async () => {
    const wrapper = mount(App)
    await flushPromises()

    expect(wrapper.get('[data-testid="module-stack"]').findAll('.module-shell')).toHaveLength(3)
    expect(wrapper.get('[data-testid="skills-page"]').text()).toContain('Skills')
    expect(wrapper.get('[data-testid="channels-page"]').text()).toContain('Channel')
    expect(wrapper.get('[data-testid="agents-page"]').text()).toContain('Agent')
  })

  it('renders install action for not-installed state', async () => {
    const wrapper = mount(App)
    await flushPromises()

    expect(wrapper.text()).toContain('OpenClaw 尚未安装')
    expect(wrapper.text()).toContain('安装')
    expect(wrapper.text()).toContain('选择离线包')
  })

  it('runs online install and transitions status to installed', async () => {
    let resolveInstall: (value: typeof installedStatus) => void = () => {}
    const installPromise = new Promise<typeof installedStatus>((resolve) => {
      resolveInstall = resolve
    })
    openclawApi.startOnlineInstall.mockReturnValueOnce(installPromise)

    const wrapper = mount(App)
    await flushPromises()

    await wrapper.get('.install-card__primary').trigger('click')

    expect(openclawApi.startOnlineInstall).toHaveBeenCalledTimes(1)
    expect(wrapper.get('[data-testid="console-status-badge"]').text()).toBe('安装中')

    resolveInstall(installedStatus)
    await flushPromises()

    expect(wrapper.get('[data-testid="console-status-badge"]').text()).toBe('已安装')
    expect(wrapper.get('[data-testid="install-status-title"]').text()).toBe('OpenClaw 已安装')
  })

  it('transitions status to install failed when online install rejects', async () => {
    openclawApi.startOnlineInstall.mockRejectedValueOnce(new Error('install failed'))

    const wrapper = mount(App)
    await flushPromises()

    await wrapper.get('.install-card__primary').trigger('click')
    await flushPromises()

    expect(openclawApi.startOnlineInstall).toHaveBeenCalledTimes(1)
    expect(wrapper.get('[data-testid="console-status-badge"]').text()).toBe('安装失败')
    expect(wrapper.get('[data-testid="install-status-title"]').text()).toBe('OpenClaw 安装失败')
  })

  it('runs offline install and transitions status correctly', async () => {
    let resolveInstall: (value: typeof installedStatus) => void = () => {}
    const installPromise = new Promise<typeof installedStatus>((resolve) => {
      resolveInstall = resolve
    })
    openclawApi.startOfflineInstall.mockImplementationOnce(() => installPromise)

    const wrapper = mount(App)
    await flushPromises()

    await wrapper.get('.install-card__secondary').trigger('click')

    expect(openclawApi.startOfflineInstall).toHaveBeenCalledTimes(1)
    expect(wrapper.get('[data-testid="console-status-badge"]').text()).toBe('安装中')

    resolveInstall(installedStatus)
    await flushPromises()

    expect(wrapper.get('[data-testid="console-status-badge"]').text()).toBe('已安装')
  })
})

describe('InstallStatusCard', () => {
  it('renders checking state', () => {
    const wrapper = mount(InstallStatusCard, {
      props: {
        status: {
          kind: 'checking',
          statusLabel: '检测中',
          installPath: null,
          message: '正在检测本机 OpenClaw 安装状态。',
        },
      },
    })

    expect(wrapper.get('[data-testid="install-status-badge"]').text()).toBe('检测中')
  })

  it('renders installed state with install path', () => {
    const wrapper = mount(InstallStatusCard, {
      props: {
        status: {
          kind: 'installed',
          statusLabel: '已安装',
          installPath: '/Applications/OpenClaw/openclaw',
          message: '已检测到本机 OpenClaw 安装文件。',
        },
      },
    })

    expect(wrapper.get('[data-testid="install-status-title"]').text()).toBe('OpenClaw 已安装')
    expect(wrapper.get('[data-testid="install-status-badge"]').text()).toBe('已安装')
    expect(wrapper.get('[data-testid="install-status-version"]').text()).toContain('/Applications/OpenClaw/openclaw')
  })

  it('renders not installed state with action buttons', () => {
    const wrapper = mount(InstallStatusCard, {
      props: {
        status: {
          kind: 'not_installed',
          statusLabel: '未安装',
          installPath: null,
          message: '检测到本机固定安装位置不存在 OpenClaw。',
        },
      },
    })

    expect(wrapper.get('[data-testid="install-status-title"]').text()).toBe('OpenClaw 尚未安装')
    expect(wrapper.get('[data-testid="install-status-badge"]').text()).toBe('未安装')
    expect(wrapper.findAll('button')).toHaveLength(2)
    expect(wrapper.text()).toContain('选择离线包')
  })

  it('renders install failed state message', () => {
    const wrapper = mount(InstallStatusCard, {
      props: {
        status: {
          kind: 'install_failed',
          statusLabel: '安装失败',
          installPath: null,
          message: '检测失败',
        },
      },
    })

    expect(wrapper.get('[data-testid="install-status-title"]').text()).toBe('OpenClaw 安装失败')
    expect(wrapper.get('[data-testid="install-status-badge"]').text()).toBe('安装失败')
    expect(wrapper.get('[data-testid="install-status-message"]').text()).toContain('检测失败')
  })
})
