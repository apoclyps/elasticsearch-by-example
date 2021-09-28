.PHONY: help build.test build.web run start debug stop clean logs shell network lint test docs docs.generate artifact datadog.run datadog.start

GIT_SHA = $(shell git rev-parse HEAD)
DOCKER_REPOTAG = $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(GIT_SHA)

default: help

build.base: ## Build the base service
	@docker-compose build base

build.test: ## Build the test container
	@docker-compose build test

build.web: ## Build the web container
	@docker-compose build web

help: ## show this help
	@echo
	@fgrep -h " ## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -Ee 's/([a-z.]*):[^#]*##(.*)/\1##\2/' | column -t -s "##"
	@echo

elasticsearch.create.indexes: network build.web  ## Run database seed locally
	@docker-compose run --rm web flask create-indexes

elasticsearch.delete.indexes: network build.web ## Run database seed locally
	@docker-compose run --rm web flask delete-indexes

run: start logs ## run the application locally

start:  ## run the application locally in the background
	@docker-compose up --build --detach web

debug: start ## run the application locally in debug mode
	@docker attach $$(docker-compose ps --quiet web)

stop: ## stop the application
	@docker-compose down --remove-orphans

clean: ## delete all data from the local elasticsearch
	@docker-compose down --remove-orphans --volumes

logs: ## show the application logs
	@docker-compose logs --follow web

shell: ## shell into a development container
	@docker-compose build web
	@docker-compose run --rm web sh

network: ## Create the elasticsearch-by-example network if it doesn't exist
	docker network create --driver bridge elasticsearch-by-example || true

lint: ## lint and autocorrect the code
	@docker-compose build web
ifeq ($(CI),true)
	@docker-compose run --rm --no-deps web sh -c "black . --check && isort --check-only --diff . && mypy . --ignore-missing-imports && flake8 ."
else
	@docker-compose run --rm --no-deps web sh -c "black . && isort . && mypy . --ignore-missing-imports && flake8 ."
endif

test: build.test network ## Run the unit tests and linters
	@docker-compose -f docker-compose.yml -f env/test.yml run --rm test sh scripts/test.sh
	@docker-compose down

test-shell: ## Spin up a shell in the test container
	@docker-compose -f docker-compose.yml -f env/test.yml build test
	@docker-compose -f docker-compose.yml -f env/test.yml run --rm test sh

unit: ## Run a single unittest or file e.g.: `make unit test=test.py::test`
	@docker-compose -f docker-compose.yml -f env/test.yml run --rm test pytest -vvv $(test)

docs: ## Run the documentation service
	@docker-compose up --build --detach swagger
	@echo
	@echo Swagger running: http://localhost:8080
	@echo

docs.generate: ## Generates the OpenAPI documentation
	@docker-compose build web
	@docker-compose run --rm --no-deps web scripts/docs.py --path=./openapi.yaml

artifact: ## build and push the application's Docker container
	docker build -t $(DOCKER_REPOTAG) .
	docker push $(DOCKER_REPOTAG)

datadog.run: datadog.start logs ## run the application locally with Datadog

datadog.start: ## run the application locally in the background with Datadog
	@docker-compose -f docker-compose.yml -f docker-compose.datadog.yml up --build --detach web
