from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import db

app = FastAPI()
app.title = "My very first FastAPI application"

@app.get("/", tags=["Home"])
def root():
	return HTMLResponse("<h1>Hello World</h1>")

@app.get("/movies", tags=["Movies"])
def get_movies():
	return db.data