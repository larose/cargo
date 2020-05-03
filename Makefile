GENERATED_DOCKERFILE=Dockerfile.generated
CHANGELOG_FILENAME=CHANGELOG.md
TEMPLATE_DOCKERFILE=Dockerfile.template
TEST_DOCKER_IMAGE=cargo-tests
PYPI_REPO_NAME=pypi
PYPI_JSON_API_URL=https://pypi.org/pypi
PYPI_LEGACY_API_URL=https://upload.pypi.org/legacy/
TEST_PYPI_REPO_NAME=test-pypi
TEST_PYPI_JSON_API_URL=https://test.pypi.org/pypi
TEST_PYPI_LEGACY_API_URL=https://test.pypi.org/legacy/
SOURCE_DIRS=cargo examples scripts tests

.PHONY: build
build:
	poetry build

.PHONY: bootstrap
bootstrap: bootstrap.install

.PHONY: bootstrap.install
bootstrap.install:
	poetry install

.PHONY: ci.bootstrap
ci.bootstrap:
	pip install poetry
	make bootstrap

.PHONY: ci.configure-poetry
ci.configure-poetry:
	poetry config repositories.$(PYPI_REPO_NAME) $(PYPI_LEGACY_API_URL)
	@poetry config pypi-token.$(PYPI_REPO_NAME) $(PYPI_API_TOKEN)
	poetry config repositories.$(TEST_PYPI_REPO_NAME) $(TEST_PYPI_LEGACY_API_URL)
	@poetry config pypi-token.$(TEST_PYPI_REPO_NAME) $(TEST_PYPI_API_TOKEN)
	poetry config --list

.PHONY: ci.publish.pypi
ci.publish.pypi:
	python scripts/publish.py $(PYPI_REPO_NAME) $(PYPI_JSON_API_URL)

.PHONY: ci.publish.test-pypi
ci.publish.test-pypi:
	python scripts/publish.py $(TEST_PYPI_REPO_NAME) $(TEST_PYPI_JSON_API_URL)

.PHONY: ci.update-version-in-pyproject
ci.update-version-in-pyproject:
	python scripts/update_version_in_pyproject.py $(CHANGELOG_FILENAME)

.PHONY: ci.tag-release
ci.tag-release:
	bash scripts/tag_release.sh

.PHONY: check
check: lint test

.PHONY: clean
clean:
	rm -rf dist

.PHONY: format
format:
	poetry run black $(SOURCE_DIRS)
	poetry run isort --recursive $(SOURCE_DIRS)

.PHONY: lint
lint: lint.format lint.types

.PHONY: lint.format
lint.format:
	poetry run flake8 $(SOURCE_DIRS)
	poetry run isort --check-only --diff --ignore-whitespace --recursive --quiet $(SOURCE_DIRS)
	poetry run black --check --diff $(SOURCE_DIRS)


# --cache-dir=/dev/null because mypy fails on the second run with:
#   AssertionError: Cannot find component 'D' for 'tests.test_recursive.D'
.PHONY: lint.types
lint.types:
	poetry run mypy --cache-dir=/dev/null $(SOURCE_DIRS)


.PHONY: test
test: test.unit test.integration

.PHONY: test.unit
test.unit:
	poetry run pytest

.PHONY: test.integration
test.integration: clean build
	python -c 'import sys; print(f"FROM python:{sys.version_info.major}.{sys.version_info.minor}-buster")' > $(GENERATED_DOCKERFILE)
	cat $(TEMPLATE_DOCKERFILE) >> $(GENERATED_DOCKERFILE)
	docker build --tag $(TEST_DOCKER_IMAGE) --file $(GENERATED_DOCKERFILE) .
	docker run --rm $(TEST_DOCKER_IMAGE) pytest -v
