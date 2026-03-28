pub mod backend;
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
