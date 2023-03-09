from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from utils import get_movie, get_data, modify_movies
from models.movie import Movie
import random

app = FastAPI()
app.title = "My very first FastAPI application"

@app.get("/", tags=["Home"])
def root():
	return HTMLResponse("<h1>Hello World</h1>")

@app.get("/movies", tags=["Movie"])
def get_movies(category: str = None):
	current_movies = get_data()

	if category:
		updated_movies = list(
			filter(lambda item: category in item["category"], current_movies)
		)
		current_movies = updated_movies

	return current_movies

@app.get("/movie/{movie_id}", tags=["Movie"])
def get_movie_detail(movie_id: int):
	matching_movies = list(
		filter(lambda movie: movie["id"] == movie_id, get_data())
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

@app.post("/movie", tags=["Movie"], status_code=status.HTTP_201_CREATED)
async def add_movie(movie: Movie):
	current_movies = get_data()

	movie.update({"id": random.randInt()})
	current_movies.append(movie)

	try:
		modify_movies(current_movies)
		return movie
	except:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.put("/movie/{movie_id}", tags=["Movie"])
async def modify_movie(movie_id, request: Request):
	new_properties = await request.json()

	try:
		new_movie, movie_index = get_movie(id=movie_id)
	except:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

	new_movie.update(new_properties)

	try:
		new_data = get_data()
		new_data[movie_index] = new_movie
		modify_movies(new_data)
	except:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return new_movie

@app.delete("/movie/{movie_id}", tags=["Movie"])
def delete_movie(movie_id):
	try:
		_, movie_index = get_movie(id=movie_id)
	except:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

	movies = get_data()
	deleted_movie = movies.pop(movie_index)

	try:
		modify_movies(movies)
	except:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return deleted_movie