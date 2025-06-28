from setuptools import setup

setup(
    name='pre-commit-filename-linter',
    version='1.0.0',
    description='Pre-commit filename linter for checking file and directory naming conventions',
    author='Ahmet Demir',
    url='https://github.com/ahmet-enes-demir/pre-commit-filename-linter',
    packages=['src'],
    package_dir={'src': 'src'},
    entry_points={
        'console_scripts': [
            'filename-linter=src.file_name_checker:main',
            'directory-linter=src.directory_checker:main',
            'empty-file-linter=src.empty_file_checker:main',
            'duplicate-file-linter=src.duplicate_file_checker:main',
        ],
    },
    install_requires=[
        'pyyaml',
    ],
    python_requires='>=3.6',
)
