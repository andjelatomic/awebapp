from pydantic.main import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Request, Response, Form


#Schema 

class Stock(BaseModel):
    nameoftheitem: str
    description: str
    price: str
    totalamountonstock: int

    class Config:
        orm_mode=True


class Login(BaseModel):
    username: str = Form(..., title="Username", max_lengthe=32)
    password: str = Form(..., title="Password")


class HomePageData(BaseModel):
    but_addtobag: str = ""
    but_search: str = ""
    but_viewbag: str = ""
    search: str = ""
 #   items: list = []
    @classmethod
    def as_form(
      cls,
       but_addtobag: str = Form(...),
       but_search: str= Form(...),
       but_viewbag: str= Form(...),
       search: str=Form(...)
    ):
        return cls(
            but_addtobag=but_addtobag,
            but_search=but_search,
            but_viewbag= but_viewbag,
            search=search
        )