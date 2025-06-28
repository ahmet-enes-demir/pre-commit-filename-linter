from setuptools import setup

setup(
    name='pre-commit-filename-linter',
    version='1.0.0',
    description='Pre-commit filename linter for checking file naming conventions',
    author='Ahmet Demir',
    packages=['src'],
    package_dir={'src': 'src'},
    entry_points={
        'console_scripts': [
            'filename-linter=src.file_name_checker:main',
        ],
    },
    python_requires='>=3.6',
)
