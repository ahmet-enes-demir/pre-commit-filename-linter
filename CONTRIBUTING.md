# Contributing to Pre-commit Filename Linter

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/pre-commit-filename-linter.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run tests
python3 -m pytest tests/

# Run individual checkers
python3 src/file_name_checker.py --help
python3 src/directory_checker.py --help
python3 src/empty_file_checker.py --help
python3 src/duplicate_file_checker.py --help
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for new functions and classes
- Keep functions focused and small

## Testing

- Add tests for new features in the `tests/` directory
- Ensure all existing tests pass
- Test both positive and negative cases
- Include configuration file tests

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include tests for new functionality
- Update documentation if needed
- Ensure CI checks pass

## Reporting Issues

When reporting bugs or requesting features:

- Use the issue templates
- Provide clear reproduction steps
- Include relevant configuration files
- Specify your environment details

## Questions?

Feel free to open an issue for questions or discussions about the project.
