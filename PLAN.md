# Academic homepage roadmap

## Current direction

The site is a static academic profile built with Astro and hosted entirely on GitHub Pages. The design prioritizes readable research content, fast loading, and simple maintenance over decorative interaction.

## Content still to add

- Professional portrait
- Canonical paper and project-page links
- Downloadable CV
- Preferred public contact address
- Images, demos, or videos for selected research projects

Keep private drafts and source documents in `_source/`; that directory is ignored by Git and is never included in the deployed site.

## Deployment

Pushes to `main` trigger the GitHub Actions workflow in `.github/workflows/deploy.yml`. The workflow installs dependencies, builds the Astro project, and publishes `dist/` to GitHub Pages.
