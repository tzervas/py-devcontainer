# py-devcontainer

Python DevContainer generator for creating tailored development environments with GitHub Copilot, testing frameworks, and development tools.

## Installation

```bash
pip install py-devcontainer
```

## Usage

Generate a DevContainer configuration interactively:

```bash
devcontainer generate --interactive
```

Generate with specific options:

```bash
devcontainer generate --python-version 3.11 --include-copilot --include-testing
```

Validate a DevContainer configuration:

```bash
devcontainer validate .devcontainer/devcontainer.json
```

## Features

- **Interactive Setup**: Guided configuration with questionary
- **Python Version Support**: 3.9, 3.10, 3.11, 3.12
- **GitHub Copilot Integration**: Optional Copilot and Copilot Chat extensions
- **Testing Frameworks**: Pytest and test explorer integration
- **Development Tools**: Black, isort, pylint, debugpy
- **Docker Support**: Docker-in-Docker feature for container development

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Format code
uv run black src/
uv run isort src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.