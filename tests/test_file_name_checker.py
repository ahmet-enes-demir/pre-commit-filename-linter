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

    with tempfile.NamedTemporaryFile(suffix='/README.md', delete=False) as f:
        errors = checker.check_file(f.name)
        assert len(errors) == 0
        os.unlink(f.name)

    with tempfile.NamedTemporaryFile(suffix='/Dockerfile', delete=False) as f:
        errors = checker.check_file(f.name)
        assert len(errors) == 0
        os.unlink(f.name)


def test_python_files():
    """Test Python file naming."""
    checker = FileNameChecker()

    with tempfile.NamedTemporaryFile(suffix='/user_service.py', delete=False) as f:
        errors = checker.check_file(f.name)
        assert len(errors) == 0
        os.unlink(f.name)

    with tempfile.NamedTemporaryFile(suffix='/UserService.py', delete=False) as f:
        errors = checker.check_file(f.name)
        assert len(errors) > 0
        os.unlink(f.name)





if __name__ == '__main__':
    test_kebab_case()
    test_snake_case()
    test_special_characters()
    test_allowed_files()
    test_python_files()
    print("All file tests passed!")
