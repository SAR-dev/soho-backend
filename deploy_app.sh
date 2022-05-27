#!/bin/sh

sudo docker-compose -f docker-compose.prod.yml down
sudo docker-compose -f docker-compose.prod.yml up --build -d
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

