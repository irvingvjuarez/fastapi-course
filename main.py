from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from utils.get_movie import get_movie
from utils.get_data import get_data

app = FastAPI()
app.title = "My very first FastAPI application"

@app.get("/", tags=["Home"])
def root():
	return HTMLResponse("<h1>Hello World</h1>")

@app.get("/movies", tags=["Movies"])
def get_movies(category: str = None):
	current_movies = get_data()

	if category:
		updated_movies = list(
			filter(lambda item: category in item["category"], current_movies)
		)
		current_movies = updated_movies

	return current_movies

@app.get("/movie/{movie_id}", tags=["Movies"])
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

@app.post("/movie", tags=["Movies"], status_code=status.HTTP_201_CREATED)
async def add_movie(request: Request):
	movie = await request.json()

	try:
		current_movies = get_data()
		movie["id"] = len(current_movies) + 1
		current_movies.append(movie)

		return movie
	except:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"There was an error adding the movie, try again later"
		)

@app.put("/movie/{movie_id}")
async def modify_movie(movie_id, request: Request):
	new_properties = await request.json()

	try:
		new_movie, movie_index = get_movie(id=movie_id)
	except:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

	new_movie.update(new_properties)
	db.data.get("data")[movie_index] = new_movie

	return new_movie