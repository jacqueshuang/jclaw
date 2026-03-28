backend-test:
	cd apps/backend && python -m pytest

desktop-test:
	cd apps/desktop && npm test

lint:
	cd apps/backend && python -m pytest tests/test_health.py -q
	cd apps/desktop && npm run test -- --runInBand

test: lint
