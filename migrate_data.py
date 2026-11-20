
import sqlite3
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert

from backend.database import Base, engine
from backend import (
    models,
    agent_models,
    workflow_models,
    task_models,
    execution_models
)

tables = ["users", "agents", "workflows", "tasks", "executions"]

sqlite_conn = sqlite3.connect("enterprise_ai.db")
sqlite_conn.row_factory = sqlite3.Row

try:
    with engine.begin() as pg_conn:
        for table_name in tables:
            table = Base.metadata.tables[table_name]

            rows = sqlite_conn.execute(
                f'SELECT * FROM "{table_name}"'
            ).fetchall()

            for row in rows:
                record = dict(row)

                for column in table.columns:
                    value = record.get(column.name)

                    if value is not None and column.type.python_type is datetime:
                        if isinstance(value, str):
                            record[column.name] = datetime.fromisoformat(
                                value.replace("Z", "+00:00")
                            )

                statement = (
                    pg_insert(table)
                    .values(**record)
                    .on_conflict_do_nothing()
                )

                pg_conn.execute(statement)

            print(f"{table_name}: {len(rows)} records processed")

        for table_name in tables:
            pg_conn.execute(
                text(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table_name}', 'id'),
                        COALESCE((SELECT MAX(id) FROM "{table_name}"), 1),
                        EXISTS(SELECT 1 FROM "{table_name}")
                    )
                """)
            )

    print("PostgreSQL migration completed successfully!")

finally:
    sqlite_conn.close()
