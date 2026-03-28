# OpenClaw Console Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current task-workspace desktop app with an OpenClaw Console that detects local installation state, supports online/offline install flows, and presents Skills / Channel / Agent management shells.

**Architecture:** Keep the desktop product as a Tauri + Vue app, but pivot the frontend from a task form into a shell-style console with one dominant installation dashboard and three management modules. Put all filesystem and installation behavior behind new Tauri commands in Rust, then expose a minimal typed frontend API layer for install status, online install, offline install, and shell module summaries.

**Tech Stack:** Vue 3, Vite, Vitest, Tauri 2, Rust

---

## File Structure

### Frontend files to modify
- `apps/desktop/src/App.vue` — replace the task workspace root with the OpenClaw console root.
- `apps/desktop/src/main.ts` — keep bootstrap simple; only adjust if the new app root needs additional setup.
- `apps/desktop/src/styles.css` — replace task-form styling with the approved console visual system.
- `apps/desktop/src/lib/api.ts` — stop calling the current backend task API and replace with a Tauri invoke-based desktop API wrapper.

### Frontend files to create
- `apps/desktop/src/lib/openclaw.ts` — typed frontend wrappers around Tauri commands.
- `apps/desktop/src/pages/OpenClawConsolePage.vue` — top-level console page with sidebar, install card, and module summary cards.
- `apps/desktop/src/components/InstallStatusCard.vue` — primary installation status card and action area.
- `apps/desktop/src/components/InstallSourceCard.vue` — online/offline install mode summary card.
- `apps/desktop/src/components/ModuleSummaryGrid.vue` — summary cards for Skills / Channel / Agent.
- `apps/desktop/src/components/SidebarNav.vue` — left navigation shell.
- `apps/desktop/src/types/openclaw.ts` — shared frontend types for install status and module summaries.
- `apps/desktop/tests/openclaw-console.spec.ts` — component tests for the new console page.
- `apps/desktop/tests/openclaw-api.spec.ts` — frontend API wrapper tests.

### Rust files to modify
- `apps/desktop/src-tauri/src/lib.rs` — stop auto-spawning the old Python backend, register Tauri commands for OpenClaw detection and install flows, and initialize app state.
- `apps/desktop/src-tauri/Cargo.toml` — add Rust dependencies needed for state serialization, file copy/unzip, and command handling.

### Rust files to create
- `apps/desktop/src-tauri/src/openclaw.rs` — install state model, install detection, online install, offline install, and command implementations.
- `apps/desktop/src-tauri/src/state.rs` — persisted app state and summary metadata for Skills / Channel / Agent.
- `apps/desktop/src-tauri/tests/openclaw_commands.rs` — Rust tests for install detection and command behavior.

### Docs to modify
- `README.md` — replace task-workspace language with OpenClaw Console purpose, run flow, and test commands.

---

### Task 1: Replace the current app root with the OpenClaw console shell

**Files:**
- Modify: `apps/desktop/src/App.vue:1-10`
- Modify: `apps/desktop/src/styles.css:1-34`
- Create: `apps/desktop/src/pages/OpenClawConsolePage.vue`
- Create: `apps/desktop/src/components/SidebarNav.vue`
- Create: `apps/desktop/src/components/ModuleSummaryGrid.vue`
- Test: `apps/desktop/tests/openclaw-console.spec.ts`

- [ ] **Step 1: Write the failing console shell test**

