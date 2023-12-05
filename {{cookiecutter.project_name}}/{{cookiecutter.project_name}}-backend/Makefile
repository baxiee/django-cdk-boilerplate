SHELL=/bin/bash -euo pipefail

COMPOSE_ARGS=-f ./local/compose/docker-compose.yml

.PHONY: build up upbuild stop restart down clean ps logs shell django makemigrations


build:
	docker-compose ${COMPOSE_ARGS} build


up:
	docker-compose ${COMPOSE_ARGS} up


upbuild:
	docker-compose ${COMPOSE_ARGS} up --build


stop:
	docker-compose ${COMPOSE_ARGS} stop


restart:
	docker-compose ${COMPOSE_ARGS} restart


down:
	docker-compose ${COMPOSE_ARGS} down


clean:
	docker-compose ${COMPOSE_ARGS} down --remove-orphans -v


ps:
	docker-compose ${COMPOSE_ARGS} ps


logs:
	docker-compose ${COMPOSE_ARGS} logs -f


shell:
	docker-compose ${COMPOSE_ARGS} exec django bash


admin:
	docker-compose ${COMPOSE_ARGS} exec django bash -c "cd backend && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin1').exists() or User.objects.create_superuser('admin1', 'admin1@example.com', 'admin1')\""


django:
	docker-compose ${COMPOSE_ARGS} exec django bash -c "cd backend && python manage.py shell"


makemigrations:
	docker-compose ${COMPOSE_ARGS} exec django bash -c "cd backend && python manage.py makemigrations"
