run-dev:
	cp dev.env .env
	poetry run python src/main.py 

build:
	podman build -t trade_producer .

run: build
	podman run --network=redpanda_network --env-file=prod.env trade_producer
