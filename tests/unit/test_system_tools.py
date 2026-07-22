from ai_agent.tools.system import execute_command


def test_execute_command():
    res = execute_command("Write-Output 'Hello SysAdmin'")
    assert res.success is True
    assert "Hello SysAdmin" in res.output
