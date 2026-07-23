from pathlib import Path
from ai_agent.tools.filesystem import (
    write_file, read_file, list_directory, copy_move_delete, search_files
)


def test_write_and_read_file(tmp_path):
    target = tmp_path / "test.txt"
    res_w = write_file(str(target), "Hello World")
    assert res_w.success is True

    res_r = read_file(str(target))
    assert res_r.success is True
    assert res_r.output == "Hello World"


def test_list_directory(tmp_path):
    (tmp_path / "file1.txt").write_text("1")
    res = list_directory(str(tmp_path))
    assert res.success is True
    assert "file1.txt" in res.output


def test_copy_move_delete(tmp_path):
    src = tmp_path / "src.txt"
    src.write_text("content")
    dest = tmp_path / "dest.txt"

    res_c = copy_move_delete("copy", str(src), str(dest))
    assert res_c.success is True
    assert dest.exists()

    res_d = copy_move_delete("delete", str(src))
    assert res_d.success is True
    assert not src.exists()
