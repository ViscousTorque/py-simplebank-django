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

selenium:
	docker run -d \
	--network bank-network \
	--add-host=host.docker.internal:host-gateway \
	-p 4444:4444 \
	-p 7900:7900 \
	-e VNC_NO_PASSWORD=1 \
	selenium/standalone-chrome:123.0

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
	dbdocs build docs/db.dbml

db_schema:
	dbml2sql --postgres -o docs/schema.sql doc/db.dbml

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

stopLocalEnv:
	docker stop redis pgadmin4 postgres selenium android

server:
	python manage.py runserver 5000

frontend:
	cd frontend && npm run dev -- --host

shell:
	python manage.py shell

define run_test_sequence
	set -e; \
	COMPOSE="docker compose -f $(1)"; \
	echo "Running test sequence using $$COMPOSE"; \
	$$COMPOSE run --rm unittests; \
	$$COMPOSE run --rm migrations; \
	$$COMPOSE run --rm seed_users; \
	EXIT_CODE=0; \
	for SERVICE in $(TEST_SERVICES); do \
		$$COMPOSE run --rm $$SERVICE || EXIT_CODE=$$?; \
	done; \
	$$COMPOSE down; \
	if [ $$EXIT_CODE -eq 0 ]; then \
		echo "✅ All tests passed. ✅"; \
	else \
		echo "❌ One or more tests failed. ❌"; \
	fi; \
	exit $$EXIT_CODE
endef

define run_comp_tests
	set -e; \
	COMPOSE_FILE=$(1); \
	INFRA_SERVICES="$(2)"; \
	COMPOSE="docker compose -f $$COMPOSE_FILE"; \
	echo "Building containers for $$COMPOSE_FILE..."; \
	COMPOSE_BAKE=true $$COMPOSE build $(if $(NO_CACHE),--no-cache); \
	echo "Starting infrastructure: $$INFRA_SERVICES"; \
	$$COMPOSE up -d --remove-orphans $$INFRA_SERVICES; \
	$(call run_test_sequence,$(1))
endef

define run_comp_parallel_tests
	set -e; \
	COMPOSE_FILE=$(1); \
	INFRA_SERVICES="$(2)"; \
	COMPOSE="docker compose -f $$COMPOSE_FILE"; \
	echo "Starting android-emulator build ..."; \
	$$COMPOSE build $(if $(NO_CACHE),--no-cache) android-emulator; \
	echo "Docker container android-emulator build complete. Starting emulator..."; \
	$$COMPOSE up -d android-emulator; \
	echo "Building other containers..."; \
	FILTERED_INFRA_SERVICES="$(filter-out android-emulator,$(2))"; \
	COMPOSE_BAKE=true $$COMPOSE build $(if $(NO_CACHE),--no-cache) $$FILTERED_INFRA_SERVICES $$TEST_SERVICES; \
	echo "Starting remaining infrastructure..."; \
	$$COMPOSE up -d --remove-orphans $$FILTERED_INFRA_SERVICES; \
 	echo "Running setup services (unit tests, migrations, seed)..."; \
	$$COMPOSE run --rm unittests; \
	$$COMPOSE run --rm --no-deps migrations; \
	$$COMPOSE run --rm --no-deps seed_users; \
	echo "Waiting for emulator to boot..."; \
 	$$COMPOSE exec -T android-emulator bash ./component_tests/android_emulator/wait-for-emulator.sh; \
	$(call run_parallel_tests,$(1))
endef

define run_parallel_tests
	set -e; \
	EXIT_CODE=0; \
	PIDS=""; \
	for TEST_SERVICE in $(TEST_SERVICES); do \
		echo "Running $$TEST_SERVICE..."; \
		docker compose -f $(1) up --no-deps --exit-code-from $$TEST_SERVICE $$TEST_SERVICE & \
		PIDS="$$PIDS $$!"; \
	done; \
	for PID in $$PIDS; do \
		wait $$PID || EXIT_CODE=$$?; \
	done; \
	docker compose -f $(1) down --remove-orphans; \
	if [ $$EXIT_CODE -eq 0 ]; then \
		echo "✅ All component tests passed. ✅"; \
	else \
		echo "❌ One or more component tests failed. ❌"; \
	fi; \
	exit $$EXIT_CODE
endef

COMPOSE_FILE_CI = docker-compose.ci.yaml
COMPOSE_FILE_DEV = docker-compose.dev.yaml

TEST_SERVICES = behave_selenium_tests pytest_selenium_tests pytest_playwright_tests playwright_codegen_tests postman_tests pytest_appium_android
dev_comp_tests:
	$(call run_comp_tests,$(COMPOSE_FILE_DEV),postgres frontend backend pgadmin4 selenium android-emulator migrations seed_users)

ci_tests:
	@NO_CACHE=1 $(MAKE) _ci_tests_internal

_ci_tests_internal:
	$(call run_comp_parallel_tests,$(COMPOSE_FILE_CI),postgres frontend backend selenium migrations seed_users)

dev_comp_parallel_tests:
	$(call run_comp_parallel_tests,$(COMPOSE_FILE_DEV),postgres frontend backend pgadmin4 selenium migrations seed_users)

ci_parallel_tests:
	@NO_CACHE=1 $(MAKE) _ci_parallel_tests_internal

_ci_parallel_tests_internal:
	$(call run_comp_parallel_tests,$(COMPOSE_FILE_CI),postgres frontend backend selenium migrations seed_users)


open_html_report:s
	xdg-open test_reports/report.html

unittests:
	coverage run manage.py test --settings=config.settings_test
	coverage report

unittests-html:
	coverage html
	xdg-open htmlcov/index.html

documentation:
	python manage.py spectacular --file docs/openapi-schema.yml
	npx @redocly/cli build-docs docs/openapi-schema.yml -o docs/openapi.html
	
local-api-doc:
	make documentation
	bash -c 'cd docs && python -m http.server 7000 & \
	PID=$$!; \
	trap "kill $$PID" EXIT; \
	xdg-open http://localhost:7000/openapi.html; \
	wait $$PID'

.PHONY: documentation startLocalEnv network postgres createdb dropdb db_docs db_schema migrate migrations frontend redis stopdb server shell ci_comp_tests dev_comp_tests unittests unittests-html
