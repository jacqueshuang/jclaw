#[test]
fn backend_command_uses_python_module_entrypoint() {
    let command = jclaw_desktop::backend::build_backend_command("python");

    assert_eq!(command.get_program().to_string_lossy(), "python");
}
