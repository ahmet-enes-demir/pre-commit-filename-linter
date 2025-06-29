# Configuration Guide

This guide provides detailed information about configuring the pre-commit filename linter using the `.naming-convention.yaml` file.

## Configuration File Structure

The configuration file uses YAML format and supports the following sections:

- `files` - File naming rules
- `directories` - Directory naming rules
- `empty-files` - Empty file detection settings
- `duplicate-files` - Duplicate file detection settings
- `exclude-patterns` - Patterns to exclude from checking

## File Configuration

### Basic Options

```yaml
files:
  use-hyphen: true          # Allow kebab-case (default: true)
  use-underscore: false     # Allow snake_case (default: false)
  use-capital: false        # Allow capital letters (default: false)
  allow-unicode: false      # Allow non-English characters (default: false)
  allow-spaces: false       # Allow spaces in filenames (default: false)
```

### Case Style Options

```yaml
files:
  use-pascal-case: false           # Allow PascalCase (default: false)
  use-camel-case: false            # Allow camelCase (default: false)
  use-screaming-snake-case: false  # Allow SCREAMING_SNAKE_CASE (default: false)
```

**Important:** To use PascalCase, camelCase, or SCREAMING_SNAKE_CASE, you must also set `use-capital: true`.

### Length Constraints

```yaml
files:
  min-length: 3     # Minimum filename length (default: 1)
  max-length: 50    # Maximum filename length (default: 100)
```

### File Type Specific Rules

```yaml
files:
  python-files:
    use-underscore: true    # Python files use snake_case (default: true)
    use-hyphen: false       # Disable hyphens for Python files

  config-files:
    use-underscore: true    # Allow snake_case for config files
    use-hyphen: true        # Allow kebab-case for config files
```

### Reject Patterns

```yaml
files:
  reject-patterns:
    - "^doc[0-9]*$"     # Reject doc1, doc2, etc.
    - "^file[0-9]*$"    # Reject file1, file2, etc.
    - "^temp.*$"        # Reject files starting with temp
    - "^test[0-9]*$"    # Reject test1, test2, etc.
```

## Directory Configuration

Directory configuration follows the same structure as files:

```yaml
directories:
  use-hyphen: true
  use-underscore: false
  use-capital: false
  use-pascal-case: false
  use-camel-case: false
  use-screaming-snake-case: false
  allow-unicode: false
  min-length: 3
  max-length: 50

  reject-patterns:
    - "^dir[0-9]*$"
    - "^folder[0-9]*$"
    - "^temp.*$"
```

## Empty Files Configuration

```yaml
empty-files:
  allow-empty: false    # Disallow empty files (default: false)
```

**Automatically Allowed Empty Files:**
- `__init__.py` - Python package markers
- `.gitkeep` - Git directory placeholders
- `.gitignore` - Git ignore files
- `.env.example` - Environment file templates
- `requirements.txt` - Python dependencies
- `CHANGELOG.md` - Project changelogs
- `TODO.md` - Project todo lists

## Duplicate Files Configuration

```yaml
duplicate-files:
  allow-duplicates: false    # Disallow duplicate files (default: false)
```

## Exclude Patterns

Use regex patterns to exclude files and directories from checking:

```yaml
exclude-patterns:
  - ".*\\.tmp$"        # Exclude temporary files
  - "__pycache__"      # Exclude Python cache directories
  - "\\.git/"          # Exclude git directories
  - "node_modules"     # Exclude Node.js modules
  - "\\.pytest_cache"  # Exclude pytest cache
  - "build/"           # Exclude build directories
  - "dist/"            # Exclude distribution directories
```

## Configuration Examples

### JavaScript/TypeScript Project

```yaml
files:
  use-hyphen: false
  use-camel-case: true
  use-capital: true
  allow-unicode: false

directories:
  use-hyphen: true
  use-camel-case: true
  use-capital: true

exclude-patterns:
  - "node_modules"
  - "\\.next/"
  - "build/"
  - "dist/"
```

### Java Project

```yaml
files:
  use-hyphen: false
  use-pascal-case: true
  use-capital: true

directories:
  use-hyphen: true
  use-pascal-case: true
  use-capital: true

exclude-patterns:
  - "target/"
  - "\\.class$"
  - "\\.jar$"
```

### Python Project

```yaml
files:
  use-hyphen: true
  python-files:
    use-underscore: true

directories:
  use-hyphen: true
  use-underscore: true

exclude-patterns:
  - "__pycache__"
  - "\\.pyc$"
  - "\\.pytest_cache"
  - "venv/"
  - ".venv/"
```

### Multi-Language Project

```yaml
files:
  use-hyphen: true
  use-pascal-case: true
  use-camel-case: true
  use-capital: true

directories:
  use-hyphen: true
  use-pascal-case: true
  use-camel-case: true
  use-capital: true

exclude-patterns:
  - "node_modules"
  - "__pycache__"
  - "target/"
  - "build/"
  - "dist/"
```

## Unicode Support

Enable Unicode support for international projects:

```yaml
files:
  allow-unicode: true

directories:
  allow-unicode: true
```

**Examples with Unicode:**
- Turkish: `internet-değişimi.md`, `çayır/`
- German: `straße-info.md`, `größe/`
- French: `café-menu.md`, `résumé/`

## Troubleshooting

### Common Issues

1. **"Files should use kebab-case" but capitals are allowed**
   - Ensure `use-capital: true` is set when using PascalCase or camelCase

2. **"Underscores not allowed" with SCREAMING_SNAKE_CASE**
   - The linter automatically allows underscores when `use-screaming-snake-case: true`

3. **Unicode characters rejected**
   - Set `allow-unicode: true` in both files and directories sections

4. **Python files failing snake_case**
   - Python files automatically use snake_case, this is expected behavior

### Validation Priority

The linter validates in this order:
1. Exclude patterns (skip if matched)
2. Standard allowed files (README.md, LICENSE, etc.)
3. File type specific rules (Python, config files)
4. General file rules
5. Case style validation

### Performance Tips

- Use specific exclude patterns to skip unnecessary files
- Place frequently matched patterns first in exclude-patterns list
- Use anchored regex patterns (^, $) for better performance
