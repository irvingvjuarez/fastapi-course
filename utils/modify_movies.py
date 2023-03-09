import re

def modify_movies(data: dict):
	with open("db/data.json", "w") as file:
		file.write(str(data).replace("'", '"'))

		file.close()