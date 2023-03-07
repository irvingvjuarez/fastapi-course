from fastapi import FastAPI, HTTPException, status
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

@app.get("/movie/{movie_id}", tags=["Movies"])
def get_movie_detail(movie_id: int):
	matching_movies = list(
		filter(lambda movie: movie["id"] == movie_id, db.data.get("data"))
	)

	matches = len(matching_movies)
	if matches == 1:
		return matching_movies[0]
	elif matches > 1:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="There has been an error retrieving the data, please try again later"
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Movie with id {movie_id} not found."
		)