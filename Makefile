.PHONY: run clean

export PYTHONPATH := src

run:
	@echo "Starting the service..."
	docker compose up -d
	poetry run python -m wiki_helper

clean:
	@echo "Stopping the service..."
	docker compose down
