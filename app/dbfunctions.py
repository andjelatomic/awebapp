from sqlalchemy.orm import Session
from sqlalchemy import Column, String, TEXT, Integer,BLOB, DateTime, Boolean, DECIMAL, select, MetaData,func
from sqlalchemy.sql.expression import func
from  database import Base
from database import engine
from database import SessionLocal
import models
from sqlalchemy.sql import text
from requests_toolbelt.multipart import decoder
from datetime import datetime


#from globals import currentuserid

from starlette.formparsers import MultiPartParser, FormParser
from starlette.datastructures import Headers
import asyncio


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# GET ALL THE ITEMS FROM THE STOCK TABLE
def stocklist(db: Session):
    allitems = db.query(models.Stock).all()
    return allitems


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# GET AVAILABLE ITEMS FROM THE STOCK TABLE
def stocklistavailable(db: Session):
    availableitems = db.query(models.Stock).filter(models.Stock.totalamountonstock > 0)
    return availableitems

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# HOME PAGE ACTION
#    items = dbfunctions.homepageaction(request, action,  pagedata, cuid, db=db)

def homepageaction(request, homeformdata, curuid, db: Session): 
  
     # GET ACTION AND SEARCH STRING
     action:str = homeformdata['actionhome']
     homesearch:str = homeformdata['homesearch']
   
     # GET SELECTED ITEMS
     itemsforbag = []
     for formvalue in homeformdata:
         if formvalue.isnumeric():
             itemsforbag.append(formvalue)


     if action == "SEARCH":
       searchitems = db.query(models.Stock).filter(models.Stock.nameoftheitem.contains(homesearch)).filter(models.Stock.totalamountonstock > 0)
       return searchitems
     if action == "ADD TO BAG":
          ntime = datetime.now().strftime("%Y-%m-%d %H:%M:%f")
     
          query = []
          for pushtobag in itemsforbag:
            query.append("""INSERT INTO shoppingbags ([customerid], [stockid], [when]) VALUES(""" + str(curuid) + """,""" + pushtobag + """,datetime())""")
          
          with engine.connect() as con:
            for oneset in query:
                con.execute(oneset)
          con.close()
     #if action == # "VIEW BAG"

     availableitems = db.query(models.Stock).filter(models.Stock.totalamountonstock > 0)
     return availableitems


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# CHECK USER PASSWORD
# STILL NEED TO BE ENCRYPTED IN THE DATABASE!!! NOT DONE YET
def checkpassword(musername, mpassword, db: Session ):
    checkuser : Customers  = db.query(models.Customers).filter(models.Customers.loginname == musername and models.Customers.passwordmd5 == mpassword)
    cnt = checkuser.count()
    for record in checkuser:
       cusid = record.customerid

    if cnt>0:
        return cusid
    return 0

def createitem(nameoftheitem:str,description:str,price:int, db: Session):
    db_product = models.Shop(nameoftheitem=nameoftheitem, description=description, price=price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product




# -----------------------------------------------------------------------------------------------------------------------------------------------------
# SHOW CUSTOMER SHOPPING BAG
def viewcustomerbag(curuid, db: Session):
    bagquery = "SELECT sb.shoppingbagid as shoppingbagid, st.nameoftheitem as nameoftheitem , st.description as description, st.price as price, st.totalamountonstock as totalamountonstock FROM shoppingbags sb JOIN stock st ON st.stockid = sb.stockid WHERE sb.customerid=" + str(curuid) + " ORDER BY nameoftheitem"
    with engine.connect() as con:
        customerbag = con.execute(bagquery).fetchall()
    con.close()
    return customerbag


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# GET TOTAL TO PAY FROM THE CUSTOMER SHOPPING BAG
def viewcustomerbagtotal(curuid, db: Session):
    bagquery = "SELECT SUM(st.price) FROM shoppingbags sb JOIN stock st ON st.stockid = sb.stockid WHERE sb.customerid=" + str(curuid)
    with engine.connect() as con:
        totalinbag = con.execute(bagquery).fetchall()
    con.close()
    for row in totalinbag:
      totaltopay = row
    total = totaltopay[0]
    if not total:
        total = 0
    return total

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# GET CUSTOMER NAME
def getcustomername(curuid, db: Session):
    querycusname = "SELECT loginname FROM customers WHERE customerid=" + str(curuid)
    with engine.connect() as con:
        cgetname = con.execute(querycusname).fetchall()
    con.close()
    for row in cgetname:
      customername = row
    return customername[0]


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# DELETE FROM SHOPPING BAG
def deleteshoppingbag(homeformdata, curuid, db:Session):
    # GET SELECTED ITEMS
    itemstodelete = []
    for formvalue in homeformdata:
         if formvalue.isnumeric():
             itemstodelete.append(formvalue)
    if itemstodelete:
        query = []
        for todelete in itemstodelete:  
            query.append("DELETE FROM shoppingbags WHERE [shoppingbagid] =" + todelete)

        with engine.connect() as con:
            for oneset in query:
                con.execute(oneset)
            con.close()
        
        # CALL VIEW BAG
    viewcustomerbag(curuid, db)

# FOR FUTURE DEVELOPMENT -> IF CUSTOMER HAS 2 OR MORE ITEMS OF THE SAME THING, THEN DELETE WILL DECREASE THAT
# -----------------------------------------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# ADD NEW CUSTOMER
def addnewcustomer(username, password, db: Session):
    newcutomerquery = "INSERT INTO customers ([loginname], [passwordmd5]) VALUES('" + username + "','" + password +"')"
    with engine.connect() as con:
        customerbag = con.execute(newcutomerquery)
    con.close()
    return 0


# -----------------------------------------------------------------------------------------------------------------------------------------------------
# INSERT LAST LOGIN
def insertloginlog(curid, ip, success, db: Session):
    lastlogin = "INSERT INTO logins ([customerid], [ip] , [when], [success]) VALUES(" + str(curid) + ",'" + ip + "', datetime(), " + str(success) + ")"
    with engine.connect() as con:
        customerbag = con.execute(lastlogin)
    con.close()
    return 0

