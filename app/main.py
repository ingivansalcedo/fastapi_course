from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1 import auth
from app.api.v1.api import api_router
from app.deps import get_db

app = FastAPI()

@app.post("/login", response_model=auth.schemas.Token)
def login_alias(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth.login(form_data=form_data, db=db)

app.include_router(api_router, prefix="/api/v1")
