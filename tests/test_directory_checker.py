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


def test_pascal_case_directory():
    """Test PascalCase validation for directories."""
    checker = DirectoryChecker()

    # Valid PascalCase
    assert checker.check_pascal_case_directory('TestDir')
    assert checker.check_pascal_case_directory('MyComponent')
    assert checker.check_pascal_case_directory('UserService')

    # Invalid PascalCase
    assert not checker.check_pascal_case_directory('testDir')  # starts with lowercase
    assert not checker.check_pascal_case_directory('test_dir')  # has underscore
    assert not checker.check_pascal_case_directory('test-dir')  # has hyphen


def test_camel_case_directory():
    """Test camelCase validation for directories."""
    checker = DirectoryChecker()

    # Valid camelCase
    assert checker.check_camel_case_directory('testDir')
    assert checker.check_camel_case_directory('myComponent')
    assert checker.check_camel_case_directory('configData')

    # Invalid camelCase
    assert not checker.check_camel_case_directory('TestDir')  # starts with uppercase
    assert not checker.check_camel_case_directory('test_dir')  # has underscore
    assert not checker.check_camel_case_directory('test-dir')  # has hyphen


def test_screaming_snake_case_directory():
    """Test SCREAMING_SNAKE_CASE validation for directories."""
    checker = DirectoryChecker()

    # Valid SCREAMING_SNAKE_CASE
    assert checker.check_screaming_snake_case_directory('API_CONFIG')
    assert checker.check_screaming_snake_case_directory('MAX_RETRY_COUNT')
    assert checker.check_screaming_snake_case_directory('DATABASE_URL')

    # Invalid SCREAMING_SNAKE_CASE
    assert not checker.check_screaming_snake_case_directory('api_config')  # lowercase
    assert not checker.check_screaming_snake_case_directory('API-CONFIG')  # has hyphen
    assert not checker.check_screaming_snake_case_directory('ApiConfig')  # mixed case


def test_pascal_case_directory_with_config():
    """Test PascalCase directories with configuration."""
    config_content = """directories:
  use-hyphen: false
  use-pascal-case: true
  use-capital: true"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = DirectoryChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test PascalCase directory should pass
            pascal_dir = os.path.join(temp_dir, 'TestDir')
            os.makedirs(pascal_dir)
            errors = checker.check_directory(pascal_dir)
            assert len(errors) == 0, f"PascalCase directory should pass: {errors}"
    finally:
        os.unlink(config_file)


def test_camel_case_directory_with_config():
    """Test camelCase directories with configuration."""
    config_content = """directories:
  use-hyphen: false
  use-camel-case: true
  use-capital: true"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = DirectoryChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test camelCase directory should pass
            camel_dir = os.path.join(temp_dir, 'testDir')
            os.makedirs(camel_dir)
            errors = checker.check_directory(camel_dir)
            assert len(errors) == 0, f"camelCase directory should pass: {errors}"
    finally:
        os.unlink(config_file)


def test_screaming_snake_case_directory_with_config():
    """Test SCREAMING_SNAKE_CASE directories with configuration."""
    config_content = """directories:
  use-hyphen: false
  use-screaming-snake-case: true
  use-capital: true"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = DirectoryChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test SCREAMING_SNAKE_CASE directory should pass
            screaming_dir = os.path.join(temp_dir, 'API_CONFIG')
            os.makedirs(screaming_dir)
            errors = checker.check_directory(screaming_dir)
            assert len(errors) == 0, f"SCREAMING_SNAKE_CASE directory should pass: {errors}"
    finally:
        os.unlink(config_file)


def test_directory_unicode_support():
    """Test Unicode character support in directory names."""
    # Test without Unicode support (default)
    checker = DirectoryChecker()
    with tempfile.TemporaryDirectory() as temp_dir:
        # Turkish directory name should fail by default
        dir_path = os.path.join(temp_dir, 'çayır')
        os.makedirs(dir_path)
        errors = checker.check_directory(dir_path)
        assert len(errors) > 0, f"Turkish directory should fail without Unicode support: {errors}"
        assert "non-English characters" in errors[0], f"Error should mention non-English characters: {errors[0]}"

    # Test with Unicode support enabled via argument
    checker_unicode = DirectoryChecker(allow_unicode=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        # Turkish directory name should pass with Unicode support
        dir_path = os.path.join(temp_dir, 'çayır')
        os.makedirs(dir_path)
        errors = checker_unicode.check_directory(dir_path)
        assert len(errors) == 0, f"Turkish directory should pass with Unicode support: {errors}"

    # Test with Unicode support enabled via config
    config_content = "directories:\n  allow-unicode: true"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker_config = DirectoryChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Turkish directory name should pass with config Unicode support
            dir_path = os.path.join(temp_dir, 'çayır')
            os.makedirs(dir_path)
            errors = checker_config.check_directory(dir_path)
            assert len(errors) == 0, f"Turkish directory should pass with config Unicode support: {errors}"
    finally:
        os.unlink(config_file)


if __name__ == '__main__':
    test_kebab_case_directory()
    test_descriptive_directory()
    test_directory_naming()
    test_directory_with_config()
    test_excluded_directories()
    test_pascal_case_directory()
    test_camel_case_directory()
    test_screaming_snake_case_directory()
    test_pascal_case_directory_with_config()
    test_camel_case_directory_with_config()
    test_screaming_snake_case_directory_with_config()
    test_directory_unicode_support()
    print("All directory tests passed!")
