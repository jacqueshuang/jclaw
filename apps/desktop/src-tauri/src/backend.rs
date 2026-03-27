pub fn build_backend_command(python_bin: &str) -> std::process::Command {
    let mut command = std::process::Command::new(python_bin);
    command.arg("-m").arg("uvicorn").arg("app.main:app");
    command
}
