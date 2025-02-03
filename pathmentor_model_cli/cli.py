from pathlib import Path
import tempfile
from mediatr import Mediator 
from typing import List, Optional

import typer

from pathmentor_core.errors_constants import ERRORS
from pathmentor_model_cli import __app_name__, __version__
from pathmentor_usecases.model.commands.stage_database_command import StageDatabaseCommand
from pathmentor_usecases.model.commands.train_model_command import TrainModelCommand

app = typer.Typer()
mediator = Mediator()
        
@app.command()
def stage(
        connection_string: str = typer.Argument(envvar="ConnectionStrings__DefaultConnection"),
    ) -> None:
    request = StageDatabaseCommand(connection_string)
    result, error = mediator.send(request)
    if error:
        typer.secho(
            f'Staging database failed with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-model: database was staged {result}""",
            fg=typer.colors.GREEN)
        
@app.command()
def train(
        connection_string: str = typer.Argument(envvar="ConnectionStrings__DefaultConnection"),
        output_path: Path = typer.Argument(..., dir_okay=True, file_okay=True, writable=True, resolve_path=True)
    ) -> None:
    request = TrainModelCommand(connection_string, output_path)
    result, error = mediator.send(request)
    if error:
        typer.secho(
            f'Training model failed with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-model: model was trained {result}""",
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
