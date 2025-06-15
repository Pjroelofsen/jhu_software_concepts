# query_data.py

from psycopg2 import sql

# ─── 1. SQL STATEMENT BUILDERS ─────────────────────────────────────────────

def build_fetch_stats_query(
    schema: str,
    table: str,
    pk_col: str,
    pk_value,
    limit: int | None = None
) -> sql.Composed:
    """
    Build a fully composed SELECT query using Identifiers and Literals with an optional LIMIT:
      SELECT id, name, score
        FROM schema.table
       WHERE pk_col = pk_value
       [LIMIT limit];
    """
    cols = ['id', 'name', 'score']
    parts: list[sql.SQL] = [
        sql.SQL("SELECT "),
        sql.SQL(', ').join(map(sql.Identifier, cols)),
        sql.SQL(" FROM "),
        sql.Identifier(schema), sql.SQL('.'), sql.Identifier(table),
        sql.SQL(" WHERE "),
        sql.Identifier(pk_col), sql.SQL(' = '), sql.Literal(pk_value)
    ]
    if limit is not None:
        parts += [sql.SQL(' LIMIT '), sql.Literal(limit)]
    parts.append(sql.SQL(';'))
    return sql.Composed(parts)


def build_insert_user_query(
    schema: str,
    table: str,
    data: dict
) -> sql.Composed:
    """
    Build a fully composed INSERT query using Identifiers and Literals:
      INSERT INTO schema.table (col1, col2, ...)
           VALUES (val1, val2, ...);
    """
    cols = list(data.keys())
    vals = list(data.values())
    return sql.Composed([
        sql.SQL("INSERT INTO "),
        sql.Identifier(schema), sql.SQL('.'), sql.Identifier(table),
        sql.SQL(" ("), sql.SQL(', ').join(map(sql.Identifier, cols)), sql.SQL(") VALUES ("),
        sql.SQL(', ').join(sql.Literal(v) for v in vals),
        sql.SQL(");")
    ])


def build_update_status_query(
    schema: str,
    table: str,
    id_col: str,
    id_val,
    updates: dict
) -> sql.Composed:
    """
    Build a fully composed UPDATE query using Identifiers and Literals:
      UPDATE schema.table
         SET col1 = val1, col2 = val2, ...
       WHERE id_col = id_val;
    """
    set_clauses = [
        sql.Composed([
            sql.Identifier(col), sql.SQL(' = '), sql.Literal(val)
        ])
        for col, val in updates.items()
    ]
    return sql.Composed([
        sql.SQL("UPDATE "),
        sql.Identifier(schema), sql.SQL('.'), sql.Identifier(table),
        sql.SQL(" SET "),
        sql.SQL(', ').join(set_clauses),
        sql.SQL(" WHERE "),
        sql.Identifier(id_col), sql.SQL(' = '), sql.Literal(id_val),
        sql.SQL(';')
    ])

# ─── 2. EXECUTOR ───────────────────────────────────────────────────────────

def execute_query(
    conn,
    query: sql.Composed
):
    """
    Execute any composed SQL query. If it's a SELECT, fetchall; otherwise commit.
    """
    with conn.cursor() as cur:
        cur.execute(query)
        sql_text = query.as_string(conn).lstrip().upper()
        if sql_text.startswith('SELECT'):
            return cur.fetchall()
        conn.commit()

# ─── 3. CONVENIENCE WRAPPERS ────────────────────────────────────────────────

def fetch_stats(
    conn,
    schema: str,
    table: str,
    pk_col: str,
    pk_value,
    limit: int | None = None
):
    q = build_fetch_stats_query(schema, table, pk_col, pk_value, limit)
    return execute_query(conn, q)


def insert_user(
    conn,
    schema: str,
    table: str,
    data: dict
):
    q = build_insert_user_query(schema, table, data)
    return execute_query(conn, q)


def update_status(
    conn,
    schema: str,
    table: str,
    id_col: str,
    id_val,
    updates: dict
):
    q = build_update_status_query(schema, table, id_col, id_val, updates)
    return execute_query(conn, q)
