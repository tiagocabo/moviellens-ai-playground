

build:
	docker build . -t movilens-ai-playground

lunch: build
	docker run movilens-ai-playground