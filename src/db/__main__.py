"""
Утилита для управления состоянием базы данных, обертка над alembic.
Можно вызывать из любой директории, а также указать произвольный DSN для базы
данных, отличный от указанного в файле alembic.ini.
"""
import argparse
import os
import sys

from alembic.config import CommandLine, Config
from pathlib import Path
from db.db_params import SYNC_SQLALCHEMY_DATABASE_URL

base_path = Path(__file__).parent.parent.resolve()


def main():

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        "--url",
        default=SYNC_SQLALCHEMY_DATABASE_URL,
        help=(
            "Specify URL using --pg-url or specify "
            "env vars DB_USER, DB_PASSWORD, DB_HOST, DB_NAME"
        ),
    )

    options = alembic.parser.parse_args()

    if "None" in options.url:
        msg = (
            f"Your URL is '{options.url}'.\n"
            "Use --pg-url or env vars DB_USER, DB_PASSWORD, DB_HOST, DB_NAME. \n"
            "Is URL correct? (y/n) \n"
        )
        sys.stdout.write(msg)
        sys.stdout.flush()
        ans = ""
        while ans not in ["y", "n"]:
            ans = sys.stdin.readline().strip()

        if ans == "n":
            sys.stdout.write("Finishing...\n")
            sys.stdout.flush()
            return

    if not os.path.isabs(options.config):
        options.config = base_path / options.config

    config = Config(file_=options.config, ini_section=options.name, cmd_opts=options)

    alembic_location = config.get_main_option("script_location")

    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", str(base_path / alembic_location))
    if options.url:
        config.set_main_option("sqlalchemy.url", options.url)

    exit(alembic.run_cmd(config, options))


if __name__ == "__main__":
    main()