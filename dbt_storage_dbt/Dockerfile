# Use a specific Python version for reproducibility. This creates a smaller image.
FROM python:3.12-slim

# Create a non-root user and group for security best practices
# No home directory is needed as we will use a relative path for profiles.
RUN groupadd -r dbt && useradd --no-log-init -r -g dbt dbt_user

# Install git and clean up apt cache to keep image small
# Running as root before switching to the non-root user
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/app/dbt

# Copy only the requirements file to leverage Docker layer caching
COPY --chown=dbt_user:dbt requirements.txt .

# Install dependencies. This layer is cached as long as requirements.txt doesn't change.
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project files
COPY --chown=dbt_user:dbt . .

# Make the script executable
RUN chmod +x run_dbt.sh

# Switch to the non-root user
USER dbt_user

ENV DBT_PROFILES_DIR=profile

# This is the default command that will run when the container starts.
CMD ["./run_dbt.sh"]