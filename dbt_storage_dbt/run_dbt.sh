#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# First, run dbt debug to verify the connection and project setup.
# This is a good practice before running models.
echo "--- Running dbt debug ---"
dbt debug

dbt run

dbt test





