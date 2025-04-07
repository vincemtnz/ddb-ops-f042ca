from datetime import datetime
from typing import Annotated
from typer import Typer, Option, BadParameter

from ddb_ops.config.logger import setup_logger
from ddb_ops.tasks.seed import CURRENT_DATE, run_seed
from ddb_ops.tasks.reading import run_batch_get, run_query

cli = Typer()


def validate_date(value: str):
    try:
        validated_date = datetime.strptime(value, "%Y-%m-%d")
        return validated_date.strftime("%Y-%m-%d")
    except ValueError:
        raise BadParameter("Date must be in YYYY-MM-DD format")


@cli.command()
def seed(
    total: Annotated[int, Option("--total", help="Number of records to generate")],
    date: Annotated[str, Option( "--date", callback=validate_date, help="Date in YYYY-MM-DD format. Defaults to the current date.", )] = CURRENT_DATE,
    prefix: Annotated[str, Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")] = "XXA",
    execute: Annotated[bool, Option("--execute", help="Write the values to DynamoDB")] = False,
):
    run_seed(total=total, date=date, prefix=prefix, execute=execute)


@cli.command()
def batch_get(
    prefix: Annotated[str, Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")] = "XXA",
    total: Annotated[int, Option("--total", help="Total number of records to read")] = 10,
    execute: Annotated[bool, Option("--execute", help="Write the values to DynamoDB")] = False,
):
    run_batch_get(prefix=prefix, total=total, execute=execute)

@cli.command()
def query(
    prefix: Annotated[str, Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")] = "XXA",
    total: Annotated[int, Option("--total", help="Total number of records to read")] = 10,
    execute: Annotated[bool, Option("--execute", help="Write the values to DynamoDB")] = False,
):
    run_query(prefix=prefix, total=total, execute=execute)



if __name__ == '__main__':
    setup_logger()
    cli()
