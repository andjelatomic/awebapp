from sqlalchemy import Column, String, TEXT, Integer,BLOB, DateTime, Boolean, DECIMAL, select, MetaData
from  database import Base

class Stock(Base):
     __tablename__="stock"
     stockid = Column(Integer, primary_key=True, index=True)
     nameoftheitem = Column(String)
    #slugnameoftheitem = Column(String, unique=True)
     description = Column(TEXT)
     price = Column(DECIMAL(scale=2))
     possiblediscount = Column(Boolean)
     image = Column(BLOB)
     categoryid = Column(Integer) # , ForeignKey("categories.categoryid"))
     totalamountonstock = Column(Integer)

class Categories(Base):
     __tablename__="categories"
     categoryid = Column(Integer, primary_key=True, index=True)
     name = Column(String)
     description = Column(TEXT)

class Sold(Base):
     __tablename__="sold"
     soldid = Column(Integer, primary_key=True, index=True)
     stockid = Column(Integer)
     customerid = Column(Integer)
     when = Column(DateTime)

class Customers(Base):
     __tablename__="customers"
     customerid = Column(Integer, primary_key=True, index=True)
     loginname = Column(String, unique=True)
     passwordmd5 = Column(String)
     lastlogin = Column(DateTime)
     #for the future development
     #email = Column(String)
     #phone = Column(String)
     #address = Column(String)

class Logins(Base):
     __tablename__="logins"
     id = Column(Integer, primary_key=True, index=True)
     customerid = Column(Integer)
     ip = Column(String)
     when = Column(DateTime)
     success = Column(Boolean)

class Shoppingbags(Base):
     __tablename__="shoppingbags"
     shoppingbagid = Column(Integer, primary_key=True, index=True)
     customerid = Column(Integer)
     stockid = Column(Integer)
     when = Column(DateTime)


#class Images(Base):
#     __tablename__="shoppingbags"
#     imagesid = Column(Integer, primary_key=True, index=True)
#     image = Column(Blob)
#     stockid = Column(Integer)



def getAllCustomers(db: Customers):
     return db.query(Customers).all()

