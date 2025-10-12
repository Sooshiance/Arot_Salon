.PHONY: install versions migrations migrate test run clean

VENV = ./.venv
PYTHON = $(VENV)/bin/python3.11
MANAGE = ./backend/manage.py 

run:
	$(PYTHON) $(MANAGE) runserver

migrations:
	$(PYTHON) $(MANAGE) makemigrations
	
migrate:
	$(PYTHON) $(MANAGE) migrate
	
test:
	$(PYTHON) $(MANAGE) test
