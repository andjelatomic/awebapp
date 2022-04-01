- You can pull docker image with ->

docker pull ghcr.io/andjelatomic/awebapp

- Source code is on git ->

https://github.com/andjelatomic/awebapp

 -To run the docker, please define port 8001 for the webserver (locally accessed port : docker side port). You can change the access port of course if you want.

docker run -p8001:8001 ghcr.io/andjelatomic/awebapp
