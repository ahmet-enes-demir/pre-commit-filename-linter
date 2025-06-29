# Pre-commit Filename Linter

A pre-commit filename linter to enforce file naming conventions based on Soliner's naming standards.

## Features

- ✅ Enforces kebab-case for most files and directories
- ✅ Allows snake_case for Python files
- ✅ Detects empty files and duplicate files
- ✅ Optional Unicode support for international projects
- ✅ YAML configuration file support

## Installation

Basic setup:

```yaml
repos:
  - repo: https://github.com/ahmet-enes-demir/pre-commit-filename-linter.git
    rev: v1.3.0
    hooks:
      - id: check-file-names
      - id: check-directory-names
      - id: check-empty-files
      - id: check-duplicate-files
```

With arguments:

```yaml
repos:
  - repo: https://github.com/ahmet-enes-demir/pre-commit-filename-linter.git
    rev: v1.3.0
    hooks:
      - id: check-file-names
        args: ['--config', '.naming-convention.yaml']
      - id: check-directory-names
        args: ['--exclude', 'temp.*', '--allow-unicode']
      - id: check-empty-files
        args: ['--allow-empty']
      - id: check-duplicate-files
        args: ['--allow-duplicates']
```

Using Docker:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-file-names-docker
        name: Check file names (Docker)
        entry: ahmetenesdemir/pre-commit-filename-linter:latest check-file-names
        language: docker_image
        files: .*
        pass_filenames: true
        args: ['--config', '.naming-convention.yaml']
```

## Naming Rules

- **Files**: kebab-case (`user-guide.md`, `api-docs.md`)
- **Python files**: snake_case (`user_service.py`, `api_client.py`)
- **Directories**: kebab-case (`user-service/`, `test-data/`)
- **Config files**: both kebab-case and snake_case allowed
- **Standard files**: `README.md`, `LICENSE`, `Dockerfile` etc. preserved

## Examples

✅ **Good**:
```
user-authentication.md
user_service.py
docker-compose.yml
user-service/
```

❌ **Bad**:
```
UserAuthentication.md    # Uppercase
user_authentication.md  # Underscores in non-Python
doc1.md                 # Not descriptive
system architecture.md  # Spaces
```

## Configuration

Create `.naming-convention.yaml`:

```yaml
files:
  use-hyphen: true
  use-underscore: false
  use-capital: false
  allow-unicode: false
  min-length: 3
  max-length: 50

directories:
  use-hyphen: true
  use-underscore: false
  use-capital: false
  allow-unicode: false

empty-files:
  allow-empty: false

duplicate-files:
  allow-duplicates: false

exclude-patterns:
  - ".*\\.tmp$"
  - "__pycache__"
  - "\\.git/"
```
