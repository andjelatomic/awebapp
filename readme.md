I am not great fan of using pythong to create websites, since there are much more 
professional tools and languages, and much closer to the dataflow, and the actual
datapackages internet flow. 

Anyhow, this is small example made as a part of an asignment, very quickly, in less then a day,
just to show posibilities on how to use Python, FastAPI, SQLITE, SQLAlchemy to build simple
website.

You can find in here:
 - How to design simple relational database. This example is in SQLIte, but it can be used in SQL Server (MS) and Oracle server as well, as two fastest database servers
 - How to use FastAPI, get and push data to the webpage, set and get cookies, and how to process HTML pages with the dynamic data.
 - Different database functions, and two different approach to pull/insert/update data into the relational database
 




- Please use the following line to  pull docker image with ->
docker pull ghcr.io/andjelatomic/awebapp

- To run the docker, please define port 8001 for the webserver (locally accessed port : docker side port).

docker run -p8001:8001 ghcr.io/andjelatomic/awebapp
