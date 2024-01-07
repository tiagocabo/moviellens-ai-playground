

build:
	docker build . -t movilens-ai-playground

lunch: build
	docker run -p 9090:9090 movilens-ai-playground

up:
	docker-compose up app