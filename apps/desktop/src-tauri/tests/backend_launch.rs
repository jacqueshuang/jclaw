#[test]
fn backend_command_uses_python_module_entrypoint() {
    let command = jclaw_desktop::backend::build_backend_command("python");
    let args: Vec<_> = command
        .get_args()
        .map(|arg| arg.to_string_lossy().into_owned())
        .collect();

    assert_eq!(command.get_program().to_string_lossy(), "python");
    assert_eq!(args, vec!["-m", "uvicorn", "app.main:app"]);
}
