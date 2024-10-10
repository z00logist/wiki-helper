.PHONY: run clean

export PYTHONPATH := src

run:
	@echo "Starting the service..."
	docker compose up -d
	poetry run python -m wiki_helper

clean:
	@echo "Stopping the service..."
	docker compose down

prepare:
	@echo "Creating virtual environment..."
	virtualenv -p $(which python3.12) .venv
	@echo "Activating virtual environment..."
	@source .venv/bin/activate && \
		echo "Installing environment with Poetry..." && \
		poetry install --no-root && \
		echo "Downloading baseline models..." && \
		resources/download-models.sh