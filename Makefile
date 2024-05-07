# A self-documenting Makefile
# You can set these variables from the command line, and also
# from the environment for the first two.

SOURCEDIR = ./ocx_common
CONDA_ENV = ocx_common
COVDIR = htmlcov
# Color output
BLUE='\033[0;34m'
NC='\033[0m' # No Color


# PROJECT setup using conda and powershell
conda-create:  ## Create a new conda environment with the python version and basic development tools as specified in environment.yml
	@conda env create -f environment.yml

conda-upd:  ## Update the conda development environment when environment.yml has changed
	@conda env update -f environment.yml


conda-clean: ## Purge all conda tarballs, log files and caches
	conda clean -a -y

conda-activate: ## Activate the conda environment for the project
	@conda activate $(CONDA_ENV)



doc-serve: ## Open the the html docs built by Sphinx
	@cmd /c start "_build/index.html"

ds: doc-serve

doc: ## Build the html docs using Sphinx. For other Sphinx options, run make in the docs folder
	@sphinx-build docs _build

doc-links: ## Check the internal and external links after building the documentation
	@sphinx-build docs -W -b linkcheck -d _build/doctrees _build/html

# POETRY ########################################################################
build:   ## Build the package dist with poetry
	@poetry update
	@poetry build

poetry-fix:  ## Force pip poetry re-installation
	@pip install poetry --upgrade

export:   ## Export the dependencies to docs/requirements.txt
	@poetry export --with=docs --without-hashes -o ./docs/requirements.txt


# pre-commit ######################################################################
pre-commit:	## Run any pre-commit hooks
	@pre-commit run --all-files

sourcery:  ## Run sourcery with --fix
# TESTS #######################################################################
	@sourcery review --fix --no-summary $(SOURCEDIR)


test:  ## Run unit and integration tests
	@pytest -m "not skip" --durations=5  --cov-report html --cov $(PACKAGE) .

test-upd:  ## Run unit and integration tests
	@pytest --force-regen --durations=5  --cov-report html --cov $(PACKAGE) .


test-cov:  ## View the test coverage report
	cmd /c start $(CURDIR)/htmlcov/index.html

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

#-----------------------------------------------------------------------------------------------
