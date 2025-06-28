#!/usr/bin/env python3
"""Duplicate file checker for pre-commit hooks."""
# Version 1.0.0

import argparse
import hashlib
import os
import re
import sys
import yaml
from typing import List, Dict, Any, Set


class DuplicateFileChecker:
    """Check for duplicate files with identical content."""

    def __init__(self, exclude_patterns=None, config_file=None, allow_duplicates=False):
        self.exclude_patterns = exclude_patterns or []
        self.allow_duplicates = allow_duplicates
        # Add default exclusions
        self.exclude_patterns.extend([r'\.git/', r'__pycache__', r'\.pytest_cache', r'node_modules'])
        self.config = self.load_config(config_file) if config_file else None
        if self.config and 'exclude-patterns' in self.config:
            self.exclude_patterns.extend(self.config['exclude-patterns'])
        # Override allow_duplicates from config if specified
        if self.config and 'duplicate-files' in self.config:
            self.allow_duplicates = self.config['duplicate-files'].get('allow-duplicates', self.allow_duplicates)

    def get_file_hash(self, filepath: str) -> str:
        """Get MD5 hash of file content."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""

    def check_files(self, filepaths: List[str]) -> int:
        """Check for duplicate files and return exit code."""
        if self.allow_duplicates:
            return 0

        hash_to_files = {}
        all_errors = []

        # Build hash map
        for filepath in filepaths:
            if not os.path.isfile(filepath) or self.is_excluded(filepath):
                continue

            file_hash = self.get_file_hash(filepath)
            if file_hash:
                if file_hash not in hash_to_files:
                    hash_to_files[file_hash] = []
                hash_to_files[file_hash].append(filepath)

        # Find duplicates
        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                files.sort()  # Sort for consistent output
                for i, filepath in enumerate(files):
                    if i == 0:
                        all_errors.append(f"{filepath}: Duplicate file found (original)")
                    else:
                        all_errors.append(f"{filepath}: Duplicate of {files[0]}")

        if all_errors:
            for error in all_errors:
                print(error, file=sys.stderr)
            return 1

        return 0

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
    parser = argparse.ArgumentParser(description='Check for duplicate files')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument('--exclude', action='append', help='Exclude files matching regex pattern')
    parser.add_argument('--config', help='Path to YAML configuration file')
    parser.add_argument('--allow-duplicates', action='store_true', help='Allow duplicate files')

    args = parser.parse_args()

    checker = DuplicateFileChecker(exclude_patterns=args.exclude or [], config_file=args.config, allow_duplicates=args.allow_duplicates)

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
