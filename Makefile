PYTHON := python3
TESTRUNNER := -m pytest tests --tb=native -vv -s
COVERAGE := --cov=pennylane_ls --cov-report term-missing --cov-report=html:coverage_html_report

.PHONY: help
help:
	@echo "Usage: make [target] where [target] can be any of"
	@echo "  install     - to install pennylane_ls"
	@echo "  test        - to run the unittests"
	@echo "  coverage    - to generate a coverage report"
	@echo "  benchmark   - to run a few benchmarks"

.PHONY: install
install:
	$(PYTHON) setup.py install

.PHONY: wheel
wheel:
	$(PYTHON) setup.py bdist_wheel

.PHONY: dist
dist:
	$(PYTHON) setup.py sdist

.PHONY: test
test:
	$(PYTHON) $(TESTRUNNER)

.PHONY: coverage
coverage:
	@echo "Generating coverage report..."
	$(PYTHON) $(TESTRUNNER) $(COVERAGE)
