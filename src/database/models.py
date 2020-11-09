#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask_migrate import Migrate
import json
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy import Column, String, Integer
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#