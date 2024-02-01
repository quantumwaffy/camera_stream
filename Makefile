.PHONY: help build run init_linters lint

ORG ?= test
REPO ?= detector
APP ?= detector_app
MAIN_CAMERA ?= /dev/video0

XSOCK ?= /tmp/.X11-unix
XAUTH ?= /tmp/.docker.xauth


help: ## Commands
	@echo "Please use 'make <target>' where <target> is one of:"
	@awk -F ':|##' '/^[a-zA-Z\-_0-9]+:/ && !/^[ \t]*all:/ { printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$3 }' $(MAKEFILE_LIST)

build: ## Build Docker image
	docker build -t $(ORG)/$(REPO) .

run: ## Run Docker container
	@xhost +local:docker
	@#xauth nlist $(DISPLAY) | sed -e 's/^..../ffff/' | xauth -f $(XAUTH) nmerge -
	@docker run -m 8GB --rm --privileged --name $(APP) -e DISPLAY=$(DISPLAY) -v $(XSOCK):$(XSOCK) -v $(XAUTH):$(XAUTH) -e XAUTHORITY=$(XAUTH) -v $(MAIN_CAMERA):$(MAIN_CAMERA) -v ./camera_stream:/app $(ORG)/$(REPO) python3 main.py
	@xhost -local:docker

init_linters: ## Install pre-commit hooks
	@pre-commit install


lint: init_linters ## Run linting
	@pre-commit run -a
