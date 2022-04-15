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
- Run docker-compose exec web bash -c "python manage.py index_area"
- Run "python manage.py index_area" to create indexer

Build Deploy to server
- push to dev branch
- create new branch release/$TAG ($TAG is version release branche)
- login ssh server, run ./update.sh $TAG

Open/Close port DB
- comment/uncomment 2 dòng ports, comment 2 dòng expose trong file docker-compose.production.yml
- chạy lệnh: docker-compose -f docker-compose.production.yml up -d
pg_restore -c --dbname=postgresql://postgres:postgres@127.0.0.1/tgnp tgnp-2021-08-24.dump

Show Log docker
- docker logs -f --tail 5 app_web_1

Restart certificate on docker
docker-compose -f docker-compose.production.yml exec -it certbot /bin/sh
docker-compose -f docker-compose.production.yml up -d certbot  
docker-compose -f docker-compose.production.yml exec nginx bash -c "nginx -s reload"

