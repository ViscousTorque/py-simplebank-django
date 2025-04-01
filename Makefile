DB_URL=postgresql://admin:adminSecret@localhost:5432/simple_bank?sslmode=disable

network:
	docker network create bank-network

postgres:
	docker run -d --rm \
  --name postgres \
  --network bank-network \
  -p 5432:5432 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=adminSecret \
  -e POSTGRES_DB=simple_bank_py \
  -v postgres-data:/var/lib/postgresql/data \
  postgres

pgadmin4:
	docker run -d --rm \
  --name pgadmin4 \
  --network bank-network \
  -p 8000:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@example.com \
  -e PGADMIN_DEFAULT_PASSWORD=adminSecret \
  -v pgadmin-data:/var/lib/pgadmin \
  dpage/pgadmin4

redis:
	docker run -d --rm --name redis -p 6379:6379 -d redis:7-alpine

DOCKER_RUNNING := $(shell docker ps -q -f name=postgres)

create-db:
	@echo "DOCKER_RUNNING is [$(DOCKER_RUNNING)]"
ifeq ($(DOCKER_RUNNING),)
	@echo "Using local psql to create DB with owner 'simplebank'"
	psql -h localhost -U admin -d postgres -c "CREATE DATABASE simple_bank_py OWNER simplebank;"
else
	@echo "Using docker to create DB with owner 'simplebank'"
	docker exec -it postgres createdb --username=admin --owner=simplebank simple_bank_py
endif

dropdb:
	docker exec -it postgres dropdb simple_bank_py

stopdb:
	docker stop postgres pgadmin4

db_docs:
	dbdocs build doc/db.dbml

db_schema:
	dbml2sql --postgres -o doc/schema.sql doc/db.dbml

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

create-superuser:
	python manage.py createsuperuser

startLocalEnv:
	@$(MAKE) postgres
	@sleep 2
	@$(MAKE) pgadmin4
	@sleep 2
	@$(MAKE) redis

server:
	python manage.py runserver 5000

frontend:
	cd frontend && npm run dev

shell:
	python manage.py shell

ci_comp_tests:
	@set -e; \
	docker compose -f docker-compose.ci.yaml build unitests component_tests && \
	docker compose -f docker-compose.ci.yaml up -d postgres migrations && \
	docker compose -f docker-compose.ci.yaml run --rm unitests && \
	docker compose -f docker-compose.ci.yaml run --rm component_tests; \
	EXIT_CODE=$$?; \
	docker compose -f docker-compose.ci.yaml down; \
	exit $$EXIT_CODE

dev_comp_tests:
	docker compose -f docker-compose.dev.yaml up --build --abort-on-container-exit

unittests:
	coverage run manage.py test --settings=config.settings_test
	coverage report

unittests-html:
	coverage html
	xdg-open htmlcov/index.html

.PHONY: startLocalEnv network postgres createdb dropdb db_docs db_schema migrate migrations frontend redis stopdb server shell ci_comp_tests dev_comp_tests unittests unittests-html
