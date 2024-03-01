from datasette_test import wait_until_responds
import pytest
import sqlite3
from subprocess import Popen, PIPE
import sys


@pytest.fixture(scope="session")
def ds_server(tmp_path_factory):
    tmpdir = tmp_path_factory.mktemp("tmp")
    db_path = str(tmpdir / "data.db")
    db = sqlite3.connect(db_path)
    with db:
        db.execute(
            """
        create table demo (
            id integer primary key,
            category text,
            value_int integer,
            value_float float
        )           
        """
        )
        db.execute(
            """
        insert into demo (category, value_int, value_float)
        values
            ('a', 1, 1.1),
            ('a', 2, 2.2),
            ('b', 3, 3.3),
            ('b', 4, 4.4)
        """
        )
    process = Popen(
        [
            sys.executable,
            "-m",
            "datasette",
            "--port",
            "8127",
            str(db_path),
        ],
        stdout=PIPE,
    )
    wait_until_responds("http://localhost:8127/")
    yield "http://localhost:8127"
    process.terminate()
    process.wait()
