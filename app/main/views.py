from flask import render_template,request,redirect,url_for,abort
from . import main
from .. import db,photos
from ..models import User,Pitch,Comment
from flask_login import login_required,current_user
from .forms import ReviewForm,UpdateProfile,CreatePitches,CommentForm
# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting pitches
    title = '60 seconds to impress someone'
    pitch = Pitch.query.all()
    comment = Comment.query.all()
    return render_template('index.html', title = title,pitch = pitch, comment = comment)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def create_pitches():
    form = CreatePitches()

    if form.validate_on_submit():

        pitch=form.post.data
        title=form.title.data
        new_pitch=Pitch(pitch = pitch,user= current_user,title = title)

        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('pitches.html',form = form,user= current_user) 

def create_comments(id):

    form = CommentForm()

    if form.validate_on_submit():

        comment=form.comment.data

        new_comment= Comment(comment= comment,pitches_id = id,user= current_user)
        db.session.add(new_comment)
        db.session.commit()

    comment = Comment.query.filter_by(pitches_id=id).all()
        

    return render_template('comment.html',comment = comment, form = form)        

