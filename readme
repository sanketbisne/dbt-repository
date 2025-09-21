# dbt CronJob on GKE

This project contains a dbt setup designed to be run as a scheduled CronJob on Google Kubernetes Engine (GKE). It uses GKE Workload Identity for secure, keyless authentication to Google BigQuery.

## Overview

The project is structured to be built into a self-contained Docker image and deployed via a Helm chart.

- **dbt**: Handles data transformations in BigQuery.
- **Docker**: Containerizes the dbt project and its dependencies.
- **Helm**: Manages the deployment of a Kubernetes `CronJob` and its associated resources.
- **Workload Identity**: Provides secure, passwordless authentication from the GKE pod to Google Cloud services.

## Prerequisites

- dbt CLI
- Docker
- gcloud CLI
- kubectl
- Helm

## Project Structure

```
├── Dockerfile          # Defines the container image for the dbt project.
├── helm/
│   └── dbt-cron/       # Helm chart for Kubernetes deployment.
├── models/             # dbt models (SQL transformations).
├── profile/
│   └── profiles.yml    # dbt profile, configured to use environment variables.
├── requirements.txt    # Python dependencies.
└── run_dbt.sh          # The entrypoint script for the container.
```

## Local Development

For local development, you will need to authenticate with Google Cloud and have a local `profiles.yml` file.

1.  **Authenticate with Google Cloud:**
    This command stores credentials on your local machine that dbt can use.
    ```bash
    gcloud auth application-default login
    ```

2.  **Set up Local Profile:**
    Your local `~/.dbt/profiles.yml` should point to your BigQuery project. The `method: oauth` will use the credentials from the previous step.

3.  **Install Dependencies and Run:**
    ```bash
    # Install dbt packages if any are defined in packages.yml
    dbt deps

    # Verify connection to BigQuery
    dbt debug

    # Run your dbt models
    dbt run
    ```

## Containerization (Docker)

The `Dockerfile` creates a self-contained image with your dbt project and its configuration.

1.  **Build the Docker Image:**
    Navigate to the project root directory to run the build command.

    ```bash
    # For x86/amd64 machines (most cloud VMs)
    docker build -t <IMAGE_NAME>:<TAG> .

    # IMPORTANT: For Apple Silicon (M1/M2/M3) Macs, build for the correct platform
    docker build --platform linux/amd64 -t <IMAGE_NAME>:<TAG> .
    ```

2.  **Push to Google Artifact Registry:**
    First, configure Docker to authenticate with GAR. Then, tag and push your image.

    ```bash
    # Replace <LOCATION> with your GAR region (e.g., europe-west2)
    gcloud auth configure-docker <LOCATION>-docker.pkg.dev

    # Tag the image
    docker tag <IMAGE_NAME>:<TAG> <LOCATION>-docker.pkg.dev/<GCP_PROJECT_ID>/<REPO_NAME>/<IMAGE_NAME>:<TAG>

    # Push the image
    docker push <LOCATION>-docker.pkg.dev/<GCP_PROJECT_ID>/<REPO_NAME>/<IMAGE_NAME>:<TAG>
    ```

## Deployment (Helm on GKE)

The Helm chart deploys a `CronJob` that runs your dbt container on a schedule.

### 1. Prerequisites for GKE

- A GKE cluster with Workload Identity enabled.
- A Google Service Account (GSA), e.g., `agg-dbt-sa@<PROJECT_ID>.iam.gserviceaccount.com`.
  - This GSA must have the necessary BigQuery roles (e.g., `BigQuery Job User`, `BigQuery Data Editor`).
- A Kubernetes Service Account (KSA) in your target namespace, e.g., `agg-dbt-sa`.
- An IAM policy binding that allows the KSA to impersonate the GSA.
  ```bash
  gcloud iam service-accounts add-iam-policy-binding <GSA_EMAIL> \
      --role="roles/iam.workloadIdentityUser" \
      --member="serviceAccount:<PROJECT_ID>.svc.id.goog[<K8S_NAMESPACE>/<KSA_NAME>]"
  ```

### 2. Configure the Helm Chart

Update `helm/dbt-cron/values.yaml` with your specific configuration:

- **`image.repository` and `image.tag`**: Point to the image you pushed to Artifact Registry.
- **`serviceAccount.annotations`**: Ensure the `iam.gke.io/gcp-service-account` value matches your GSA email.
- **`dbt.env`**: Set the `GCP_PROJECT_ID` and `GCP_BQ_DATASET_NAME` that your `profiles.yml` will use.

### 3. Deploy the Chart

Navigate to the chart directory and run the install command.

```bash
cd helm/dbt-cron

# Perform a dry run to validate the generated YAML
helm install <RELEASE_NAME> . --dry-run --debug -n <NAMESPACE>

# Install the chart
helm install <RELEASE_NAME> . -n <NAMESPACE>
```

## Managing the Deployment

- **Upgrade:** `helm upgrade <RELEASE_NAME> . -n <NAMESPACE>`
- **Check Status:** `helm list -n <NAMESPACE>`
- **Check Pod Logs:** `kubectl logs -f <POD_NAME> -n <NAMESPACE>`
- **Uninstall:** `helm uninstall <RELEASE_NAME> -n <NAMESPACE>`

---

## Deployment in Air-Gapped Environments

Deploying this project in a highly secure environment (e.g., private cluster, no internet) requires additional configuration.

### 1. Private Python Packages

If `pypi.org` is blocked, `pip` must be configured to use an internal repository like Nexus.

- Create a `pip.conf` file in the project root with the URL of your internal repository.
- The `Dockerfile` is already configured to copy this file to the correct location (`/etc/pip.conf`) in the image.

### 2. Google API Connectivity

For pods to reach Google APIs (BigQuery, IAM) without internet access, your GKE cluster's subnet must be configured with **Private Google Access**. This allows traffic to flow to Google services over Google's internal network. This is an infrastructure task for your cloud networking team.

### 3. Docker Image Distribution

The GKE cluster must be able to pull the Docker image from an internal container registry.

1.  **Push to Internal Registry:** After building the image, push it to your organization's private registry (e.g., Nexus, Harbor, or a private Artifact Registry).
2.  **Update Helm Values:** Modify the `image.repository` value in `helm/dbt-cron/values.yaml` to point to the image's location in the internal registry.

With these changes, the same dbt project can be securely and reliably deployed in environments with strict network controls.