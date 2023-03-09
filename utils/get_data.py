import sys
sys.path.append("../db")

import db

def get_data():
	return db.data.get("data")