# Pre-commit Filename Linter

A pre-commit filename linter to enforce file naming conventions based on Soliner's naming standards.

## Features

- ✅ Enforces kebab-case for most files and directories
- ✅ Allows snake_case for Python files
- ✅ Supports both snake_case and kebab-case for config files
- ✅ Preserves standard file names (README.md, Dockerfile, etc.)
- ✅ Checks for descriptive file and directory names
- ✅ Prevents special characters and spaces
- ✅ Exclude files and directories with regex patterns
- ✅ YAML configuration file support

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/ahmet-enes-demir/pre-commit-filename-linter.git
    rev: v1.0.0
    hooks:
      - id: check-file-names        # Check file names
      - id: check-directory-names   # Check directory names (scans entire repo)
```

With custom exclude patterns:

```yaml
repos:
  - repo: https://github.com/ahmet-enes-demir/pre-commit-filename-linter.git
    rev: v1.0.0
    hooks:
      - id: check-file-names
        args: ['--exclude', '.*\.tmp$', '--exclude', '__pycache__']
      - id: check-directory-names
        args: ['--exclude', 'temp.*']
```

With custom configuration file:

```yaml
repos:
  - repo: https://github.com/ahmet-enes-demir/pre-commit-filename-linter.git
    rev: v1.0.0
    hooks:
      - id: check-file-names
        args: ['--config', '.naming-convention.yaml']
      - id: check-directory-names
        args: ['--config', '.naming-convention.yaml']
```

## Naming Rules

### General Files
- Use **kebab-case** (lowercase with hyphens)
- Examples: `user-guide.md`, `api-documentation.md`

### Directories
- Use **kebab-case** (lowercase with hyphens)
- Examples: `user-service/`, `api-documentation/`, `test-data/`

### Python Files
- Use **snake_case** (lowercase with underscores)
- Examples: `user_service.py`, `api_client.py`

### Config Files
- Support both **snake_case** and **kebab-case**
- Examples: `docker-compose.yml`, `app_config.json`

### Allowed Standard Files
- `README.md`, `LICENSE`, `CHANGELOG.md`
- `Dockerfile`, `Makefile`
- `.gitignore`, `.env.example`
- And other common project files

## Examples

✅ **Good examples:**
```
Files:
user-authentication.md
api-documentation.md
system-architecture.png
user_service.py
config.yml
docker-compose.yml
README.md

Directories:
user-service/
api-documentation/
test-data/
src/
tests/
```

❌ **Bad examples:**
```
Files:
UserAuthentication.md     # Uses uppercase
user_authentication.md   # Uses underscores for non-Python files
doc1.md                  # Not descriptive
system architecture.md   # Contains spaces
file@name.md            # Special characters

Directories:
UserService/             # Uses uppercase
user_service/           # Uses underscores
dir1/                   # Not descriptive
my folder/              # Contains spaces
```

## Manual Usage

You can also run the checkers manually:

```bash
# Check files
python3 src/file_name_checker.py file1.md file2.py

# Check directories
python3 src/directory_checker.py src/ tests/ docs/

# Exclude files/directories with patterns
python3 src/file_name_checker.py --exclude '.*\.tmp$' --exclude '__pycache__' file1.md file2.py
python3 src/directory_checker.py --exclude 'temp.*' src/ tests/

# Use custom configuration
python3 src/file_name_checker.py --config .naming-convention.yaml file1.md file2.py
python3 src/directory_checker.py --config .naming-convention.yaml src/ tests/
```

## Configuration

The checker automatically detects file types and applies appropriate naming conventions. Use `--exclude` flag to skip files matching regex patterns or `--config` to use a YAML configuration file.

### Configuration File Format

Create a YAML file (e.g., `.naming-convention.yaml`) with your naming rules:

```yaml
# File naming configuration
files:
  use-hyphen: true
  use-underscore: false
  use-capital: false
  allow-spaces: false
  require-descriptive: true
  min-length: 3
  max-length: 50

  # File type specific rules
  python-files:
    use-underscore: true
    use-hyphen: false

  config-files:
    use-underscore: false
    use-hyphen: true

  # Generic name patterns to reject
  reject-patterns:
    - "^doc[0-9]*$"
    - "^file[0-9]*$"
    - "^temp.*$"
    - "^tmp.*$"
    - "^test[0-9]*$"

# Directory naming configuration
directories:
  use-hyphen: true
  use-underscore: false
  use-capital: false
  allow-spaces: false
  require-descriptive: true
  min-length: 3
  max-length: 50

  # Generic name patterns to reject
  reject-patterns:
    - "^dir[0-9]*$"
    - "^folder[0-9]*$"
    - "^temp.*$"
    - "^tmp.*$"
    - "^test[0-9]*$"

# Exclude files and directories matching these patterns
exclude-patterns:
  - ".*\\.tmp$"
  - "__pycache__"
  - "\\.git/"
```
