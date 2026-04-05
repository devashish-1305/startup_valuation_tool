# Startup Valuation — React frontend

Connects to the FastAPI backend in the repo root (`api.py`). Design direction matches Stitch project **Financial Valuation Tool** (teal accent, white surfaces, Manrope + Inter).

## Run (development)

1. Start the API (from repo root):

   ```bash
   uvicorn api:app --reload --port 8000
   ```

2. Install and run the frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000). Vite proxies `/api/*` to `http://127.0.0.1:8000` (see `vite.config.ts`).

## Environment

- **`VITE_API_BASE_URL`** — Optional. Set if the API is not proxied (e.g. `https://api.example.com` with no trailing slash). Leave unset for local dev with the proxy.

## Build

```bash
npm run build
```

Serve `dist/` behind any static host; configure the same-origin API or set `VITE_API_BASE_URL`.

## Design vs Google Stitch

Stitch exports **screenshots and HTML** for a fixed canvas; this app is a **hand-built React UI** that follows the same **design tokens** (teal primary `#00685f` / `#0d9488`, light surfaces, Manrope + Inter, soft shadows). It will not match Stitch **pixel-for-pixel** unless you **port HTML/CSS from Stitch** into components or rebuild sections from exported assets. Styles live in `src/styles/index.css` and are tuned to project **310911392740599810** (“Financial Valuation Tool”).
