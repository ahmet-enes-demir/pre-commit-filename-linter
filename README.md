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
        entry: ahmetenesdemir/pre-commit-filename-linter:latest filename-linter
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

## Manual Usage

```bash
# Basic usage
python3 src/file_name_checker.py *.md
python3 src/directory_checker.py

# With configuration file
python3 src/file_name_checker.py --config .naming-convention.yaml *.md

# With exclude patterns
python3 src/file_name_checker.py --exclude '.*\.tmp$' --exclude '__pycache__' *.py

# Enable Unicode support
python3 src/file_name_checker.py --allow-unicode türkçe-dosya.md
python3 src/directory_checker.py --allow-unicode

# Allow empty files and duplicates
python3 src/empty_file_checker.py --allow-empty
python3 src/duplicate_file_checker.py --allow-duplicates
```

## Docker Usage

```bash
# Basic usage
docker run --rm -v $(pwd):/app ahmetenesdemir/pre-commit-filename-linter:latest filename-linter *.md

# With configuration file
docker run --rm -v $(pwd):/app ahmetenesdemir/pre-commit-filename-linter:latest filename-linter --config .naming-convention.yaml

# With exclude patterns
docker run --rm -v $(pwd):/app ahmetenesdemir/pre-commit-filename-linter:latest filename-linter --exclude '.*\.tmp$' *.py

# Enable Unicode support
docker run --rm -v $(pwd):/app ahmetenesdemir/pre-commit-filename-linter:latest filename-linter --allow-unicode

# Check for empty files (allow empty)
docker run --rm -v $(pwd):/app ahmetenesdemir/pre-commit-filename-linter:latest empty-file-linter --allow-empty
```

## Available Commands

| Command | Description |
|---------|-------------|
| `filename-linter` | Check file naming conventions |
| `directory-linter` | Check directory naming conventions |
| `empty-file-linter` | Detect empty files |
| `duplicate-file-linter` | Find duplicate files |
