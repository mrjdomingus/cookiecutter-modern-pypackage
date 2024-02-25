"""Script that run after the project is generated."""

from pathlib import Path
from typing import Union

PROJECT_DIR = Path.cwd()
PROJECT_TESTS = PROJECT_DIR / Path("tests")
PROJECT_SRC = PROJECT_DIR / Path("src/{{ cookiecutter.project_slug }}")
PROJECT_DOCS = PROJECT_DIR / Path("docs")
PROJECT_VSCODE = PROJECT_DIR / Path(".vscode")


def remove_file(filepath: Union[str, Path]) -> None:
    """Remove a file from the file system."""
    Path.unlink(PROJECT_DIR / filepath)


def add_symlink(path: Path, target: Union[str, Path], target_is_directory: bool = False) -> None:
    """Add symbolic link to target."""
    if path.is_symlink():
        path.unlink()
    path.symlink_to(target, target_is_directory)


def add_vscode_launch_json_file() -> None:
    """Add .vscode/launch.json file."""
    # if directory PROJECT_VSCODE does not exist, create it
    if not PROJECT_VSCODE.exists():
        PROJECT_VSCODE.mkdir()

    vscode_launch_json = PROJECT_VSCODE / "launch.json"
    if not vscode_launch_json.exists():
        vscode_launch_json.write_text(
            """{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File with Arguments",
            "type": "debugpy",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            },
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": "${command:pickArgs}",
            "justMyCode": true
        }
    ]
}
"""
        )


def add_poetry_toml_file() -> None:
    """Add poetry.toml file."""
    vscode_launch_json = PROJECT_DIR / "poetry.toml"
    if not vscode_launch_json.exists():
        vscode_launch_json.write_text(
            """
[virtualenvs]
in-project = true
"""
        )


if __name__ == "__main__":
    if "No command-line interface" in "{{ cookiecutter.command_line_interface }}":
        remove_file(PROJECT_TESTS / "test_cli.py")
        remove_file(PROJECT_SRC / "cli.py")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE.rst")
    else:
        add_symlink(PROJECT_DOCS / "license.rst", "../LICENSE.rst")

    if "{{ cookiecutter.add_code_of_conduct }}" != "y":
        remove_file("CODE_OF_CONDUCT.md")

    if "{{ cookiecutter.add_contributing_file }}" != "y":
        remove_file("CONTRIBUTING.md")

    if "{{ cookiecutter.add_security_file }}" != "y":
        remove_file("SECURITY.md")

    if "{{ cookiecutter.add_codeowners_file }}" != "y":
        remove_file(".github/CODEOWNERS")

    if "{{ cookiecutter.add_funding_file }}" != "y":
        remove_file(".github/FUNDING.yml")

    if "{{ cookiecutter.add_citation_file }}" != "y":
        remove_file("CITATION.cff")

    if "{{ cookiecutter.add_vscode_launch_json_file }}" == "y":
        add_vscode_launch_json_file()

    if "{{ cookiecutter.add_poetry_toml_file }}" == "y":
        add_poetry_toml_file()

    add_symlink(PROJECT_DOCS / "readme.md", "../README.md")
    add_symlink(PROJECT_DOCS / "changelog.md", "../CHANGELOG.md")
