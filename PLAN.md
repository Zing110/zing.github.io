# Academic homepage roadmap

## Current direction

The site is a static academic profile built with Astro and hosted entirely on GitHub Pages. The design prioritizes readable research content, fast loading, and simple maintenance over decorative interaction.

## Content still to add

- Verified affiliation and education history
- Publication list with canonical links
- Downloadable CV
- Preferred public contact address
- Two or three additional research or engineering case studies

Keep private drafts and source documents in `_source/`; that directory is ignored by Git and is never included in the deployed site.

## Deployment

Pushes to `main` trigger the GitHub Actions workflow in `.github/workflows/deploy.yml`. The workflow installs dependencies, builds the Astro project, and publishes `dist/` to GitHub Pages.
