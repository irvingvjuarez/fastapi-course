from .get_data import get_data
data = get_data()

def get_movie(**kwargs):
	movies = []

	for key, value in list(kwargs.items()):
		filtered_movies = [(movie, index) for index, movie in enumerate(data) if movie[key] == int(value)]
		movies = filtered_movies

	if len(movies) == 1:
		return movies[0][0], movies[0][1]

	return list(map(lambda x: x[0], movies))