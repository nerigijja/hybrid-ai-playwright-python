def test_db_table(db_client):
    # Create sample table if not exists
    db_client.run_update('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    r = db_client.run_query("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert len(r) == 1
