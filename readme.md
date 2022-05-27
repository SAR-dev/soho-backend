# Deployment instructions:
1. Go to project root directory.
2. Run `chmod +x app/entrypoint.prod.sh` 
3. Run `git fetch`.
4. Run `git pull`.
5. Run `sudo ./deploy.sh`. (Might need to make this executable at first). Alternatively we can run the following commands:
    1. `sudo docker-compose -f docker-compose.prod.yml down`
    2. `sudo docker-compose -f docker-compose.prod.yml up --build -d`
    3. `sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`
    4. `sudo docker-compose -f docker-compose.prod.yml  exec web python manage.py collectstatic --noinput`

# Docker containers instructions
There are three containers configured in total:
1. Web: Runs django server
2. db: Runs posgres version 13.0
3. nginx: Runs nginx for production environment

Two separate environments have been configured:
1. Development: Has only db and web containers. Because no reverse proxy is needed for development environment.
 For any change in development containers, name changes to Dockerfile and docker-compose.yml files. .env.dev contains the 
 environment variables for dev environment. To build docker containers locally for development:
    1. Run `docker-compose up --build` to build the containers.
    2. Once the containers are up, we can run `docker-compose exec web python manage.py migrate --noinput` to run pending migrations.
    3. Once the build is complete, we can simply run `docker-compose up --build` to start development server.
2. Production: Has additional nginx container. To make any change in production containers, look at Dockerfile.prod, docker-compose.prod.yml.
The environment variables are stored in .env.prod and .env.prod.db.
3. Resources followed for creating deployment config:
    1. https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
    2. For ssl configuration we can follow https://realpython.com/django-nginx-gunicorn/#starting-with-django-and-wsgiserver
    3. Connect Godaddy with EC2 instance: https://www.youtube.com/watch?v=VedY6EjOBWM&ab_channel=Javapocalypse

# Important Notes
1. After creating EC2 instance, make sure to expose necessary ports in Security Group rules for that EC2 instance. For example we need to expose 80 and 443 ports for receiving http requests.
2.  

  
