PYTHON ?= python
APP ?= app.main:app
HOST ?= 127.0.0.1
PORT ?= 8000

.PHONY: install run test

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

test:
	$(PYTHON) -m pytest -q
