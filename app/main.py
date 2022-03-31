from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request, Response, Form, Body,Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


import uvicorn
import dbfunctions
import models
import webschemas
import os
import requests
import json

#from globals import currentuserid
from webschemas import HomePageData
from database import engine, SessionLocal


import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore',
 r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
 "and SQLAlchemy must convert from floating point - rounding errors and other "
 "issues may occur\. Please consider storing Decimal numbers as strings or "
 "integers on this platform for lossless storage\.$",
 SAWarning, r'^sqlalchemy\.sql\.type_api$')


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#@app.get('../static/favicon.ico', include_in_schema=False)

homepageheadings = ("Select to buy", "Name of the item","Description","Price","Avalilable on stock")


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# LOGIN PAGE
# -----------------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def login_form_post(request: Request):
    message = "Please enter your username and password"
    return templates.TemplateResponse('login.html', context={'request': request, 'message': message})

@app.post("/")
async def login_form_post(request: Request, response: Response, db: Session() = Depends(get_db)):
    homeform_data = await request.form()
    action:str = homeform_data['action']
    if action == 'NEW CUSTOMER':
      return RedirectResponse(url="/newuser", status_code=303)
    
    username:str = homeform_data['username']
    password:str = homeform_data['password']
    ip = request.client.host

    if action == 'LOGIN':
     logged = dbfunctions.checkpassword(username, password, db=db)
     if logged > 0:
        dbfunctions.insertloginlog(logged, ip, True, db=db)
        rr = RedirectResponse(url="/home", status_code=303)
        rr.set_cookie(key="myshopid", value=str(logged), httponly=True)
        return rr

    message = "Wrong password or user doesn't exist"
    return templates.TemplateResponse('login.html', context={'request': request, 'message': message})


# -----------------------------------------------------------------------------------------------------------------------------------------------------
#HOME PAGE
# -----------------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/home", response_class=HTMLResponse)
def showavailableitems(request: Request, myshopid: Optional[str] = Cookie("myshopid"), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = dbfunctions.stocklistavailable(db=db)
    cuid = request.cookies.get("myshopid")
    currentuser_name = dbfunctions.getcustomername(cuid, db)
    return templates.TemplateResponse("index.html", context={'request': request, 'headings': homepageheadings,'items': items, 'currentusername' : currentuser_name})


@app.post("/home")
async def showavailableitems(request: Request, db: Session = Depends(get_db)):         
    homeform_data = await request.form()
    action:str = homeform_data['actionhome']
    if action =="VIEW BAG":
        return RedirectResponse(url="/viewbag", status_code=303)

    currentuserid = request.cookies.get("myshopid")
    items = dbfunctions.homepageaction(request, homeform_data, currentuserid, db=db)
    return templates.TemplateResponse("index.html", context={'request': request, 'headings': homepageheadings, 'items': items})

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------------------------------
#NEW CUSTOMER
# -----------------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/newuser") #, response_class=HTMLResponse)
def showavailableitems(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("newcustomer.html", context={'request': request, 'newusername': "", 'newpassword':"", 'message':"Please eneter your preferable credentials"})

@app.post("/newuser")
async def showavailableitems(request: Request, response: Response, newusername: str = Form(...), newpassword: str = Form(...), db: Session = Depends(get_db)):
    dbfunctions.addnewcustomer(newusername, newpassword, db=db)
    return RedirectResponse("/", status_code=303)

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------


#VIEW BAG
# -----------------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/viewbag", response_class=HTMLResponse)
def showavailableitems(request: Request, db: Session = Depends(get_db)):
    currentuserid = request.cookies.get("myshopid")
    currentuser_name = dbfunctions.getcustomername(currentuserid, db)
    items = dbfunctions.viewcustomerbag(currentuserid, db=db)
    total = dbfunctions.viewcustomerbagtotal(currentuserid, db=db)
    return templates.TemplateResponse("viewbag.html", context={'request': request,  'headings': homepageheadings,  'items': items, 'customername': currentuser_name, 'total':total})


@app.post("/viewbag")
async def showavailableitems(request: Request, response: Response, db: Session = Depends(get_db)):
    currentuserid = request.cookies.get("myshopid")
    currentuser_name = dbfunctions.getcustomername(currentuserid, db)
    homeform_data = await request.form()
    action:str = homeform_data['actionbag']
    if action =="HOME":
        return RedirectResponse("/home", status_code=303)         
    if action =="DELETE":
        items = dbfunctions.deleteshoppingbag(homeform_data, currentuserid,  db=db)         
    
    items = dbfunctions.viewcustomerbag(currentuserid, db=db)
    total = dbfunctions.viewcustomerbagtotal(currentuserid, db=db)
    return templates.TemplateResponse("viewbag.html", context={'request': request, 'headings': homepageheadings, 'items': items, 'customername': currentuser_name, 'total':total})

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------

# FOR THE FUTURE DEVELOPMENT
@app.post("/newitem/")
def createitem(stock:webschemas.Stock, db:Session = Depends(get_db)):
    return dbfunctions.createitem(nameoftheitem=stock.nameoftheitem
                               ,description=stock.description,
                               price=stock.price,db=db)

@app.get("/listall/", response_class=HTMLResponse)
def allstocklist(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = dbfunctions.stocklistavailable(db=db)
    return templates.TemplateResponse("list.html", context={'request': request, 'items': items})
#   return dbfunctions.stocklist(db=db)

# 
@app.get("/items/{itemid}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"itemid": itemid, "q": q}

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------



#SET PORT AND LOCAL HOST FOR THE uvicorn WEBSERVER  AND RUN THE WEB SERVER   
if __name__ == '__main__':
    uvicorn.run(app, port=8001, host="0.0.0.0") # log_level="debug")

