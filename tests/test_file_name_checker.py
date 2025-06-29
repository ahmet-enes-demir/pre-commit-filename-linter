#!/usr/bin/env python3
"""Tests for file name checker."""

import tempfile
import os
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from file_name_checker import FileNameChecker


def test_kebab_case():
    """Test kebab-case validation."""
    checker = FileNameChecker()

    # Valid kebab-case
    assert checker.check_kebab_case('user-guide.md')
    assert checker.check_kebab_case('api-documentation.md')
    assert checker.check_kebab_case('simple.md')

    # Invalid kebab-case
    assert not checker.check_kebab_case('UserGuide.md')
    assert not checker.check_kebab_case('user_guide.md')
    assert not checker.check_kebab_case('user guide.md')


def test_snake_case():
    """Test snake_case validation."""
    checker = FileNameChecker()

    # Valid snake_case
    assert checker.check_snake_case('user_service.py')
    assert checker.check_snake_case('api_client.py')
    assert checker.check_snake_case('simple.py')

    # Invalid snake_case
    assert not checker.check_snake_case('UserService.py')
    assert not checker.check_snake_case('user-service.py')


def test_special_characters():
    """Test special character detection."""
    checker = FileNameChecker()

    assert checker.has_special_characters('file@name.md')
    assert checker.has_special_characters('file#name.md')
    assert checker.has_special_characters('file name.md')
    assert not checker.has_special_characters('file-name.md')
    assert not checker.has_special_characters('file_name.py')


