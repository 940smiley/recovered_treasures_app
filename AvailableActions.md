# Available GitHub Actions Inventory

## CI / CD
- **Python API checks**
  - Lint & test FastAPI backend.
  - Sample:
    ```yaml
    name: Backend CI
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: '3.11'
          - run: pip install -r backend/requirements.txt
          - run: pytest
    ```
- **Docker build**
  - Validate container builds for deployment.
  - Sample:
    ```yaml
    name: Build Container
    on: [push]
    jobs:
      docker:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: docker/setup-buildx-action@v3
          - run: docker build -t seller-dashboard .
    ```

## Linting & Formatting
- **Python lint (ruff/flake8)**: ensure style consistency.
- **YAML lint**: catch config mistakes.
- Example snippet:
  ```yaml
  - name: Run Ruff
    run: pip install ruff && ruff check backend
  ```

## Security & Dependency Health
- **Dependabot**: automated dependency PRs.
- **pip-audit / safety**: scan Python dependencies.
- Example snippet:
  ```yaml
  - name: Dependency Audit
    run: pip install pip-audit && pip-audit -r backend/requirements.txt
  ```

## Deployment
- **GitHub Pages**: publish `/docs` or `frontend/` via `actions/deploy-pages@v4`.
- **Release tagging**: automate semantic version tags after successful pipelines.

## Trigger Examples
- `on: push` for quick feedback on main.
- `on: pull_request` for gated reviews.
- `on: workflow_dispatch` for manual deploys or hotfix checks.
