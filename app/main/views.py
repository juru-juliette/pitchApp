from . import main
from .. import db
from ..models import User,Pitch
from flask_login import login_required
# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular movie
    title = '60 seconds to impress someone'
    pitch = Pitch.query.all()
    
        return render_template('index.html', title = title)

