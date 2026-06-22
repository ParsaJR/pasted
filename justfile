#############
# Database  #
#############

postgres_tag := "16-alpine"
postgres_password := "secret"
postgres_container_name := "pasted-postgres-dev"

setup-db:
	@docker volume create pgdata
	@docker run --detach \
		--name {{postgres_container_name}} \
		--volume pgdata:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD={{postgres_password}} \
		-p 127.0.0.1:5432:5432 \
		postgres:16-alpine

stop-db:
	@docker stop {{postgres_container_name}}

remove-db:
	@docker rm -f {{postgres_container_name}}

############
# Alembic  

#
############

alembic_conf := "./app/alembic.ini"

create-migration message:
	@uv run alembic -c {{alembic_conf}} revision --autogenerate -m "{{message}}"

migrate:
	@uv run alembic -c {{alembic_conf}} upgrade head

rollback:
	@uv run alembic -c {{alembic_conf}} downgrade -1
