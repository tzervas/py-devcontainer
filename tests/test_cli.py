"""Tests for devcontainer CLI."""

import pytest
from click.testing import CliRunner
from devcontainer.cli import main


def test_cli_help():
    """Test that CLI shows help."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "DevContainer generator" in result.output


def test_generate_command():
    """Test generate command with basic options."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["generate", "--python-version", "3.11"])
        assert result.exit_code == 0
        assert "Generating DevContainer" in result.output

        # Check if files were created
        import os
        assert os.path.exists(".devcontainer/devcontainer.json")
        assert os.path.exists(".devcontainer/Dockerfile")