# Personality-Analyzer
**Commands for install library**:
* pip install -r requirements.txt
* pip install -r requirements-dev.txt

**Commands for alembic**:
* for generate migration (use user table): alembic revision --autogenerate -m "create users table"
* Before generate migration: alembic upgrade head
* Откатить на одну миграцию назад: alembic downgrade -1
* Откатить на самое начало (тоесть игнорирует все предыдущие миграции): alembic downgrade base

**Commands for docker**:
* create command: docker compose up -d pg
* valid(works docker?): docker compose ps