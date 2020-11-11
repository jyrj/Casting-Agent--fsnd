import os
from flask_migrate import Migrate
import json
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy import Column, String, Integer
from forms import *

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
databse_path = "postgresql:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()
