use std::path::PathBuf;

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
    #[cfg(target_os = "macos")]
    {
        PathBuf::from("/Applications/OpenClaw/openclaw")
    }
    #[cfg(all(not(target_os = "windows"), not(target_os = "macos")))]
    {
        PathBuf::from("/opt/openclaw/openclaw")
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
