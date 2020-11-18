import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
databse_path = "postgresql:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()
