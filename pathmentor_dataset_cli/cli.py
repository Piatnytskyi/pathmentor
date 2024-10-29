from mediatr import Mediator 
from typing import List, Optional

import typer

from pathmentor_core.errors_constants import ERRORS
from pathmentor_dataset_cli import __app_name__, __version__
from pathmentor_usecases.dataset.commands.build_dataset_command import BuildDatasetCommand
from pathmentor_usecases.dataset.commands.prepare_dataset_command import PrepareDatasetCommand
from pathmentor_usecases.dataset.commands.normalize_dataset_command import NormalizeDatasetCommand

app = typer.Typer()
mediator = Mediator()

@app.command()
def build() -> None:
    """Builds the initial dataset"""
    request = BuildDatasetCommand()
    result, error = mediator.send(request)
    if error:
        typer.secho(
            f'Building dataset failed with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-dataset: intial dataset was built """,
            fg=typer.colors.GREEN)

@app.command()
def prepare() -> None:
    """Prepare the initial dataset"""
    request = PrepareDatasetCommand()
    _, error = mediator.send(request)
    if error:
        typer.secho(
            f'Building dataset failed with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-dataset: intial dataset was built """,
            fg=typer.colors.GREEN)

@app.command()
def normalize(connection_string: str = typer.Argument(envvar="CONNECTION_STRING")) -> None:
    """Normalize the initial dataset"""
    request = NormalizeDatasetCommand(connection_string)
    _, error = mediator.send(request)
    if error:
        typer.secho(
            f'Building dataset failed with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-dataset: intial dataset was built """,
            fg=typer.colors.GREEN)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
