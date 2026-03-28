# Jclaw MVP

## Prerequisites
- Install Python and Node.js before running local checks.

## Verification targets
- `docker compose up -d`
- `make backend-test`
- `make desktop-test`
- `make lint`
- `make test`

## Local run
1. `docker compose up -d`
2. `cd apps/backend && uvicorn app.main:app --reload`
3. `cd apps/desktop && npm install && npm run dev`
4. `cd apps/desktop/src-tauri && cargo tauri dev`

## Smoke expectation
- `make backend-test` should pass.
- `make desktop-test` should pass.
