FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY setup.py .

RUN pip3 install -e .

# Create wrapper scripts for each checker
RUN echo -e '#!/bin/sh\npython3 /app/src/file_name_checker.py "$@"' > /usr/local/bin/check-file-names && chmod +x /usr/local/bin/check-file-names
RUN echo -e '#!/bin/sh\npython3 /app/src/directory_checker.py "$@"' > /usr/local/bin/check-directory-names && chmod +x /usr/local/bin/check-directory-names
RUN echo -e '#!/bin/sh\npython3 /app/src/empty_file_checker.py "$@"' > /usr/local/bin/check-empty-files && chmod +x /usr/local/bin/check-empty-files
RUN echo -e '#!/bin/sh\npython3 /app/src/duplicate_file_checker.py "$@"' > /usr/local/bin/check-duplicate-files && chmod +x /usr/local/bin/check-duplicate-files
