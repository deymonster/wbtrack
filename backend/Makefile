.PHONY: start-dev
start-dev: ## start docker-compose.dev.yml
	docker compose -f docker-compose.dev.yml up -d

.PHONY: stop-dev
stop-dev: ## start docker-compose.dev.yml
	docker compose -f docker-compose.dev.yml stop

.PHONY: logs
log: ## view logs of docker-compose containers
	docker compose -f docker-compose.dev.yml logs --tail=150 -f postgres

.PHONY: migrate
migrate: ## create and apply new alembic migration
	alembic revision --autogenerate && alembic upgrade head

.PHONY: migrate-apply
migrate-apply: ## apply alembic migrations to database/schema
	alembic upgrade head

.PHONY: migrate-create
migrate-create: ## create new alembic migration
	alembic revision --autogenerate

.PHONY: migrate-apply
docker-migrate-apply: ## apply alembic migrations to database/schema
	docker compose -f docker-compose.yml run backend alembic upgrade head

.PHONY: migrate-create
docker-migrate-create: ## create new alembic migration
	docker compose -f docker-compose.yml run backend alembic revision --autogenerate

.PHONY: docker-build
docker-build: ## create new alembic migration
	docker-compose -f docker-compose.dev.yml build --quiet