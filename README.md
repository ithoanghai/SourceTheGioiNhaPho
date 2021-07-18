# Real Estate Django Web App

A real estate listings website built with `python` `django` `bootstrap`.

A simple, reponsive  website. Built with:

- Python 🐍
- Django 🎸
- Bootstrap 4 🌈
- Vanilla JS - ES6
- JQuery


Search Engine - Meilisearch:
- Run docker-compose up --build web. Setup port and environment variables (MEILI_HOST, MEILI_PORT)
- Run docker-compose exec web bash -c "python manage.py index_listing"
- Run "python manage.py index_listing" to create indexer