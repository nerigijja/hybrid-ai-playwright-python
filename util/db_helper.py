def exists_table(db_client, table):
    r = db_client.run_query("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return len(r) > 0
