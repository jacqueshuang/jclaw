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
