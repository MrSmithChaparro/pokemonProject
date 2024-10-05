.PHONY: build up migrate

build:
	docker-compose build

up:
	docker-compose up -d

migrate:
	docker-compose run app python manage.py migrate

start: build up migrate