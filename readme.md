
# AWebApp
##### by Andjela Tomic 2022
***

I am not great fan of using Python for creating a website, since there are far more professional tools and languages, much closer to the dataflow, and to the actual internet datapackages flow. Of course, using this fat layer of libraries makes life in some sense easier. 

Anyhow, this is small example I've made as a part of an asignment, very quickly, in less than half of a day, just to show posibilities on how to use Python, FastAPI, SQLITE, SQLAlchemy to build simple website.

---


### You can find in here:
 - How to design simple relational database. This example is in SQLIte, but it can be used in SQL Server (MS) and Oracle server as well, as two fastest database servers
 - How to use FastAPI, get and push data to the webpage, set and get cookies, and how to process HTML pages with the dynamic data.
 - Different database functions, and two different approach to pull/insert/update data into the relational database
 
---

- Please use the following lines to pull and then to run it. Define port 8001 for the webserver (locally accessed port : docker side port).

```jsx 
docker pull ghcr.io/andjelatomic/awebapp
docker run -p8001:8001 ghcr.io/andjelatomic/awebapp
```




