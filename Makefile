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
	sudo docker exec docker-db-uvicorn_back_1 pytest .
logs:
	sudo docker logs docker-db-uvicorn_back_1
