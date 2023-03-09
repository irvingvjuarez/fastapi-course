import json
import sys
sys.path.append("../db")

def get_data():
	file = open("db/data.json")
	data = json.load(file)
	file.close()

	return data.get("data")
