.PHONY: help setup-env all backend frontend attach-api migrate seed-mock-data-transpas generate-integration ci-frontend ci-backend

# Show help for available make targets
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "Available targets:"
	@awk '/^[a-zA-Z_-]+:/ {print "  " $$1}' $(MAKEFILE_LIST) | sed 's/://'

# ========================================
# 🔧 Code Quality & Development
# ========================================

fix:
	@echo "Cleaning code and running quality checks..."
	@uv run --extra dev ruff check . --fix
	@uv run --extra dev ruff format .
	@uv run --extra dev mypy .

# ========================================
# 🐳 Docker Operations
# ========================================

# Setup Docker infrastructure for CI
start-docker:
	@echo "Setting up Docker infrastructure for CI..."
	@docker compose up --build
	@docker compose down --remove-orphans
	@docker compose up --watch

# Start all services (uses current .env configuration)
all:
	docker compose up api --watch

backend:
	docker compose up api adminer --watch


attach-api:
	@docker attach $$(docker compose ps -q api)

# ========================================
# 🔧 Backend Development
# ========================================

# MySQL database migration command (app database)
migrate:
	@echo "Running MySQL database migrations (app database)..."
	@docker compose exec -T api make migrate


# ========================================
# 🚀 CI Pipeline
# ========================================

# Backend CI pipeline (build + start services + run checks + cleanup)
ci-backend:
	@echo "Building required containers for backend testing..."
	@docker compose down -v --remove-orphans
	@docker compose build api --no-cache

	@echo "Running backend quality checks and tests..."
	@docker compose up api -d
	@docker compose exec -T api make qa || { docker compose logs api; exit 1; }
	@docker compose exec -T api make test || { docker compose logs api; exit 1; }
	@docker compose down -v --remove-orphans