"""Command-line interface for devcontainer generator."""

from pathlib import Path

import click
import questionary
import yaml
from jinja2 import Environment, FileSystemLoader


@click.group()
@click.version_option()
def main():
    """DevContainer generator for creating tailored Python development environments."""
    pass


@main.command()
@click.option("--interactive", "-i", is_flag=True, help="Run in interactive mode")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
@click.option(
    "--python-version", default="3.12", help="Python version for devcontainer"
)
@click.option(
    "--include-copilot", is_flag=True, default=True, help="Include GitHub Copilot"
)
@click.option(
    "--include-testing", is_flag=True, default=True, help="Include testing frameworks"
)
def generate(interactive, output, python_version, include_copilot, include_testing):
    """Generate a DevContainer configuration for Python development."""
    output_path = Path(output) if output else Path.cwd() / ".devcontainer"

    if interactive:
        python_version = questionary.select(
            "Select Python version:",
            choices=["3.9", "3.10", "3.11", "3.12"],
            default=python_version,
        ).ask()

        include_copilot = questionary.confirm(
            "Include GitHub Copilot?", default=include_copilot
        ).ask()

        include_testing = questionary.confirm(
            "Include testing frameworks?", default=include_testing
        ).ask()

    click.echo(f"🔧 Generating DevContainer for Python {python_version}")
    click.echo(f"📁 Output directory: {output_path}")

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate devcontainer.json
    config = {
        "name": f"Python {python_version} Development",
        "image": f"mcr.microsoft.com/devcontainers/python:{python_version}",
        "features": {
            "ghcr.io/devcontainers/features/github-cli:1": {},
            "ghcr.io/devcontainers/features/docker-in-docker:2": {},
        },
        "customizations": {
            "vscode": {
                "extensions": [
                    "ms-python.python",
                    "ms-python.black-formatter",
                    "ms-python.isort",
                    "ms-python.pylint",
                    "ms-python.debugpy",
                ],
                "settings": {
                    "python.defaultInterpreterPath": "/usr/local/bin/python",
                    "python.formatting.provider": "black",
                    "python.linting.enabled": True,
                    "python.linting.pylintEnabled": True,
                    "editor.formatOnSave": True,
                    "editor.codeActionsOnSave": {"source.fixAll": "explicit"},
                    "git.autofetch": True,
                    "terminal.integrated.shell.linux": "/bin/bash",
                },
            }
        },
        "postCreateCommand": "pip install uv && uv sync",
        "remoteUser": "vscode",
    }

    if include_copilot:
        config["customizations"]["vscode"]["extensions"].extend(
            ["GitHub.copilot", "GitHub.copilot-chat"]
        )

    if include_testing:
        config["customizations"]["vscode"]["extensions"].extend(
            ["ms-python.pytest", "hbenl.vscode-test-explorer"]
        )

    # Write devcontainer.json
    with open(output_path / "devcontainer.json", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    # Generate Dockerfile if needed
    dockerfile_content = f"""FROM mcr.microsoft.com/devcontainers/python:{python_version}

# Install additional tools
RUN pip install --upgrade pip uv

# Set up user
USER vscode
"""
    with open(output_path / "Dockerfile", "w") as f:
        f.write(dockerfile_content)

    click.echo("✅ DevContainer configuration generated successfully")


@main.command()
@click.argument("config_path", type=click.Path(exists=True))
def validate(config_path):
    """Validate a DevContainer configuration."""
    config_file = Path(config_path)
    click.echo(f"🔍 Validating DevContainer config: {config_file}")

    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)

        # Basic validation
        required_fields = ["name", "image"]
        for field in required_fields:
            if field not in config:
                click.echo(f"❌ Missing required field: {field}")
                return

        click.echo("✅ DevContainer configuration is valid")

    except Exception as e:
        click.echo(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    main()
