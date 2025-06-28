#!/usr/bin/env python3
"""Tests for duplicate file checker."""

import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duplicate_file_checker import DuplicateFileChecker


def test_duplicate_detection():
    """Test detection of duplicate files."""
    checker = DuplicateFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create two identical files
        file1 = os.path.join(temp_dir, 'file1.txt')
        file2 = os.path.join(temp_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('identical content')
        with open(file2, 'w') as f:
            f.write('identical content')

        exit_code = checker.check_files([file1, file2])
        assert exit_code == 1, "Duplicate files should return exit code 1"


def test_unique_files():
    """Test that unique files pass."""
    checker = DuplicateFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create two different files
        file1 = os.path.join(temp_dir, 'file1.txt')
        file2 = os.path.join(temp_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('content one')
        with open(file2, 'w') as f:
            f.write('content two')

        exit_code = checker.check_files([file1, file2])
        assert exit_code == 0, "Unique files should return exit code 0"


def test_single_file():
    """Test that single file always passes."""
    checker = DuplicateFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, 'file1.txt')
        with open(file1, 'w') as f:
            f.write('content')

        exit_code = checker.check_files([file1])
        assert exit_code == 0, "Single file should always pass"


def test_allow_duplicates_flag():
    """Test allow_duplicates flag."""
    checker = DuplicateFileChecker(allow_duplicates=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create two identical files
        file1 = os.path.join(temp_dir, 'file1.txt')
        file2 = os.path.join(temp_dir, 'file2.txt')

        with open(file1, 'w') as f:
            f.write('identical content')
        with open(file2, 'w') as f:
            f.write('identical content')

        exit_code = checker.check_files([file1, file2])
        assert exit_code == 0, "Duplicates should pass with allow_duplicates=True"


def test_config_file():
    """Test configuration file support."""
    config_content = "duplicate-files:\n  allow-duplicates: true"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = DuplicateFileChecker(config_file=config_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            file1 = os.path.join(temp_dir, 'file1.txt')
            file2 = os.path.join(temp_dir, 'file2.txt')

            with open(file1, 'w') as f:
                f.write('identical content')
            with open(file2, 'w') as f:
                f.write('identical content')

            exit_code = checker.check_files([file1, file2])
            assert exit_code == 0, "Duplicates should pass with config allow-duplicates: true"
    finally:
        os.unlink(config_file)


def test_file_hash():
    """Test file hashing functionality."""
    checker = DuplicateFileChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, 'file1.txt')
        file2 = os.path.join(temp_dir, 'file2.txt')

        # Same content should have same hash
        with open(file1, 'w') as f:
            f.write('test content')
        with open(file2, 'w') as f:
            f.write('test content')

        hash1 = checker.get_file_hash(file1)
        hash2 = checker.get_file_hash(file2)
        assert hash1 == hash2, "Identical files should have same hash"

        # Different content should have different hash
        with open(file2, 'w') as f:
            f.write('different content')

        hash2_new = checker.get_file_hash(file2)
        assert hash1 != hash2_new, "Different files should have different hash"


if __name__ == '__main__':
    test_duplicate_detection()
    test_unique_files()
    test_single_file()
    test_allow_duplicates_flag()
    test_config_file()
    test_file_hash()
    print("All duplicate file tests passed!")
