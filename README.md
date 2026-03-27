# Jclaw MVP

## Prerequisites
- Install Python and Node.js before running local checks.

## Verification targets
- `docker compose up -d`
- `make backend-test`
- `make desktop-test`
- `make test`

## Smoke expectation
- In current bootstrap state, `make test` is expected to fail with missing `apps/backend` and `apps/desktop` directories until app scaffolds are added.
