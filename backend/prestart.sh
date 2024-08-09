#! /usr/bin/env bash

# Let the DB start
python /app/app/backend_pre_start.py

# Run migrations
# alembic revision --autogenerate -m "add superuser to be role enum"
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py
