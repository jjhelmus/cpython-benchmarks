import sqlite3
import time

import pyperf


def bench_sqlite_create_table(loops: int, num_tables: int) -> float:
    dt = 0
    for _ in range(loops):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        table_iter = range(num_tables)
        t0 = time.perf_counter()
        for i in table_iter:
            cursor.execute(f"""
                CREATE TABLE test_table_{i} (
                    idx INTEGER PRIMARY KEY,
                    col1 INTEGER,
                    col2 INTEGER,
                    col3 INTEGER,
                    col4 INTEGER,
                    col5 INTEGER
                )
            """)
        dt += time.perf_counter() - t0
        conn.close()
    return dt


def bench_sqlite_insert(loops, num_rows_per_table):
    dt = 0
    for _ in range(loops):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("""
            CREATE TABLE test_table (
                idx INTEGER PRIMARY KEY,
                col1 INTEGER,
                col2 INTEGER,
                col3 INTEGER,
                col4 INTEGER,
                col5 INTEGER
            )
        """)
        rows = [
            (j, j * 2, j * 3, j * 4, j * 5, j * 6) for j in range(num_rows_per_table)
        ]
        t0 = time.perf_counter()
        cursor.executemany(
            "INSERT INTO test_table (idx, col1, col2, col3, col4, col5) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
        dt += time.perf_counter() - t0
        conn.close()
    return dt


def bench_sqlite_create_trigger(loops):
    dt = 0
    for _ in range(loops):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("""
            CREATE TABLE test_table (
                idx INTEGER PRIMARY KEY,
                col1 INTEGER,
                col2 INTEGER,
                col3 INTEGER,
                col4 INTEGER,
                col5 INTEGER
            )
        """)
        t0 = time.perf_counter()
        cursor.execute("""
            CREATE TRIGGER test_table_insert BEFORE INSERT ON test_table
            BEGIN SELECT RAISE(ABORT, 'INSERT not allowed'); END;
        """)

        cursor.execute("""
            CREATE TRIGGER test_table_delete BEFORE DELETE ON test_table
            BEGIN SELECT RAISE(ABORT, 'DELETE not allowed'); END;
        """)

        cursor.execute("""
            CREATE TRIGGER test_table_update_idx BEFORE UPDATE OF idx ON test_table
            BEGIN SELECT RAISE(ABORT, 'UPDATE of idx not allowed'); END;
        """)
        dt += time.perf_counter() - t0
        conn.close()
    return dt


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "sqlite benchmarks"

    runner.bench_time_func("sqlite_create_table", bench_sqlite_create_table, 1_000)
    runner.bench_time_func("sqlite_insert", bench_sqlite_insert, 1_000)
    runner.bench_time_func("sqlite_create_trigger", bench_sqlite_create_trigger)

    args = runner.parse_args()
