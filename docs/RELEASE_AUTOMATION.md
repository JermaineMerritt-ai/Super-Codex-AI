# Release Automation & CI/CD

## Automated Release Workflow

- When you push a tag matching `v*` (e.g., `v1.0.0`), GitHub Actions will:
  - Run all tests (Python and Node.js)
  - Generate release notes automatically
  - Create a GitHub Release for the tag
  - (Optional) Upload release assets or trigger deployment steps

## How to Use

1. Tag your release:
   ```
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
2. The workflow in `.github/workflows/release-on-tag.yml` will run automatically.
3. Check the Releases page on GitHub for release notes and assets.

## Customization
- Edit `.github/workflows/release-on-tag.yml` to add deployment, asset upload, or notification steps.
- Use `RELEASE_NOTES_TEMPLATE.md` for manual notes if needed.

---

## Dashboard Integration
- The dashboard can display the latest release version and link to release notes.
- To automate, fetch the latest tag and release info from the GitHub API and show it in a dashboard widget.
- Example API endpoint: `https://api.github.com/repos/JermaineMerritt-ai/Jermaine-ai-assistance/releases/latest`
