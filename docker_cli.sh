# dele all images
docker rmi -f $(docker images -aq)

docker volume ls


docker volume rm $(docker volume ls -q)