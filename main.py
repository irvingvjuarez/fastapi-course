from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from utils import get_movie, get_data, modify_movies
from models.movie import Movie
from typing import List
from random import randint

app = FastAPI()
app.title = "My very first FastAPI application"

@app.get("/", tags=["Home"], status_code=status.HTTP_200_OK)
def root():
	return HTMLResponse("<h1>Hello World</h1>")

@app.get("/movies", tags=["Movie"], status_code=status.HTTP_200_OK, response_model=List[Movie])
def get_movies(category: str = None) -> List[Movie]:
	current_movies = get_data()

	if category:
		updated_movies = list(
			filter(lambda item: category in item["category"], current_movies)
		)
		current_movies = updated_movies

	return JSONResponse(content=current_movies)

@app.get("/movie/{movie_id}", tags=["Movie"], status_code=status.HTTP_200_OK, response_model=Movie)
def get_movie_detail(movie_id: int) -> Movie:
	matching_movies = list(
		filter(lambda movie: movie["id"] == movie_id, get_data())
	)

	matches = len(matching_movies)
	if matches == 1:
		return JSONResponse(content=matching_movies[0])
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

@app.post("/movie", tags=["Movie"], status_code=status.HTTP_201_CREATED, response_model=Movie)
async def add_movie(movie: Movie) -> Movie:
	current_movies = get_data()

	id = randint(1, 10000)
	assert type(id) == int, f"{id} must be an integer"

	new_movie = dict(movie)
	new_movie["id"] = id

	current_movies.append(new_movie)

	try:
		modify_movies(current_movies)
		return JSONResponse(content=new_movie)
	except:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.put("/movie/{movie_id}", tags=["Movie"], status_code=status.HTTP_200_OK)
async def modify_movie(movie_id, new_properties: Movie) -> Movie:
	try:
		new_movie, movie_index = get_movie(id=movie_id)
	except:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

	for key, value in list(dict(new_properties).items()):
		if value:
			new_movie[key] = value

	try:
		new_data = get_data()
		new_data[movie_index] = new_movie
		modify_movies(new_data)
	except:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return JSONResponse(content=new_movie)

@app.delete("/movie/{movie_id}", tags=["Movie"], status_code=status.HTTP_200_OK)
def delete_movie(movie_id) -> Movie:
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

	return JSONResponse(content=deleted_movie)