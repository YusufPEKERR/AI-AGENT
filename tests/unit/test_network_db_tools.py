from ai_agent.tools.network_db import db_query


def test_db_query(tmp_path):
    db_file = tmp_path / "test.db"
    res1 = db_query("sqlite", "CREATE TABLE users (id INT, name TEXT);", str(db_file))
    assert res1.success is True

    res2 = db_query("sqlite", "INSERT INTO users VALUES (1, 'Alice');", str(db_file))
    assert res2.success is True

    res3 = db_query("sqlite", "SELECT * FROM users;", str(db_file))
    assert res3.success is True
    assert "Alice" in res3.output
