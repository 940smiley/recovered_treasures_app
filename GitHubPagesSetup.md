# GitHub Pages Setup

## Activate Pages
1. Open **Settings → Pages** in GitHub.
2. Select **Source**: `Deploy from a branch`.
3. Choose **Branch**: `main` and **Folder**: `/docs` (recommended) or `/` if mirroring `frontend/` directly.
4. Save to enable the site at `https://<org-or-user>.github.io/<repo>/`.

## Directory Guidance
- Mirror static artifacts into `/docs` for Pages consumption.
- Keep `manifest.json` and `service-worker.js` under `/docs` or rewrite paths in `index.html` accordingly.
- If you add a docs site, keep a landing `index.html` that links back to the PWA.

## Theme Configuration
- Enable GitHub's default Pages theme via `_config.yml` in `/docs` (e.g., `theme: minima`).
- Add navigation links for API docs and deployment runbooks.

## Custom Domain + DNS
- Create a `CNAME` file inside `/docs` with your domain (e.g., `pwa.example.com`).
- Point DNS `CNAME` record to `<user>.github.io`.
- Enforce HTTPS in Pages settings once DNS propagates.

## Recommended CI/CD Deploy Pipeline
- Use a GitHub Action to build or copy static assets into `/docs` on every push to `main`.
- Example workflow snippet:
```yaml
name: Deploy Docs
on:
  push:
    branches: [main]
    paths: ["frontend/**", "docs/**", "GitHubPagesSetup.md"]
jobs:
  deploy-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Prepare docs folder
        run: |
          mkdir -p docs
          cp -r frontend/* docs/
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs
      - name: Deploy to Pages
        uses: actions/deploy-pages@v4
```

The repo is now Pages-ready and only needs the workflow wired into GitHub.
