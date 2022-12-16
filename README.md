# Real Estate Django Web App
    A real estate listings website built with `python` `django` `bootstrap`.
    A simple, reponsive  website. Built with:
    - Python 🐍
    - Django 🎸
    - Bootstrap 4 🌈
    - Vanilla JS - ES6
    - JQuery

#Build Deploy to server
    - push to dev branch
    - create new branch release/$TAG ($TAG is version release branche)
    - login ssh server, run ./update.sh $TAG
    docker stack deploy --compose-file docker-compose.production.yml app   //deploy app
    docker stack rm search_engine   //deploy app

#Work with DB Server:
    psql -h db -d tgnp -U postgres
    python manage.py makemigrations
    python manage.py migrate
    python manage.py check
    pg_restore -c --dbname=postgresql://postgres:postgres@127.0.0.1/tgnp tgnp-2021-08-24.dump
    pg_basebackup -h --dbname=postgresql://postgres:postgres@127.0.0.1/tgnp -D /usr/app/data
    Open/Close port DB, update status server(comment/uncomment 2 dòng ports, comment 2 dòng expose DB trong file docker-compose.production.yml)
        docker-compose -f docker-compose.yml up -d db

#Docker command
    docker system df
    docker image prune -a
    docker volume prune -a
    docker cache prune -a
    sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*-json.log'
    sudo systemctl start docker         start docker
    docker restart $(docker ps -a -q)    restart all container
    docker logs -f --tail 5 app_web_1       showlog
    docker container ls         list container
    docker container start [OPTIONS] CONTAINER [CONTAINER...]
    docker container restart [OPTIONS] CONTAINER [CONTAINER...]
        docker container restart app_nginx_1
        docker container restart app_web_1
        docker container restart app_db_1
        docker rm -f app_redis_1
        docker rm -f app_nginx_1

#auto update & build new code on localserver
    docker-compose -f docker-compose.yml exec nginx bash -c "nginx -s reload"
    docker-compose -f docker-compose.yml up -d
    docker-compose -f docker-compose.yml up --build web
    docker-compose -f docker-compose.yml exec web bash -c "pip install -r requirements.txt"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py collectstatic --clear"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py collectstatic --noinput"
    docker-compose -f docker-compose.yml exec web bash -c "npx gulp build"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py makemigrations"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py showmigrations"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py migrate --fake"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py migrate --noinput"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py migrate --fake-initial"
    docker-compose -f docker-compose.yml restart web
    docker-compose -f docker-compose.yml up -d search_engine
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py index_area"
    docker-compose -f docker-compose.yml exec web bash -c "python manage.py index_listing"

#update and build release on server
    cd app
    docker-compose -f docker-compose.production.yml up -d certbot  
    docker-compose -f docker-compose.production.yml up --build web
    docker-compose -f docker-compose.production.yml exec nginx bash -c "nginx -s reload"
    cd app
    git reset --hard
    git clean -fd
    git fetch && git checkout release/$1
    git pull
    docker-compose -f docker-compose.production.yml exec web bash -c "pip install -r requirements.txt"
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py collectstatic --clear"
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py collectstatic --noinput"
    docker-compose -f docker-compose.production.yml exec web bash -c "npx gulp build"
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py showmigrations"
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py makemigrations --merge"
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py migrate --fake"
    docker-compose -f docker-compose.production.yml restart web
    docker-compose -f docker-compose.production.yml up -d search_engine
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py index_area"
    docker-compose -f docker-compose.production.yml exec web bash -c "python manage.py index_listing"
    
