from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.Models.Admin import Admin
from src.db import db

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def index():
    admins = Admin.query.all()
    return render_template('web/index.html', admins=admins)
