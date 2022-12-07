start:
	docker-compose up --build -d
down:
	docker-compose down -v	
stop:
	docker-compose stop
rmi-none:
	sudo docker rmi $$(sudo docker images -f "dangling=true" -q)
prune:
	sudo docker system prune
it:
	sudo docker run -it docker-db-uvicorn_back sh
tests:
	sudo docker exec --env-file db/.env.dev docker-db-uvicorn_back_1 pytest .
logs:
	sudo docker logs docker-db-uvicorn_back_1
mypy:
	docker-compose run back mypy /app/app
black:
	docker-compose run back black /app/app
flake8:
	docker-compose run back flake8 /app/app
pre-commit: black flake8 mypy tests 
alembic-init:
	docker-compose run back alembic revision --autogenerate -m "Initial"
alembic-upgrage:
	docker-compose run back alembic upgrade head
