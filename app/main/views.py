from flask import render_template,request,redirect,url_for
from . import main
from .. import db
from ..models import User
from flask_login import login_required
# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting pitches
    title = '60 seconds to impress someone'
    user= User.query.all()
    
    return render_template('index.html', title = title,user = user)