def test_allowed_files():
    """Test that standard files are allowed."""
    checker = FileNameChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test README.md
        readme_path = os.path.join(temp_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write('test')
        errors = checker.check_file(readme_path)
        assert len(errors) == 0, f"README.md should be allowed: {errors}"

        # Test Dockerfile
        dockerfile_path = os.path.join(temp_dir, 'Dockerfile')
        with open(dockerfile_path, 'w') as f:
            f.write('test')
        errors = checker.check_file(dockerfile_path)
        assert len(errors) == 0, f"Dockerfile should be allowed: {errors}"


def test_python_files():
    """Test Python file naming."""
    checker = FileNameChecker()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test good Python file
        py_path = os.path.join(temp_dir, 'user_service.py')
        with open(py_path, 'w') as f:
            f.write('test')
        errors = checker.check_file(py_path)
        assert len(errors) == 0, f"user_service.py should pass: {errors}"

        # Test bad Python file
        bad_py_path = os.path.join(temp_dir, 'UserService.py')
        with open(bad_py_path, 'w') as f:
            f.write('test')
        errors = checker.check_file(bad_py_path)
        assert len(errors) > 0, f"UserService.py should fail: {errors}"


def test_pascal_case():
    """Test PascalCase validation."""
    checker = FileNameChecker()

    # Valid PascalCase
    assert checker.check_pascal_case('TestFile.md')
    assert checker.check_pascal_case('MyComponent.tsx')
    assert checker.check_pascal_case('UserService.java')

    # Invalid PascalCase
    assert not checker.check_pascal_case('testFile.md')  # starts with lowercase
    assert not checker.check_pascal_case('test_file.md')  # has underscore
    assert not checker.check_pascal_case('test-file.md')  # has hyphen


def test_camel_case():
    """Test camelCase validation."""
    checker = FileNameChecker()

    # Valid camelCase
    assert checker.check_camel_case('testFile.js')
    assert checker.check_camel_case('myComponent.tsx')
    assert checker.check_camel_case('configData.json')

    # Invalid camelCase
    assert not checker.check_camel_case('TestFile.js')  # starts with uppercase
    assert not checker.check_camel_case('test_file.js')  # has underscore
    assert not checker.check_camel_case('test-file.js')  # has hyphen


def test_screaming_snake_case():
    """Test SCREAMING_SNAKE_CASE validation."""
    checker = FileNameChecker()

    # Valid SCREAMING_SNAKE_CASE
    assert checker.check_screaming_snake_case('API_CONFIG.txt')
    assert checker.check_screaming_snake_case('MAX_RETRY_COUNT.env')
    assert checker.check_screaming_snake_case('DATABASE_URL.conf')

    # Invalid SCREAMING_SNAKE_CASE
    assert not checker.check_screaming_snake_case('api_config.txt')  # lowercase
    assert not checker.check_screaming_snake_case('API-CONFIG.txt')  # has hyphen
    assert not checker.check_screaming_snake_case('ApiConfig.txt')  # mixed case


def test_pascal_case_with_config():
    """Test PascalCase with configuration."""
    config_content = """files:
  use-hyphen: false
  use-pascal-case: true
  use-capital: true"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = FileNameChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test PascalCase file should pass
            pascal_path = os.path.join(temp_dir, 'TestFile.md')
            with open(pascal_path, 'w') as f:
                f.write('test')
            errors = checker.check_file(pascal_path)
            assert len(errors) == 0, f"PascalCase should pass: {errors}"
    finally:
        os.unlink(config_file)


def test_camel_case_with_config():
    """Test camelCase with configuration."""
    config_content = """files:
  use-hyphen: false
  use-camel-case: true
  use-capital: true"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = FileNameChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test camelCase file should pass
            camel_path = os.path.join(temp_dir, 'testFile.js')
            with open(camel_path, 'w') as f:
                f.write('test')
            errors = checker.check_file(camel_path)
            assert len(errors) == 0, f"camelCase should pass: {errors}"
    finally:
        os.unlink(config_file)


def test_screaming_snake_case_with_config():
    """Test SCREAMING_SNAKE_CASE with configuration."""
    config_content = """files:
  use-hyphen: false
  use-screaming-snake-case: true
  use-capital: true"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker = FileNameChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test SCREAMING_SNAKE_CASE file should pass
            screaming_path = os.path.join(temp_dir, 'API_CONFIG.txt')
            with open(screaming_path, 'w') as f:
                f.write('test')
            errors = checker.check_file(screaming_path)
            assert len(errors) == 0, f"SCREAMING_SNAKE_CASE should pass: {errors}"
    finally:
        os.unlink(config_file)


def test_file_unicode_support():
    """Test Unicode character support in file names."""
    # Test without Unicode support (default)
    checker = FileNameChecker()
    with tempfile.TemporaryDirectory() as temp_dir:
        turkish_path = os.path.join(temp_dir, 'internet-değişimi.md')
        with open(turkish_path, 'w') as f:
            f.write('test')
        errors = checker.check_file(turkish_path)
        assert len(errors) > 0, f"Turkish filename should fail without Unicode support: {errors}"
        assert "special characters" in errors[0], f"Error should mention special characters: {errors[0]}"

    # Test with Unicode support enabled via argument
    checker_unicode = FileNameChecker(allow_unicode=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        turkish_path = os.path.join(temp_dir, 'internet-değişimi.md')
        with open(turkish_path, 'w') as f:
            f.write('test')
        errors = checker_unicode.check_file(turkish_path)
        assert len(errors) == 0, f"Turkish filename should pass with Unicode support: {errors}"

    # Test with Unicode support enabled via config
    config_content = "files:\n  allow-unicode: true"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_file = f.name

    try:
        checker_config = FileNameChecker(config_file=config_file)
        with tempfile.TemporaryDirectory() as temp_dir:
            turkish_path = os.path.join(temp_dir, 'internet-değişimi.md')
            with open(turkish_path, 'w') as f:
                f.write('test')
            errors = checker_config.check_file(turkish_path)
            assert len(errors) == 0, f"Turkish filename should pass with config Unicode support: {errors}"
    finally:
        os.unlink(config_file)


if __name__ == '__main__':
    test_kebab_case()
    test_snake_case()
    test_special_characters()
    test_allowed_files()
    test_python_files()
    test_pascal_case()
    test_camel_case()
    test_screaming_snake_case()
    test_pascal_case_with_config()
    test_camel_case_with_config()
    test_screaming_snake_case_with_config()
    test_file_unicode_support()
    print("All file tests passed!")
