from typing import Annotated

import typer

from rich import print

from api.api_v1.auth.services.redis_tokens import redis_token

app = typer.Typer(
    name="token",
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Tokens managment",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="Check exist token or not",
        ),
    ],
):
    """
    Check exist token or not
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exist[/green]."
            if redis_token.check_token(token)
            else "[red]not exist[/red]."
        ),
    )
