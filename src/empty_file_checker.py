#!/usr/bin/env python3
"""Empty file checker for pre-commit hooks."""

import argparse
import os
import re
import sys
import yaml
from typing import List, Dict, Any


class EmptyFileChecker:
    """Check for empty files that shouldn't be committed."""

    def __init__(self, exclude_patterns=None, config_file=None, allow_empty=False):
        self.exclude_patterns = exclude_patterns or []
        self.allow_empty = allow_empty
        # Add default exclusions
        self.exclude_patterns.extend([r'\.git/', r'__pycache__', r'\.pytest_cache', r'node_modules'])
        self.config = self.load_config(config_file) if config_file else None
        if self.config and 'exclude-patterns' in self.config:
            self.exclude_patterns.extend(self.config['exclude-patterns'])
        # Override allow_empty from config if specified
        if self.config and 'empty-files' in self.config:
            self.allow_empty = self.config['empty-files'].get('allow-empty', self.allow_empty)

    def check_file(self, filepath: str) -> List[str]:
        """Check if file is empty."""
        errors = []

        if not os.path.isfile(filepath) or self.is_excluded(filepath):
            return errors

        # Check if file is empty
        if os.path.getsize(filepath) == 0:
            # Some files are allowed to be empty
            filename = os.path.basename(filepath)
            if self.is_allowed_empty(filename):
                return errors

            if not self.allow_empty:
                errors.append(f"{filepath}: File is empty (use --allow-empty to allow)")

        return errors

    def is_allowed_empty(self, filename: str) -> bool:
        """Check if file is allowed to be empty."""
        allowed_empty = {
            '__init__.py', '.gitkeep', '.gitignore', '.env.example',
            'requirements.txt', 'CHANGELOG.md', 'TODO.md'
        }
        return filename in allowed_empty

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
            errors = self.check_file(filepath)
            all_errors.extend(errors)

        if all_errors:
            for error in all_errors:
                print(error, file=sys.stderr)
            return 1

        return 0


def find_all_files(root_path='.', exclude_patterns=None):
    """Find all files in the repository."""
    exclude_patterns = exclude_patterns or []
    files = []

    for root, dirs, filenames in os.walk(root_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(re.search(pattern, os.path.join(root, d)) for pattern in exclude_patterns)]

        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not any(re.search(pattern, file_path) for pattern in exclude_patterns):
                files.append(file_path)

    return files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Check for empty files')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument('--exclude', action='append', help='Exclude files matching regex pattern')
    parser.add_argument('--config', help='Path to YAML configuration file')
    parser.add_argument('--allow-empty', action='store_true', help='Allow empty files')

    args = parser.parse_args()

    checker = EmptyFileChecker(exclude_patterns=args.exclude or [], config_file=args.config, allow_empty=args.allow_empty)

    # If no files specified, scan the current repository
    if not args.filenames:
        files = find_all_files('.', checker.exclude_patterns)
    else:
        files = args.filenames

    if not files:
        return 0

    return checker.check_files(files)


if __name__ == '__main__':
    sys.exit(main())
