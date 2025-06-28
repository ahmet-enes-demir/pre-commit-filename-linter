#!/usr/bin/env python3
"""Tests for directory name checker."""

import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from directory_checker import DirectoryChecker


def test_kebab_case_directory():
    """Test kebab-case validation for directories."""
    checker = DirectoryChecker()

    # Valid kebab-case
    assert checker.check_kebab_case_directory('user-service')
    assert checker.check_kebab_case_directory('api-docs')
    assert checker.check_kebab_case_directory('simple')

    # Invalid kebab-case
    assert not checker.check_kebab_case_directory('UserService')
    assert not checker.check_kebab_case_directory('user_service')
    assert not checker.check_kebab_case_directory('user service')


def test_descriptive_directory():
    """Test descriptive directory name validation."""
    checker = DirectoryChecker()

    # Descriptive names
    assert checker.is_descriptive_directory('user-service')
    assert checker.is_descriptive_directory('api-documentation')
    assert checker.is_descriptive_directory('authentication')

    # Non-descriptive names
    assert not checker.is_descriptive_directory('dir1')
    assert not checker.is_descriptive_directory('folder')
    assert not checker.is_descriptive_directory('temp')


def test_directory_naming():
    """Test directory naming conventions."""
    checker = DirectoryChecker()

    # Test good directory names
    with tempfile.TemporaryDirectory() as temp_dir:
        good_dirs = ['user-service', 'api-docs', 'test-data', 'src']
        for dirname in good_dirs:
            dir_path = os.path.join(temp_dir, dirname)
            os.makedirs(dir_path)
            errors = checker.check_directory(dir_path)
            assert len(errors) == 0, f"Good directory name '{dirname}' should not have errors: {errors}"

    # Test bad directory names
    with tempfile.TemporaryDirectory() as temp_dir:
        bad_dirs = ['UserService', 'user_service', 'dir1', 'my folder']
        for dirname in bad_dirs:
            dir_path = os.path.join(temp_dir, dirname)
            os.makedirs(dir_path)
            errors = checker.check_directory(dir_path)
            assert len(errors) > 0, f"Bad directory name '{dirname}' should have errors"


def test_directory_with_config():
    """Test directory naming with configuration."""
    # Create config that disallows underscores
    config_content = "directories:\n  use-underscore: false\n  use-hyphen: true"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = DirectoryChecker(config_file=config_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Test directory with underscore (should fail)
            dir_path = os.path.join(temp_dir, 'user_service')
            os.makedirs(dir_path)
            errors = checker.check_directory(dir_path)
            assert len(errors) > 0, f"Directory with underscore should fail when config disallows it: {errors}"

            # Test directory with hyphen (should pass)
            dir_path2 = os.path.join(temp_dir, 'user-service')
            os.makedirs(dir_path2)
            errors2 = checker.check_directory(dir_path2)
            assert len(errors2) == 0, f"Directory with hyphen should pass when config allows it: {errors2}"
    finally:
        os.unlink(config_file)


def test_excluded_directories():
    """Test that certain directories are excluded from checking."""
    checker = DirectoryChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        excluded_dirs = ['.git', '__pycache__', 'node_modules', '.pytest_cache']
        for dirname in excluded_dirs:
            dir_path = os.path.join(temp_dir, dirname)
            os.makedirs(dir_path)
            errors = checker.check_directory(dir_path)
            assert len(errors) == 0, f"Excluded directory '{dirname}' should not have errors"


if __name__ == '__main__':
    test_kebab_case_directory()
    test_descriptive_directory()
    test_directory_naming()
    test_directory_with_config()
    test_excluded_directories()
    print("All directory tests passed!")
