[Back to README.md](../README.md)

<h1>Docker</h1>
The project is dockerized. At the moment it creates a django container and a postgresql container. 
Postgres has an extension called postgis. This is a nice geo feature, that, i think, mirjam included. 

The postgres container will create a .data directory in your root folder. 
This folder contains the database. The data you gather in your 
django instance will be written to the db in the container and to the .data directory, too. 

Start the docker container by the following commands in your root directory. 
The one with the manage.py:
## Setup
```console
# this will create the docker image. Takes a while to download everything.
$ sudo docker compose build

# this will start the docker containers (django and postgresql). 
# again, takes a while during the first startup.
$ sudo docker compose up

# it is possible, that during the first <docker compose up>, the database isnt ready, when django is ready. If so:
# then stop the container by STRG+C. (stop the running containers). Then start it again.
$ sudo docker compose up
```
***From now on, every time you want to start the project, just run.***
```console
$ sudo docker compose up
```

Your project now runs on [http://127.0.0.1/](http://127.0.0.1/). 
No Port 8000. 
But its also possible, to run django the normal way. 

## Migration
***Migration is done as follows.***<br>
"docker compose run -rm" runs the the container, executes the command and shuts down again.
```console
$ sudo docker compose run --rm app python manage.py makemigrations
$ sudo docker compose run --rm app python manage.py migrate
```