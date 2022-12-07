start:
	sudo docker-compose up --build -d
down:
	sudo docker-compose down -v	
stop:
	sudo docker-compose stop
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
alembic-init:
	docker-compose run back alembic revision --autogenerate -m "Initial"
alembic-upgrage:
	sudo docker-compose run back alembic upgrade head
