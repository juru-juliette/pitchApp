from flask import render_template,redirect,url_for
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm
from flask_login import login_user,logout_user,login_required