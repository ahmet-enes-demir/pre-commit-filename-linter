#!/usr/bin/env python3
"""Directory name checker for pre-commit hooks."""

import argparse
import os
import re
import sys
import yaml
from typing import List, Dict, Any


class DirectoryChecker:
    """Check directory names against naming conventions."""

    def __init__(self, exclude_patterns=None, config_file=None, allow_unicode=False):
        self.errors = []
        self.exclude_patterns = exclude_patterns or []
        self.allow_unicode = allow_unicode
        # Add default exclusions
        self.exclude_patterns.extend([r'\.git/', r'__pycache__', r'\.pytest_cache', r'node_modules'])
        self.config = self.load_config(config_file) if config_file else None
        if self.config and 'exclude-patterns' in self.config:
            self.exclude_patterns.extend(self.config['exclude-patterns'])
        # Override allow_unicode from config if specified
        if self.config and 'directories' in self.config:
            self.allow_unicode = self.config['directories'].get('allow-unicode', self.allow_unicode)

    def check_directory(self, dirpath: str) -> List[str]:
        """Check a directory name against naming conventions."""
        dirname = os.path.basename(dirpath)
        errors = []

        # Skip hidden directories and common directories
        if dirname.startswith('.') or dirname in {'__pycache__', 'node_modules', '.git', '.pytest_cache'}:
            return errors

        # Skip if excluded by patterns
        if self.is_excluded(dirpath):
            return errors

        if self.config:
            return self.check_directory_with_config(dirpath, dirname)

        # Default directory checks
        return self.check_directory_default(dirpath, dirname)

    def check_directory_with_config(self, dirpath: str, dirname: str) -> List[str]:
        """Check directory using configuration rules."""
        errors = []

        # Get directory configuration section
        dir_config = self.config.get('directories', {})

        # Check spaces
        if not dir_config.get('allow-spaces', False) and ' ' in dirname:
            errors.append(f"{dirpath}: Directory name contains spaces")

        # Check capital letters
        if not dir_config.get('use-capital', False) and any(c.isupper() for c in dirname):
            errors.append(f"{dirpath}: Directory name should be lowercase")

        # Check length
        min_len = dir_config.get('min-length', 1)
        max_len = dir_config.get('max-length', 100)
        if len(dirname) < min_len or len(dirname) > max_len:
            errors.append(f"{dirpath}: Directory name length should be between {min_len} and {max_len}")

        # Check reject patterns
        for pattern in dir_config.get('reject-patterns', []):
            if re.match(pattern, dirname):
                errors.append(f"{dirpath}: Directory name matches rejected pattern: {pattern}")

        # Check for Unicode characters when not allowed
        if not self.allow_unicode and not bool(re.match(r'^[a-zA-Z0-9._-]+$', dirname)):
            errors.append(f"{dirpath}: Directory name contains non-English characters (set allow-unicode: true to allow)")

        # General directory naming
        use_hyphen = dir_config.get('use-hyphen', True)
        use_underscore = dir_config.get('use-underscore', False)

        has_underscore = '_' in dirname
        has_hyphen = '-' in dirname

        if not use_underscore and has_underscore:
            errors.append(f"{dirpath}: Underscores not allowed in directory name (use hyphens(-) instead, e.g., user-service/)")
        if not use_hyphen and has_hyphen:
            errors.append(f"{dirpath}: Hyphens not allowed in directory name")

        return errors

    def check_directory_default(self, dirpath: str, dirname: str) -> List[str]:
        """Default directory checking logic."""
        errors = []

        # Check for spaces
        if ' ' in dirname:
            errors.append(f"{dirpath}: Directory name contains spaces")

        # Check for special characters
        if self.allow_unicode:
            if not bool(re.match(r'^[a-zA-Z0-9çğıöşüÇĞIİÖŞÜâêîôûÂÊÎÔÛ._-]+$', dirname, re.UNICODE)):
                errors.append(f"{dirpath}: Directory name contains disallowed special characters")
        else:
            if not bool(re.match(r'^[a-zA-Z0-9._-]+$', dirname)):
                errors.append(f"{dirpath}: Directory name contains non-English characters (set allow-unicode: true to allow)")

        # Check if descriptive
        if not self.is_descriptive_directory(dirname):
            errors.append(f"{dirpath}: Directory name is not descriptive enough")

        # Check kebab-case for directories
        if not self.check_kebab_case_directory(dirname):
            errors.append(f"{dirpath}: Directory should use kebab-case (use hyphens(-) between words, e.g., user-service/)")

        # Check if uppercase
        if any(c.isupper() for c in dirname):
            errors.append(f"{dirpath}: Directory name should be lowercase")

        return errors

    def check_kebab_case_directory(self, dirname: str) -> bool:
        """Check if directory name follows kebab-case convention."""
        # Reject if contains underscores
        if '_' in dirname:
            return False

        # Allow single words without hyphens
        if '-' not in dirname:
            return dirname.islower() and self.is_alphanumeric_unicode(dirname.replace('.', ''))

        # Check kebab-case pattern
        if self.allow_unicode:
            return bool(re.match(r'^[a-z0-9çğıöşüâêîôû]+(-[a-z0-9çğıöşüâêîôû]+)*$', dirname, re.UNICODE))
        else:
            return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', dirname))

    def is_alphanumeric_unicode(self, text: str) -> bool:
        """Check if text contains only alphanumeric characters including Unicode characters."""
        if self.allow_unicode:
            return bool(re.match(r'^[a-zA-Z0-9çğıöşüÇĞIİÖŞÜâêîôûÂÊÎÔÛ]+$', text, re.UNICODE))
        else:
            return bool(re.match(r'^[a-zA-Z0-9]+$', text))

    def is_descriptive_directory(self, dirname: str) -> bool:
        """Check if directory name is descriptive (not generic)."""
        generic_names = {
            'dir', 'directory', 'folder', 'temp', 'tmp', 'test', 'example',
            'sample', 'data', 'info', 'item', 'thing', 'stuff', 'misc',
            'dir1', 'dir2', 'folder1', 'folder2', 'test1', 'test2'
        }
        return dirname.lower() not in generic_names

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception:
            return {}

    def is_excluded(self, dirpath: str) -> bool:
        """Check if directory should be excluded based on patterns."""
        for pattern in self.exclude_patterns:
            if re.search(pattern, dirpath):
                return True
        return False

    def check_directories(self, dirpaths: List[str]) -> int:
        """Check multiple directories and return exit code."""
        all_errors = []

        for dirpath in dirpaths:
            if os.path.isdir(dirpath) and not self.is_excluded(dirpath):
                errors = self.check_directory(dirpath)
                all_errors.extend(errors)

        if all_errors:
            for error in all_errors:
                print(error, file=sys.stderr)
            return 1

        return 0


