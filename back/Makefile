prune:
	sudo docker system prune
build:
	sudo docker build . -t python:app --rm
run:
	sudo docker run -p 8015:8015 -it --rm python:app
rmi-none:
	sudo docker rmi $$(sudo docker images -f "dangling=true" -q)
