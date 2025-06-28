FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY setup.py .

RUN pip3 install -e .

# Create wrapper scripts for each checker
RUN echo '#!/bin/sh\npython3 src/file_name_checker.py "$@"' > /usr/local/bin/filename-linter && chmod +x /usr/local/bin/filename-linter
RUN echo '#!/bin/sh\npython3 src/directory_checker.py "$@"' > /usr/local/bin/directory-linter && chmod +x /usr/local/bin/directory-linter
RUN echo '#!/bin/sh\npython3 src/empty_file_checker.py "$@"' > /usr/local/bin/empty-file-linter && chmod +x /usr/local/bin/empty-file-linter
RUN echo '#!/bin/sh\npython3 src/duplicate_file_checker.py "$@"' > /usr/local/bin/duplicate-file-linter && chmod +x /usr/local/bin/duplicate-file-linter