def find_directories(root_path='.', exclude_patterns=None):
    """Find all directories in the repository."""
    exclude_patterns = exclude_patterns or []
    directories = []

    for root, dirs, files in os.walk(root_path):
        # Filter out excluded directories from further traversal
        dirs[:] = [d for d in dirs if not any(re.search(pattern, os.path.join(root, d)) for pattern in exclude_patterns)]

        for dirname in dirs:
            dir_path = os.path.join(root, dirname)
            # Only add if not excluded by DirectoryChecker's exclusion logic
            if not dirname.startswith('.') and dirname not in {'__pycache__', 'node_modules', '.git', '.pytest_cache'}:
                directories.append(dir_path)

    return directories


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Check directory names against naming conventions')
    parser.add_argument('directories', nargs='*', help='Directory names to check')
    parser.add_argument('--exclude', action='append', help='Exclude directories matching regex pattern')
    parser.add_argument('--config', help='Path to YAML configuration file')
    parser.add_argument('--allow-unicode', action='store_true', help='Allow non-English characters (Turkish, etc.)')

    args = parser.parse_args()

    checker = DirectoryChecker(exclude_patterns=args.exclude or [], config_file=args.config, allow_unicode=args.allow_unicode)

    # If no directories specified, scan the current repository
    if not args.directories:
        directories = find_directories('.', args.exclude or [])
    else:
        directories = args.directories

    return checker.check_directories(directories)


if __name__ == '__main__':
    sys.exit(main())
