# Real Estate Django Web App

A real estate listings website built with `python` `django` `bootstrap`.

A simple, reponsive  website. Built with:

- Python 🐍
- Django 🎸
- Bootstrap 4 🌈
- Vanilla JS - ES6
- JQuery


Search Engine - Meilisearch:   Setup port and environment variables (MEILI_HOST, MEILI_PORT)
- Run docker-compose up --build web. 
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

Restart certificate on docker server
docker-compose -f docker-compose.production.yml exec -it certbot /bin/sh
docker-compose -f docker-compose.production.yml up -d certbot  
docker-compose -f docker-compose.production.yml exec nginx bash -c "nginx -s reload"

gộp dữ liệu
python manage.py makemigrations
python manage.py migrate

server:
docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py migrate"
local:
docker-compose exec web bash -c "python manage.py makemigrations"
docker-compose exec web bash -c "python manage.py showmigrations"
docker-compose exec web bash -c "python manage.py migrate --fake contenttypes"
docker-compose exec web bash -c "python manage.py migrate --fake accounts"
docker-compose exec web bash -c "python manage.py migrate --fake customers"
docker-compose exec web bash -c "python manage.py migrate --fake listings"
docker-compose exec web bash -c "python manage.py migrate --fake transactions"
docker-compose exec web bash -c "python manage.py migrate --fake-initial"
docker-compose exec web bash -c "python manage.py migrate"

#auto update & build new code on localserver
docker-compose exec web bash -c "pip install -r requirements.txt"
docker-compose exec web bash -c "python manage.py collectstatic --noinput"
docker-compose exec web bash -c "npx gulp build"
docker-compose exec web bash -c "python manage.py migrate"
docker-compose restart web
docker-compose up -d search_engine