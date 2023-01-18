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
	docker-compose run back pytest -q -s .
	# sudo docker exec --env-file db/.env.dev docker-db-uvicorn_back_1 pytest -q .
logs:
	sudo docker logs docker-db-uvicorn_back_1
mypy:
	docker-compose run back mypy /app/app
black:
	docker-compose run back black --line-length 100 /app/app/
flake8:
	docker-compose run back flake8 /app/app
chown:	
	sudo chown -R www:www *
pre-commit: black flake8 mypy tests 
prometheus:
	sudo docker service create --replicas 1 --name my-prometheus \
    	--mount type=bind,source=/home/www/projects/docker/prometheus/prometheus.yml,destination=/etc/prometheus/prometheus.yml \
    	--publish published=9090,target=9090,protocol=tcp \
    	prom/prometheus

alembic-upgrade:
	docker-compose run back alembic upgrade head

alembic-revision:
	docker-compose run back alembic revision --autogenerate -m "comment"
