# FastAPI DevOps API - Application & CI/CD Repository

## Overview

This repository houses the source code, container configuration, and automated CI/CD pipeline for the **FastAPI DevOps Tools application**. It is designed to work hand-in-hand with the infrastructure and GitOps deployment stack, automatically packaging application updates and propagating new image tags to the Kubernetes deployment manifests.

---

## Directory Structure

```text
├── .github
│   └── workflows
│       └── code-change-pipeline.yml
├
│── Dockerfile
│── main.py
│── requirements.txt
├── .gitignore
└── README.md

```

---

## Application Components

* **FastAPI (`app/main.py`)**: A lightweight, high-performance Python application providing DevOps utility endpoints.
* **Dependencies (`app/requirements.txt`)**: Manages core libraries, primarily `fastapi` and `uvicorn`.
* **Containerisation (`app/Dockerfile`)**: Multi-stage or optimized single-stage build containerizing the Python runtime, installing dependencies, and running under a secure, non-root user profile.

---

## CI/CD Pipeline (`code-change-pipeline.yml`)

The automated pipeline handles continuous integration and continuous delivery for code changes:

1. **Trigger**: Activated automatically on every push to the `main` branch affecting files within the `/app` folder.
2. **Vulnerability Scanning**: Runs **Trivy** to scan the built Docker image for vulnerabilities before pushing to production registries.
3. **Build & Tag**: Builds the Docker image using the unique **Git commit SHA** as the container image tag to ensure strict traceability.
4. **Registry Push**: Authenticates with AWS and pushes the newly tagged image to **Amazon ECR**.
5. **Manifest Update**: Automatically modifies the `k8s/deployment.yml` manifest file (or syncs with the infrastructure repository) to reference the new image tag.
6. **GitOps Synchronization**: Commits the updated manifest back to the repository, where **ArgoCD** instantly detects the change and rolls out the update to the AWS EKS cluster with zero downtime.

---

## Security Best Practices

* **Non-Root Container Execution**: The application runs under a restricted, non-privileged user inside the container to minimize security exposure.
* **Vulnerability Scanning**: Automated Trivy scans block container images containing critical or high vulnerabilities from being deployed.
* **OIDC Authentication**: GitHub Actions leverages OpenID Connect (OIDC) to securely assume AWS IAM roles without requiring long-lived access keys or static credentials.

---

## Local Development & Testing

### Prerequisites

* Python 3.10+ installed locally
* Docker installed

### Run Locally

1. Navigate to the app directory:
```bash
cd app

```


2. Install dependencies:
```bash
pip install -r requirements.txt

```


3. Run the application locally with Uvicorn:
```bash
uvicorn main:app --reload --port 8080

```


4. Access the API locally at:
```text
http://localhost:8080/docs

```



### Build & Run Docker Container Locally

```bash
docker build -t devops-api:local ./app
docker run -p 8080:8080 devops-api:local

```

---

## What I Learnt

* **Immutable Tagging with Commit SHAs**: Tying container tags directly to Git commit SHAs provides clear traceability, making rollback procedures and version auditing effortless.
* **GitOps Feedback Loops**: Automating the hand-off from code build pipelines to manifest updates creates a seamless developer experience where pushing code automatically drives cluster-state updates through ArgoCD.

---

## Future Improvements

* Implement automated unit and integration tests (pytest) within the GitHub Actions pipeline prior to building images.
* Add semantic versioning tagging alongside commit SHA tags for release management.
* Implement dynamic environment preview deployments for Pull Requests.
