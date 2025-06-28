#!/usr/bin/env python3
"""File name checker for pre-commit hooks."""
# Version 1.0.0

import argparse
import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Set, Dict, Any


class FileNameChecker:
    """Check file names against naming conventions."""

    # Common files that should keep their standard names
    ALLOWED_UPPERCASE = {
        'README.md', 'LICENSE', 'CHANGELOG.md', 'Dockerfile', 'Makefile',
        'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md', 'AUTHORS',
        'COPYING', 'INSTALL', 'NEWS', 'TODO', 'VERSION', 'MANIFEST.in',
        'requirements.txt', 'setup.py', 'setup.cfg', 'pyproject.toml',
        'tox.ini', 'pytest.ini', '.gitignore', '.gitattributes', '.dockerignore',
        '.env.example', '.env.template', '__init__.py'
    }

    # Files that can have underscores (Python convention)
    PYTHON_FILES = {'.py', '.pyx', '.pyi'}

    # Files that commonly use underscores
    CONFIG_FILES = {'.yml', '.yaml', '.json', '.toml', '.ini', '.cfg', '.conf'}

    def __init__(self, exclude_patterns=None, config_file=None, allow_unicode=False):
        self.errors = []
        self.exclude_patterns = exclude_patterns or []
        self.allow_unicode = allow_unicode
        self.config = self.load_config(config_file) if config_file else None
        if self.config and 'exclude-patterns' in self.config:
            self.exclude_patterns.extend(self.config['exclude-patterns'])
        # Override allow_unicode from config if specified
        if self.config and 'files' in self.config:
            self.allow_unicode = self.config['files'].get('allow-unicode', self.allow_unicode)

    def check_kebab_case(self, filename: str) -> bool:
        """Check if filename follows kebab-case convention."""
        # Remove extension for checking
        name_without_ext = Path(filename).stem

        # Reject if contains underscores
        if '_' in name_without_ext:
            return False

        # Allow single words without hyphens
        if '-' not in name_without_ext:
            return name_without_ext.islower() and self.is_alphanumeric_unicode(name_without_ext.replace('.', ''))

        # Check kebab-case pattern
        if self.allow_unicode:
            return bool(re.match(r'^[a-z0-9çğıöşüâêîôû]+(-[a-z0-9çğıöşüâêîôû]+)*$', name_without_ext, re.UNICODE))
        else:
            return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name_without_ext))

    def check_snake_case(self, filename: str) -> bool:
        """Check if filename follows snake_case convention."""
        name_without_ext = Path(filename).stem
        return bool(re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', name_without_ext))

    def is_alphanumeric_unicode(self, text: str) -> bool:
        """Check if text contains only alphanumeric characters including Unicode characters."""
        if self.allow_unicode:
            return bool(re.match(r'^[a-zA-Z0-9çğıöşüÇĞIİÖŞÜâêîôûÂÊÎÔÛ]+$', text, re.UNICODE))
        else:
            return bool(re.match(r'^[a-zA-Z0-9]+$', text))

    def has_special_characters(self, filename: str) -> bool:
        """Check if filename contains disallowed special characters."""
        if self.allow_unicode:
            # Allow alphanumeric (including Unicode), hyphens, underscores, and dots
            return not bool(re.match(r'^[a-zA-Z0-9çğıöşüÇĞIİÖŞÜâêîôûÂÊÎÔÛ._-]+$', filename, re.UNICODE))
        else:
            # Allow only English alphanumeric, hyphens, underscores, and dots
            return not bool(re.match(r'^[a-zA-Z0-9._-]+$', filename))

    def has_spaces(self, filename: str) -> bool:
        """Check if filename contains spaces."""
        return ' ' in filename

    def is_descriptive(self, filename: str) -> bool:
        """Check if filename is descriptive (not generic)."""
        name_without_ext = Path(filename).stem.lower()
        generic_names = {
            'doc', 'document', 'file', 'temp', 'tmp', 'test', 'example',
            'sample', 'data', 'info', 'item', 'thing', 'stuff', 'misc',
            'doc1', 'doc2', 'file1', 'file2', 'test1', 'test2'
        }
        return name_without_ext not in generic_names

    def check_file(self, filepath: str) -> List[str]:
        """Check a single file against naming conventions."""
        filename = os.path.basename(filepath)
        path_obj = Path(filepath)
        errors = []

        # Skip hidden files and directories
        if filename.startswith('.') and filename not in self.ALLOWED_UPPERCASE:
            return errors

        # Skip allowed uppercase files
        if filename in self.ALLOWED_UPPERCASE:
            return errors

        if self.config:
            return self.check_file_with_config(filepath, filename, path_obj)

        # Default checks
        return self.check_file_default(filepath, filename, path_obj)

    def check_file_with_config(self, filepath: str, filename: str, path_obj: Path) -> List[str]:
        """Check file using configuration rules."""
        errors = []
        name_without_ext = path_obj.stem
        file_ext = path_obj.suffix.lower()

        # Get file configuration section
        file_config = self.config.get('files', {})

        # Check spaces
        if not file_config.get('allow-spaces', False) and ' ' in filename:
            errors.append(f"{filepath}: Filename contains spaces")

        # Check capital letters
        if not file_config.get('use-capital', False) and any(c.isupper() for c in filename):
            errors.append(f"{filepath}: Filename should be lowercase")

        # Check length
        min_len = file_config.get('min-length', 1)
        max_len = file_config.get('max-length', 100)
        if len(name_without_ext) < min_len or len(name_without_ext) > max_len:
            errors.append(f"{filepath}: Filename length should be between {min_len} and {max_len}")

        # Check reject patterns
        for pattern in file_config.get('reject-patterns', []):
            if re.match(pattern, name_without_ext):
                errors.append(f"{filepath}: Filename matches rejected pattern: {pattern}")

        # File type specific checks
        if file_ext in self.PYTHON_FILES:
            py_config = file_config.get('python-files', {})
            if py_config.get('use-underscore', True) and not self.check_snake_case(filename):
                errors.append(f"{filepath}: Python files should use snake_case")
        elif file_ext in self.CONFIG_FILES:
            cfg_config = file_config.get('config-files', {})
            use_underscore = cfg_config.get('use-underscore', True)
            use_hyphen = cfg_config.get('use-hyphen', True)

            has_underscore = '_' in name_without_ext
            has_hyphen = '-' in name_without_ext

            if not use_underscore and has_underscore:
                errors.append(f"{filepath}: Underscores not allowed in config filename")
            if not use_hyphen and has_hyphen:
                errors.append(f"{filepath}: Hyphens not allowed in config filename")

            if use_hyphen and not use_underscore and not self.check_kebab_case(filename):
                errors.append(f"{filepath}: Config files should use kebab-case (use hyphens(-) in the filename)")
            elif use_underscore and not use_hyphen and not self.check_snake_case(filename):
                errors.append(f"{filepath}: Config files should use snake_case (use underscores(_) in the filename)")
        else:
            # General files
            use_hyphen = file_config.get('use-hyphen', True)
            use_underscore = file_config.get('use-underscore', False)

            has_underscore = '_' in name_without_ext
            has_hyphen = '-' in name_without_ext

            if not use_underscore and has_underscore:
                errors.append(f"{filepath}: Underscores not allowed in filename")
            if not use_hyphen and has_hyphen:
                errors.append(f"{filepath}: Hyphens not allowed in filename")

            if use_hyphen and not use_underscore and not self.check_kebab_case(filename):
                errors.append(f"{filepath}: Files should use kebab-case (use hyphens(-) in the filename)")
            elif use_underscore and not use_hyphen and not self.check_snake_case(filename):
                errors.append(f"{filepath}: Files should use snake_case (use underscores(_) in the filename)")

        return errors

    def check_file_default(self, filepath: str, filename: str, path_obj: Path) -> List[str]:
        """Default file checking logic."""
        errors = []
        file_ext = path_obj.suffix.lower()

        # Check for spaces
        if self.has_spaces(filename):
            errors.append(f"{filepath}: Filename contains spaces")

        # Check for special characters
        if self.has_special_characters(filename):
            errors.append(f"{filepath}: Filename contains disallowed special characters")

        # Check if descriptive
        if not self.is_descriptive(filename):
            errors.append(f"{filepath}: Filename is not descriptive enough")

        # Check naming convention based on file type
        if file_ext in self.PYTHON_FILES:
            if not self.check_snake_case(filename):
                errors.append(f"{filepath}: Python files should use snake_case (use underscores(_) between words, e.g., user_service.py)")
        elif file_ext in self.CONFIG_FILES:
            if not (self.check_snake_case(filename) or self.check_kebab_case(filename)):
                errors.append(f"{filepath}: Config files should use snake_case or kebab-case")
        else:
            if not self.check_kebab_case(filename):
                errors.append(f"{filepath}: Files should use kebab-case (use hyphens(-) between words, e.g., user-guide.md)")

        # Check if uppercase (except allowed files)
        if any(c.isupper() for c in filename) and filename not in self.ALLOWED_UPPERCASE:
            errors.append(f"{filepath}: Filename should be lowercase")

        return errors

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception:
            return {}

    def is_excluded(self, filepath: str) -> bool:
        """Check if file should be excluded based on patterns."""
        for pattern in self.exclude_patterns:
            if re.search(pattern, filepath):
                return True
        return False

    def check_files(self, filepaths: List[str]) -> int:
        """Check multiple files and return exit code."""
        all_errors = []

        for filepath in filepaths:
            if os.path.isfile(filepath) and not self.is_excluded(filepath):
                errors = self.check_file(filepath)
                all_errors.extend(errors)

        if all_errors:
            for error in all_errors:
                print(error, file=sys.stderr)
            return 1

        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Check file names against naming conventions')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes for naming issues')
    parser.add_argument('--exclude', action='append', help='Exclude files matching regex pattern')
    parser.add_argument('--config', help='Path to YAML configuration file')
    parser.add_argument('--allow-unicode', action='store_true', help='Allow non-English characters (Turkish, etc.)')

    args = parser.parse_args()

    if not args.filenames:
        print("No files to check", file=sys.stderr)
        return 0

    checker = FileNameChecker(exclude_patterns=args.exclude or [], config_file=args.config, allow_unicode=args.allow_unicode)
    return checker.check_files(args.filenames)


if __name__ == '__main__':
    sys.exit(main())
