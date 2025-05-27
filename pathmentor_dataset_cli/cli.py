from pathlib import Path
from mediatr import Mediator 
from typing import Optional

import typer

from pathmentor_core.errors_constants import ERRORS
from pathmentor_dataset_cli import __app_name__, __version__
from pathmentor_usecases.dataset.commands.build_dataset_command import BuildDatasetCommand
from pathmentor_usecases.dataset.commands.prepare_dataset_command import PrepareDatasetCommand
from pathmentor_usecases.dataset.commands.normalize_dataset_command import NormalizeDatasetCommand

app = typer.Typer()
mediator = Mediator()

@app.command()
def build(
        output_path: Path = typer.Argument(..., dir_okay=True, file_okay=True, writable=True, resolve_path=True)
    ) -> None:
    request = BuildDatasetCommand(output_path)
    result, error = mediator.send(request)
    if error:
        typer.secho(
            f'Building dataset failed with "{ERRORS[error]}": {result}', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-dataset: intial dataset was built {result}""",
            fg=typer.colors.GREEN)

@app.command()
def prepare(
        built_dataset_path: Path = typer.Argument(..., exists=True, file_okay=True, readable=True, resolve_path=True),
        output_path: Path = typer.Argument(..., dir_okay=True, file_okay=True, writable=True, resolve_path=True)
    ) -> None:
    request = PrepareDatasetCommand(built_dataset_path, output_path)
    result, error = mediator.send(request)
    if error:
        typer.secho(
            f'Preparing dataset failed with "{ERRORS[error]}": {result}', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-dataset: intial dataset was prepared {result}""",
            fg=typer.colors.GREEN)

@app.command()
def normalize(
        prepared_dataset_path: Path = typer.Argument(..., exists=True, file_okay=True, readable=True, resolve_path=True),
        connection_string: str = typer.Argument(envvar="ConnectionStrings__DefaultConnection"),
        force: bool = typer.Option(False, "--force", "-f")
    ) -> None:
    request = NormalizeDatasetCommand(prepared_dataset_path, connection_string, force)
    result, error = mediator.send(request)
    if error:
        typer.secho(
            f'Normalizing dataset failed with "{ERRORS[error]}" {result}', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""pathmentor-dataset: intial dataset was normalized {result}""",
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
