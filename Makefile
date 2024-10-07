start-redpanda:
	podman-compose -f redpanda.yml up -d

stop-redpanda:
	podman-compose -f redpanda.yml stop