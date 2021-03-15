cr := podman
dump_path = "postgres:/db_dump"
#----------
# dev
#----------
.PHONY: dev
dev:
	-podman rm -f postgres
	podman run --network=host --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres


update:
