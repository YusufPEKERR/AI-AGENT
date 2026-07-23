from ai_agent.tools.software import project_analyze


def test_project_analyze(tmp_path):
    (tmp_path / "package.json").write_text('{"name": "test", "scripts": {"test": "echo 1"}}')
    res = project_analyze(str(tmp_path))
    assert res.success is True
    assert "Node.js" in res.output