```ts
import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import OpenClawConsolePage from '../src/pages/OpenClawConsolePage.vue'

vi.mock('../src/lib/openclaw', () => ({
  getOpenClawStatus: vi.fn().mockResolvedValue({
    kind: 'not_installed',
    statusLabel: '未安装',
    installPath: null,
  }),
  getConsoleSummary: vi.fn().mockResolvedValue({
    skills: { title: 'Skills', value: '未配置', description: '安装完成后可加载技能市场与本地技能包。' },
    channels: { title: 'Channel', value: '未接入', description: '后续可管理聊天渠道接入状态。' },
    agents: { title: 'Agent', value: '0 个实例', description: '未来可统一管理 Agent 模板与运行状态。' },
  }),
}))

describe('OpenClawConsolePage', () => {
  it('renders console navigation and install heading', async () => {
    const wrapper = mount(OpenClawConsolePage)
    await Promise.resolve()

    expect(wrapper.text()).toContain('OpenClaw 安装中心')
    expect(wrapper.text()).toContain('安装')
    expect(wrapper.text()).toContain('Skills')
    expect(wrapper.text()).toContain('Channel')
    expect(wrapper.text()).toContain('Agent')
    expect(wrapper.text()).toContain('未安装')
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm --prefix apps/desktop test -- openclaw-console.spec.ts`
Expected: FAIL with module-not-found or component-not-found errors for `OpenClawConsolePage.vue` / `openclaw.ts`.

- [ ] **Step 3: Write the minimal console shell implementation**

Create `apps/desktop/src/pages/OpenClawConsolePage.vue`:

```vue
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
      </header>
      <InstallStatusCard />
      <ModuleSummaryGrid />
    </main>
  </div>
</template>

<script setup lang="ts">
import InstallStatusCard from '../components/InstallStatusCard.vue'
import ModuleSummaryGrid from '../components/ModuleSummaryGrid.vue'
import SidebarNav from '../components/SidebarNav.vue'
</script>
```

Create `apps/desktop/src/components/SidebarNav.vue`:

```vue
<template>
  <aside class="console-sidebar">
    <div class="console-brand">OpenClaw</div>
    <nav class="console-nav">
      <button class="console-nav-item console-nav-item--active">安装</button>
      <button class="console-nav-item">Skills</button>
      <button class="console-nav-item">Channel</button>
      <button class="console-nav-item">Agent</button>
    </nav>
  </aside>
</template>
```

Create `apps/desktop/src/components/ModuleSummaryGrid.vue`:

```vue
<template>
  <section class="summary-grid">
    <article class="summary-card">
      <p class="summary-card__label">Skills</p>
      <h2>未配置</h2>
      <p>安装完成后可加载技能市场与本地技能包。</p>
    </article>
    <article class="summary-card">
      <p class="summary-card__label">Channel</p>
      <h2>未接入</h2>
      <p>后续可管理聊天渠道接入状态。</p>
    </article>
    <article class="summary-card">
      <p class="summary-card__label">Agent</p>
      <h2>0 个实例</h2>
      <p>未来可统一管理 Agent 模板与运行状态。</p>
    </article>
  </section>
</template>
```

Update `apps/desktop/src/App.vue`:

```vue
<template>
  <OpenClawConsolePage />
</template>

<script setup lang="ts">
import OpenClawConsolePage from './pages/OpenClawConsolePage.vue'
</script>

<style src="./styles.css"></style>
```

Update `apps/desktop/src/styles.css` with the console shell base:

```css
* {
  box-sizing: border-box;
}

:root {
  color: #fff;
  background: #0a0a0a;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

body {
  margin: 0;
  min-width: 1280px;
  background: #0a0a0a;
}

button {
  font: inherit;
}

.console-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 240px 1fr;
  background: #0a0a0a;
}

.console-sidebar {
  border-right: 1px solid #242424;
  padding: 28px 18px;
}

.console-brand {
  font-size: 28px;
  font-family: 'Cormorant Garamond', Georgia, serif;
  color: #fff;
}

.console-nav {
  display: grid;
  gap: 8px;
  margin-top: 24px;
}

.console-nav-item {
  border: 1px solid transparent;
  background: transparent;
  color: #d6d6d6;
  text-align: left;
  padding: 12px 14px;
}

.console-nav-item--active {
  background: #c9a962;
  color: #0a0a0a;
}

.console-main {
  padding: 40px 48px;
  display: grid;
  gap: 24px;
}

.console-eyebrow {
  margin: 0;
  color: #8b8b8b;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-size: 12px;
}

.console-header h1 {
  margin: 8px 0;
  font-size: 40px;
  font-family: 'Cormorant Garamond', Georgia, serif;
}

.console-subtitle {
  margin: 0;
  color: #9d9d9d;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.summary-card {
  border: 1px solid #242424;
  background: #111;
  padding: 20px;
}

.summary-card__label {
  margin: 0 0 8px;
  color: #8b8b8b;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 12px;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm --prefix apps/desktop test -- openclaw-console.spec.ts`
