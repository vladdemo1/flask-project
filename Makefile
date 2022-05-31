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

clear_network:
	$ sudo docker network prune

clear_volume:
	$ sudo docker volume prune

show_images:
	$ sudo docker images -a
