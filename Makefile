TAG := $(shell git describe --tags --abbrev=0)
IMAGE_NAME := inari-mastermind

build:
	docker build -t $(IMAGE_NAME) .

test:
	python3 -m pytest tests/

run:
	docker-compose up --build
