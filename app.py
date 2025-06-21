from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Add rate limiting exception handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Apply rate limiting to all routes
app.state.limiter = limiter

@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Book Publication API"}

# ... rest of your existing code ...
from api.v1.router import router as v1_router
app.include_router(v1_router)
from monitoring.prometheus import setup_prometheus
setup_prometheus(app)
from error_handlers import setup_error_handlers
setup_error_handlers(app)
from health import router as health_router
app.include_router(health_router)
from logging_config import setup_logging
setup_logging()
from middleware.tracing import RequestTracingMiddleware
app.add_middleware(RequestTracingMiddleware)
from endpoints.chapters import router as chapters_router
app.include_router(chapters_router)
from fastapi import FastAPI
from init_db import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
from fastapi import FastAPI
from init_db import create_db_and_tables
import os

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("Starting up...")
    if not os.path.exists('bookpub.db'):
        create_db_and_tables()
    else:
        print("Database already exists at:", os.path.abspath('bookpub.db'))
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import (
    fake_users_db,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
