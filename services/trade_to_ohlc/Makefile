run-live-dev:
	cp live.dev.env .env
	poetry run python src/main.py

build:
	podman build -t trade_to_ohlc .

run: build
	podman run --network=redpanda_network --env-file=live.prod.env trade_to_ohlc