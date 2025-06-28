#!/usr/bin/env python3
"""Tests for empty file checker."""

import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from empty_file_checker import EmptyFileChecker


def test_empty_file_detection():
    """Test detection of empty files."""
    checker = EmptyFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create empty file
        empty_file = os.path.join(temp_dir, 'empty.txt')
        with open(empty_file, 'w') as f:
            pass

        errors = checker.check_file(empty_file)
        assert len(errors) > 0, f"Empty file should be flagged: {errors}"
        assert "File is empty" in errors[0], f"Error should mention empty file: {errors[0]}"


def test_non_empty_file():
    """Test that non-empty files pass."""
    checker = EmptyFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create non-empty file
        file_path = os.path.join(temp_dir, 'content.txt')
        with open(file_path, 'w') as f:
            f.write('test content')

        errors = checker.check_file(file_path)
        assert len(errors) == 0, f"Non-empty file should pass: {errors}"


def test_allowed_empty_files():
    """Test that certain files are allowed to be empty."""
    checker = EmptyFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test __init__.py
        init_file = os.path.join(temp_dir, '__init__.py')
        with open(init_file, 'w') as f:
            pass

        errors = checker.check_file(init_file)
        assert len(errors) == 0, f"__init__.py should be allowed to be empty: {errors}"


def test_allow_empty_flag():
    """Test allow_empty flag."""
    checker = EmptyFileChecker(allow_empty=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create empty file
        empty_file = os.path.join(temp_dir, 'empty.txt')
        with open(empty_file, 'w') as f:
            pass

        errors = checker.check_file(empty_file)
        assert len(errors) == 0, f"Empty file should pass with allow_empty=True: {errors}"


def test_config_file():
    """Test configuration file support."""
    config_content = "empty-files:\n  allow-empty: true"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = EmptyFileChecker(config_file=config_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            empty_file = os.path.join(temp_dir, 'empty.txt')
            with open(empty_file, 'w') as f:
                pass

            errors = checker.check_file(empty_file)
            assert len(errors) == 0, f"Empty file should pass with config allow-empty: true: {errors}"
    finally:
        os.unlink(config_file)


if __name__ == '__main__':
    test_empty_file_detection()
    test_non_empty_file()
    test_allowed_empty_files()
    test_allow_empty_flag()
    test_config_file()
    print("All empty file tests passed!")
