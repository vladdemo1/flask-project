COMPOSE ?= sudo docker-compose -f docker-compose.yml

run: build
	$(COMPOSE) up -d
	@echo http://localhost/

build:
	$(COMPOSE) build

rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

log:
	$ sudo docker logs my_app -f
