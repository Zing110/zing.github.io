# Zeqing Wang — Academic Homepage

A focused academic portfolio built with [Astro](https://astro.build/). The site presents research interests, selected work, and public projects in a lightweight, accessible layout.

## Local development

```sh
npm install
npm run dev
```

Run `npm run build` to generate the production site in `dist/`.

## Deployment

The repository deploys directly to GitHub Pages through `.github/workflows/deploy.yml`. Every push to `main` builds the Astro site and publishes the generated static files; no personal server is required.

Live site: <https://zing110.github.io/zing.github.io/>

## Content updates

- Main academic profile: `src/pages/index.astro`
- Extended biography: `src/pages/about.astro`
- Global visual system: `src/styles/global.css`
- Site metadata and page shell: `src/layouts/Layout.astro`

Private source material can be kept in `_source/`, which is excluded from Git.
