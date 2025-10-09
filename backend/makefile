.PHONY: fix qa run dev test seed-mock-data map-download map-process map-delete

# ========================================
# 📖 Help
# ========================================

help:
	@echo "Available commands:"
	@echo "  fix              - Format code and fix linting issues"
	@echo "  qa               - Run code quality checks"
	@echo "  migrate          - Wait for MySQL DB and run migrations (app database)"
	@echo "  run              - Run migrations and start application"
	@echo "  dev              - Development mode with auto-reload"
	@echo "  test             - Run tests"
	@echo ""

# ========================================
# 🔧 Code Quality & Development
# ========================================

# Format code and fix linting issues
fix:
	@echo "Cleaning up code..."
	@uv run --extra dev ruff check . --fix
	@uv run --extra dev ruff format .
	@uv run --extra dev mypy api

# Run code quality checks
qa:
	@echo "Running quality checks on code..."
	@uv run --extra dev mypy api scripts || { docker compose logs api; exit 1; }
	@uv run --extra dev ruff check api scripts || { docker compose logs api; exit 1; }
	@uv run --extra dev ruff format api scripts --check || { docker compose logs api; exit 1; }

# ========================================
# 🚀 Application Commands
# ========================================

# Wait for MySQL DB and run migrations (app database)
migrate:
	@echo "Waiting for MySQL DB to be ready..."
	@uv run --extra dev alembic current
	@uv run --extra dev python scripts/seed_database.py


migrate-dev:
	@docker compose exec -T api uv run alembic revision --autogenerate -m "Update database"
	@docker compose exec -T api uv run alembic upgrade head

seed-db-dev:
	@docker compose exec -T api uv run scripts/seed_database.py

# Run migrations and start application
run: migrate
	@echo "Run migrations and start application..."
	@uv run uvicorn --host=:: --workers 4 api.api.src.main:app --reload

run-ipv4: migrate
	@echo "Run migrations and start application..."
	@uv run uvicorn --host=0.0.0.0 --workers 4 api.api.src.main:app --reload

# Development mode
dev:
	@echo "Start DB and run migrations..."
	@uv run --extra dev uvicorn --host=0.0.0.0 --workers 4 api.api.src.main:app --reload

# ========================================
# 🧪 Testing
# ========================================

# Run tests
test:
	@echo "Running tests..."
	@uv run --extra dev mypy .
	@uv run --extra dev pytest