Expected: PASS with `1 passed`.

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src/App.vue apps/desktop/src/pages/OpenClawConsolePage.vue apps/desktop/src/components/SidebarNav.vue apps/desktop/src/components/ModuleSummaryGrid.vue apps/desktop/src/styles.css apps/desktop/tests/openclaw-console.spec.ts
git commit -m "feat: replace task shell with openclaw console"
```

### Task 2: Add typed desktop API wrappers and installation status card states

**Files:**
- Create: `apps/desktop/src/types/openclaw.ts`
- Create: `apps/desktop/src/lib/openclaw.ts`
- Create: `apps/desktop/src/components/InstallStatusCard.vue`
- Test: `apps/desktop/tests/openclaw-api.spec.ts`
- Modify: `apps/desktop/tests/openclaw-console.spec.ts`

- [ ] **Step 1: Write the failing API wrapper and card-state tests**

Create `apps/desktop/tests/openclaw-api.spec.ts`:

```ts
import { describe, expect, it, vi } from 'vitest'

const invoke = vi.fn()
vi.mock('@tauri-apps/api/core', () => ({ invoke }))

describe('openclaw desktop api', () => {
  it('calls the install-status command', async () => {
    invoke.mockResolvedValueOnce({ kind: 'not_installed', statusLabel: '未安装', installPath: null })
    const { getOpenClawStatus } = await import('../src/lib/openclaw')

    const result = await getOpenClawStatus()

    expect(invoke).toHaveBeenCalledWith('get_openclaw_status')
    expect(result.kind).toBe('not_installed')
  })
})
```

Append to `apps/desktop/tests/openclaw-console.spec.ts`:

```ts
it('renders install action for not-installed state', async () => {
  const wrapper = mount(OpenClawConsolePage)
  await Promise.resolve()

  expect(wrapper.text()).toContain('OpenClaw 尚未安装')
  expect(wrapper.text()).toContain('安装')
  expect(wrapper.text()).toContain('选择离线包')
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npm --prefix apps/desktop test -- openclaw-api.spec.ts openclaw-console.spec.ts`
Expected: FAIL because `@tauri-apps/api/core` is not installed and `openclaw.ts` / `InstallStatusCard.vue` do not exist.

- [ ] **Step 3: Write the minimal typed API and status-card implementation**

Update `apps/desktop/package.json` dependencies:

```json
{
  "dependencies": {
    "@tauri-apps/api": "^2.8.0",
    "vue": "^3.5.0"
  }
}
```

Create `apps/desktop/src/types/openclaw.ts`:

```ts
export type OpenClawInstallKind =
  | 'checking'
  | 'not_installed'
  | 'installing'
  | 'installed'
  | 'install_failed'

export interface OpenClawInstallStatus {
  kind: OpenClawInstallKind
  statusLabel: string
  installPath: string | null
  message: string
}

export interface ModuleSummary {
  title: string
  value: string
  description: string
}

export interface ConsoleSummary {
  skills: ModuleSummary
  channels: ModuleSummary
  agents: ModuleSummary
}
```

Create `apps/desktop/src/lib/openclaw.ts`:

```ts
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
```

Create `apps/desktop/src/components/InstallStatusCard.vue`:

```vue
<template>
  <section class="install-card">
    <div class="install-card__header">
      <div>
        <p class="install-card__label">Primary Action</p>
        <h2>{{ title }}</h2>
        <p>{{ status.message }}</p>
      </div>
      <span class="install-card__badge">{{ status.statusLabel }}</span>
    </div>

    <div class="install-card__actions" v-if="status.kind === 'not_installed'">
      <button class="install-card__primary">安装</button>
      <button class="install-card__secondary">选择离线包</button>
    </div>

    <div class="install-card__actions" v-else-if="status.kind === 'installed'">
      <button class="install-card__primary" disabled>已安装</button>
    </div>

    <div class="install-card__actions" v-else>
      <button class="install-card__secondary" disabled>{{ status.statusLabel }}</button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { getOpenClawStatus } from '../lib/openclaw'
import type { OpenClawInstallStatus } from '../types/openclaw'

const status = ref<OpenClawInstallStatus>({
  kind: 'checking',
  statusLabel: '检测中',
  installPath: null,
  message: '正在检测本机 OpenClaw 安装状态。',
})

const title = computed(() => {
  if (status.value.kind === 'installed') return 'OpenClaw 已安装'
  if (status.value.kind === 'install_failed') return 'OpenClaw 安装失败'
  if (status.value.kind === 'installing') return 'OpenClaw 安装中'
  return 'OpenClaw 尚未安装'
})

onMounted(async () => {
  status.value = await getOpenClawStatus()
})
</script>
```

Append to `apps/desktop/src/styles.css`:

```css
.install-card {
  border: 1px solid #242424;
  background: #111;
  padding: 28px;
  display: grid;
  gap: 18px;
}

.install-card__header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.install-card__label {
  margin: 0 0 8px;
  color: #8b8b8b;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 12px;
}

.install-card h2 {
  margin: 0 0 10px;
  font-size: 32px;
  font-family: 'Cormorant Garamond', Georgia, serif;
}

.install-card__badge {
  align-self: start;
  border: 1px solid #6b2c2c;
  background: #2a1414;
  color: #f0b0b0;
  padding: 8px 12px;
}

.install-card__actions {
  display: flex;
  gap: 12px;
}

.install-card__primary,
.install-card__secondary {
  padding: 12px 20px;
  border: 1px solid transparent;
  background: transparent;
  color: #fff;
}

.install-card__primary {
  background: #c9a962;
  color: #0a0a0a;
}

.install-card__secondary {
  border-color: #2a2a2a;
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `npm --prefix apps/desktop install && npm --prefix apps/desktop test -- openclaw-api.spec.ts openclaw-console.spec.ts`
Expected: PASS with `2 passed` or more.

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/package.json apps/desktop/src/types/openclaw.ts apps/desktop/src/lib/openclaw.ts apps/desktop/src/components/InstallStatusCard.vue apps/desktop/tests/openclaw-api.spec.ts apps/desktop/tests/openclaw-console.spec.ts apps/desktop/src/styles.css
git commit -m "feat: add openclaw install status shell"
```

### Task 3: Implement Tauri commands for detection and shell summaries

**Files:**
- Modify: `apps/desktop/src-tauri/src/lib.rs:1-87`
- Modify: `apps/desktop/src-tauri/Cargo.toml:1-18`
- Create: `apps/desktop/src-tauri/src/openclaw.rs`
- Create: `apps/desktop/src-tauri/src/state.rs`
- Create: `apps/desktop/src-tauri/tests/openclaw_commands.rs`

- [ ] **Step 1: Write the failing Rust command tests**

Create `apps/desktop/src-tauri/tests/openclaw_commands.rs`:

```rust
use std::path::PathBuf;

#[test]
fn detects_not_installed_when_binary_is_missing() {
    let status = jclaw_desktop::openclaw::detect_install_status(PathBuf::from("/tmp/does-not-exist/openclaw"));

    assert_eq!(status.kind, "not_installed");
    assert_eq!(status.status_label, "未安装");
    assert!(status.install_path.is_none());
}

#[test]
fn returns_console_summary_defaults() {
    let summary = jclaw_desktop::state::default_console_summary();

    assert_eq!(summary.skills.value, "未配置");
    assert_eq!(summary.channels.value, "未接入");
    assert_eq!(summary.agents.value, "0 个实例");
}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cargo test --manifest-path apps/desktop/src-tauri/Cargo.toml openclaw_commands`
Expected: FAIL because `openclaw` and `state` modules do not exist.

- [ ] **Step 3: Write the minimal Rust command layer**

Update `apps/desktop/src-tauri/Cargo.toml`:

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
tauri = { version = "2", features = [] }
```

Create `apps/desktop/src-tauri/src/state.rs`:

```rust
use serde::Serialize;

#[derive(Clone, Serialize)]
pub struct ModuleSummary {
    pub title: String,
    pub value: String,
    pub description: String,
}

#[derive(Clone, Serialize)]
pub struct ConsoleSummary {
    pub skills: ModuleSummary,
    pub channels: ModuleSummary,
    pub agents: ModuleSummary,
}

pub fn default_console_summary() -> ConsoleSummary {
    ConsoleSummary {
        skills: ModuleSummary {
            title: "Skills".into(),
            value: "未配置".into(),
            description: "安装完成后可加载技能市场与本地技能包。".into(),
        },
        channels: ModuleSummary {
            title: "Channel".into(),
            value: "未接入".into(),
            description: "后续可管理聊天渠道接入状态。".into(),
        },
        agents: ModuleSummary {
            title: "Agent".into(),
            value: "0 个实例".into(),
            description: "未来可统一管理 Agent 模板与运行状态。".into(),
        },
    }
}
```

Create `apps/desktop/src-tauri/src/openclaw.rs`:

```rust
use std::path::{Path, PathBuf};

use serde::Serialize;

#[derive(Clone, Serialize)]
pub struct OpenClawInstallStatus {
    pub kind: String,
    pub status_label: String,
    pub install_path: Option<String>,
    pub message: String,
}

pub fn default_binary_path() -> PathBuf {
    #[cfg(target_os = "windows")]
    {
        PathBuf::from(r"C:\OpenClaw\openclaw.exe")
    }
    #[cfg(not(target_os = "windows"))]
    {
        PathBuf::from("/Applications/OpenClaw/openclaw")
    }
}

pub fn detect_install_status(path: PathBuf) -> OpenClawInstallStatus {
    if path.exists() {
        OpenClawInstallStatus {
            kind: "installed".into(),
            status_label: "已安装".into(),
            install_path: Some(path.display().to_string()),
            message: "已检测到本机 OpenClaw 安装文件。".into(),
        }
    } else {
        OpenClawInstallStatus {
            kind: "not_installed".into(),
            status_label: "未安装".into(),
            install_path: None,
            message: "检测到本机固定安装位置不存在 OpenClaw。".into(),
        }
    }
}

#[tauri::command]
pub fn get_openclaw_status() -> OpenClawInstallStatus {
    detect_install_status(default_binary_path())
}

#[tauri::command]
pub fn start_online_install() -> OpenClawInstallStatus {
    OpenClawInstallStatus {
        kind: "installing".into(),
        status_label: "安装中".into(),
        install_path: None,
        message: "正在准备在线安装 OpenClaw。".into(),
    }
}

#[tauri::command]
pub fn start_offline_install() -> OpenClawInstallStatus {
    OpenClawInstallStatus {
        kind: "installing".into(),
        status_label: "安装中".into(),
        install_path: None,
        message: "正在准备离线安装 OpenClaw。".into(),
    }
}
```

Update `apps/desktop/src-tauri/src/lib.rs`:

```rust
pub mod openclaw;
pub mod state;

#[tauri::command]
fn get_console_summary() -> state::ConsoleSummary {
    state::default_console_summary()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            openclaw::get_openclaw_status,
            openclaw::start_online_install,
            openclaw::start_offline_install,
            get_console_summary,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cargo test --manifest-path apps/desktop/src-tauri/Cargo.toml openclaw_commands`
Expected: PASS with `2 passed`.

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src-tauri/src/lib.rs apps/desktop/src-tauri/src/openclaw.rs apps/desktop/src-tauri/src/state.rs apps/desktop/src-tauri/tests/openclaw_commands.rs apps/desktop/src-tauri/Cargo.toml
git commit -m "feat: add openclaw desktop commands"
```

### Task 4: Wire installation actions and status transitions in the frontend

**Files:**
- Modify: `apps/desktop/src/components/InstallStatusCard.vue`
- Modify: `apps/desktop/src/pages/OpenClawConsolePage.vue`
- Modify: `apps/desktop/tests/openclaw-console.spec.ts`
- Modify: `apps/desktop/tests/openclaw-api.spec.ts`

- [ ] **Step 1: Write the failing interaction test**

Append to `apps/desktop/tests/openclaw-console.spec.ts`:

```ts
it('starts online install when install is clicked', async () => {
  const { getOpenClawStatus, getConsoleSummary, startOnlineInstall } = await import('../src/lib/openclaw')
  vi.mocked(getOpenClawStatus).mockResolvedValue({
    kind: 'not_installed',
    statusLabel: '未安装',
    installPath: null,
    message: '检测到本机固定安装位置不存在 OpenClaw。',
  })
  vi.mocked(getConsoleSummary).mockResolvedValue({
    skills: { title: 'Skills', value: '未配置', description: '安装完成后可加载技能市场与本地技能包。' },
    channels: { title: 'Channel', value: '未接入', description: '后续可管理聊天渠道接入状态。' },
    agents: { title: 'Agent', value: '0 个实例', description: '未来可统一管理 Agent 模板与运行状态。' },
  })
  vi.mocked(startOnlineInstall).mockResolvedValue({
    kind: 'installing',
    statusLabel: '安装中',
    installPath: null,
    message: '正在准备在线安装 OpenClaw。',
  })

  const wrapper = mount(OpenClawConsolePage)
  await Promise.resolve()
  await wrapper.get('[data-testid="online-install-button"]').trigger('click')
  await Promise.resolve()

  expect(startOnlineInstall).toHaveBeenCalledTimes(1)
  expect(wrapper.text()).toContain('安装中')
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm --prefix apps/desktop test -- openclaw-console.spec.ts`
Expected: FAIL because buttons are not wired and no `data-testid` exists.

- [ ] **Step 3: Implement minimal action wiring**

Update `apps/desktop/src/components/InstallStatusCard.vue`:

```vue
<template>
  <section class="install-card">
    <div class="install-card__header">
      <div>
        <p class="install-card__label">Primary Action</p>
        <h2>{{ title }}</h2>
        <p>{{ currentStatus.message }}</p>
      </div>
      <span class="install-card__badge">{{ currentStatus.statusLabel }}</span>
    </div>

    <div class="install-card__actions" v-if="currentStatus.kind === 'not_installed'">
      <button class="install-card__primary" data-testid="online-install-button" @click="runOnlineInstall">安装</button>
      <button class="install-card__secondary" data-testid="offline-install-button" @click="runOfflineInstall">选择离线包</button>
    </div>

    <div class="install-card__actions" v-else-if="currentStatus.kind === 'installed'">
      <button class="install-card__primary" disabled>已安装</button>
    </div>

    <div class="install-card__actions" v-else>
      <button class="install-card__secondary" disabled>{{ currentStatus.statusLabel }}</button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { getOpenClawStatus, startOfflineInstall, startOnlineInstall } from '../lib/openclaw'
import type { OpenClawInstallStatus } from '../types/openclaw'

const currentStatus = ref<OpenClawInstallStatus>({
  kind: 'checking',
  statusLabel: '检测中',
  installPath: null,
  message: '正在检测本机 OpenClaw 安装状态。',
})

const title = computed(() => {
  switch (currentStatus.value.kind) {
    case 'installed':
      return 'OpenClaw 已安装'
    case 'installing':
      return 'OpenClaw 安装中'
    case 'install_failed':
      return 'OpenClaw 安装失败'
    default:
      return 'OpenClaw 尚未安装'
  }
})

async function runOnlineInstall() {
  currentStatus.value = await startOnlineInstall()
}

async function runOfflineInstall() {
  currentStatus.value = await startOfflineInstall()
}

onMounted(async () => {
  currentStatus.value = await getOpenClawStatus()
})
</script>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm --prefix apps/desktop test -- openclaw-console.spec.ts`
Expected: PASS with the online-install interaction test green.

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src/components/InstallStatusCard.vue apps/desktop/tests/openclaw-console.spec.ts apps/desktop/tests/openclaw-api.spec.ts apps/desktop/src/pages/OpenClawConsolePage.vue
git commit -m "feat: wire openclaw install actions"
```

### Task 5: Add skeleton pages for Skills, Channel, and Agent

**Files:**
- Create: `apps/desktop/src/pages/SkillsPage.vue`
- Create: `apps/desktop/src/pages/ChannelsPage.vue`
- Create: `apps/desktop/src/pages/AgentsPage.vue`
- Modify: `apps/desktop/src/components/SidebarNav.vue`
- Modify: `apps/desktop/src/pages/OpenClawConsolePage.vue`
- Modify: `apps/desktop/tests/openclaw-console.spec.ts`

- [ ] **Step 1: Write the failing module-shell test**

Append to `apps/desktop/tests/openclaw-console.spec.ts`:

```ts
it('renders skills channel and agent summary sections', async () => {
  const wrapper = mount(OpenClawConsolePage)
  await Promise.resolve()

  expect(wrapper.text()).toContain('安装完成后可加载技能市场与本地技能包。')
  expect(wrapper.text()).toContain('后续可管理聊天渠道接入状态。')
  expect(wrapper.text()).toContain('未来可统一管理 Agent 模板与运行状态。')
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm --prefix apps/desktop test -- openclaw-console.spec.ts`
Expected: FAIL if the summary copy and shell components are not yet aligned.

- [ ] **Step 3: Create the skeleton module pages**

Create `apps/desktop/src/pages/SkillsPage.vue`:

```vue
<template>
  <section class="module-shell">
    <p class="module-shell__label">Skills</p>
    <h2>技能管理</h2>
    <p>安装完成后可加载技能市场与本地技能包。</p>
  </section>
</template>
```

Create `apps/desktop/src/pages/ChannelsPage.vue`:

```vue
<template>
  <section class="module-shell">
    <p class="module-shell__label">Channel</p>
    <h2>聊天渠道管理</h2>
    <p>后续可管理聊天渠道接入状态、连接配置与诊断入口。</p>
  </section>
</template>
```

Create `apps/desktop/src/pages/AgentsPage.vue`:

```vue
<template>
  <section class="module-shell">
    <p class="module-shell__label">Agent</p>
    <h2>Agent 管理</h2>
    <p>未来可统一管理 Agent 模板、实例与运行状态。</p>
  </section>
</template>
```

Append to `apps/desktop/src/styles.css`:

```css
.module-shell {
  border: 1px solid #242424;
  background: #111;
  padding: 20px;
  display: grid;
  gap: 10px;
}

.module-shell__label {
  margin: 0;
  color: #8b8b8b;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 12px;
}
```

Update `apps/desktop/src/pages/OpenClawConsolePage.vue` to render the three page shells beneath the summary grid:

```vue
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
      </header>
      <InstallStatusCard />
      <ModuleSummaryGrid />
      <div class="module-stack">
        <SkillsPage />
        <ChannelsPage />
        <AgentsPage />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import AgentsPage from './AgentsPage.vue'
import ChannelsPage from './ChannelsPage.vue'
import SkillsPage from './SkillsPage.vue'
import InstallStatusCard from '../components/InstallStatusCard.vue'
import ModuleSummaryGrid from '../components/ModuleSummaryGrid.vue'
import SidebarNav from '../components/SidebarNav.vue'
</script>
```

Append to `apps/desktop/src/styles.css`:

```css
.module-stack {
  display: grid;
  gap: 18px;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm --prefix apps/desktop test -- openclaw-console.spec.ts`
Expected: PASS with the module-summary assertions green.

- [ ] **Step 5: Commit**

```bash
git add apps/desktop/src/pages/SkillsPage.vue apps/desktop/src/pages/ChannelsPage.vue apps/desktop/src/pages/AgentsPage.vue apps/desktop/src/pages/OpenClawConsolePage.vue apps/desktop/src/styles.css apps/desktop/tests/openclaw-console.spec.ts
git commit -m "feat: add openclaw management module shells"
```

### Task 6: Update docs and run end-to-end desktop verification

**Files:**
- Modify: `README.md:1-156`
- Test: `apps/desktop/tests/openclaw-console.spec.ts`
- Test: `apps/desktop/tests/openclaw-api.spec.ts`
- Test: `apps/desktop/src-tauri/tests/openclaw_commands.rs`

- [ ] **Step 1: Write the failing README expectation check**

Add this checklist to your working notes before editing README:

```md
- README no longer describes the desktop app as a task workspace.
- README describes OpenClaw install detection.
- README describes online/offline install direction.
- README names Skills / Channel / Agent as console modules.
```

- [ ] **Step 2: Run verification before README update**

Run: `grep -n "TaskWorkspace\|任务" README.md`
Expected: It still shows outdated task-workspace wording.

- [ ] **Step 3: Update README to match OpenClaw Console**

Replace the desktop-purpose sections so README communicates:

```md
## 项目结构
- `apps/desktop`：OpenClaw Console 桌面前端（Vite + Vue 3）
- `apps/desktop/src-tauri`：OpenClaw Console 桌面壳（Tauri 2 + Rust）

## 本地运行
### 3. 启动桌面应用
```bash
cd apps/desktop
npm run tauri:dev
```

桌面应用启动后会先检测 OpenClaw 是否已安装：
- 未安装：首页主按钮显示“安装”
- 已安装：首页主按钮显示“已安装”

当前首版控制台包含四个一级模块：
- 安装
- Skills
- Channel
- Agent
```
```

- [ ] **Step 4: Run the full desktop verification**

Run:
- `npm --prefix apps/desktop install`
- `npm --prefix apps/desktop test`
- `cargo test --manifest-path apps/desktop/src-tauri/Cargo.toml`
- `npm --prefix apps/desktop run build`
- `npm --prefix apps/desktop run tauri:build`

Expected:
- Vitest passes.
- Rust tests pass.
- Vite build passes.
- Tauri build outputs the desktop bundle successfully.

- [ ] **Step 5: Commit**

```bash
git add README.md apps/desktop apps/desktop/src-tauri
git commit -m "docs: align desktop app with openclaw console"
```

---

## Self-Review

### Spec coverage
- Homepage shell: covered by Task 1.
- Install detection and install-state UI: covered by Tasks 2-4.
- Skills / Channel / Agent management shells: covered by Task 5.
- README and end-to-end verification: covered by Task 6.

### Placeholder scan
- No `TODO`, `TBD`, or “implement later” language remains in tasks.
- Each task includes explicit file paths, code, commands, and expected outcomes.

### Type consistency
- Frontend uses `OpenClawInstallStatus`, `ConsoleSummary`, and `ModuleSummary` consistently.
- Rust command names match the frontend invoke names: `get_openclaw_status`, `get_console_summary`, `start_online_install`, `start_offline_install`.

---

Plan complete and saved to `docs/superpowers/plans/2026-03-28-openclaw-console.md`. Two execution options:

1. Subagent-Driven (recommended) - I dispatch a fresh subagent per task, review between tasks, fast iteration

2. Inline Execution - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?