start-redpanda:
	podman-compose -f redpanda.yml up -d

stop-redpanda:
	podman-compose -f redpanda.yml down

start-redpanda_1:
	podman-compose -f redpanda.yml start