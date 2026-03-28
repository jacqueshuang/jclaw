use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

#[test]
fn detects_not_installed_when_binary_is_missing() {
    let unique_suffix = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock should be after unix epoch")
        .as_nanos();
    let missing_path = std::env::temp_dir().join(format!("openclaw-missing-{unique_suffix}/openclaw"));

    let status = jclaw_desktop::openclaw::detect_install_status(PathBuf::from(&missing_path));

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
