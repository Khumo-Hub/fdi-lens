# FDI Lens — Static Portfolio Preview

This is a **frontend-only** preview for Netlify. The application is built to static
**HTML, CSS and JavaScript** files by Vite. A Python server, Railway service
or SQLite database is **not required** for this deployment.

## Netlify settings

Choose the GitHub repository `Khumo-Hub/fdi-lens` and branch
`feature/static-netlify-preview` while validating the preview.
After the change is merged, select `main`.

| Netlify setting | Value |
| --- | --- |
| Base directory | `frontend` |
| Build command | `npm run build` |
| Publish directory | `dist` |
| Environment variable | `VITE_DEMO_MODE=true` |
| `VITE_API_URL` | **Do not set** for static demo mode |

If Netlify asks for a repository-root relative publish path, use
`frontend/dist` instead of `dist`.

## What works

- KPI dashboard, destination charts, sector charts and monthly trend toggle
- Interactive investment map (OpenStreetMap tiles still require internet)
- Global search and Ctrl+K shortcut
- Project table with filtering, sorting, pagination and detail modal

All 500 displayed projects are **deterministic, synthetic sample data**.
JavaScript generates and processes them directly inside the browser.
No API requests to Railway are sent in demo mode.

## Running locally

From `frontend/`:

```bash
npm install
```

Create a local `.env` file:

```env
VITE_DEMO_MODE=true
```

Then run `npm run dev`. To test the production build, run
`npm run build`.

## Reverting to live API mode

Remove `VITE_DEMO_MODE` (or set it to `false`) and set:

```env
VITE_API_URL=https://fdi-lens-api-production.up.railway.app
```

This preserves the original full-stack architecture. Demo figures are
not real FDI statistics and should never be represented as such.
