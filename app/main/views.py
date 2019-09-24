from flask import render_template,request,redirect,url_for,abort
from . import main
from .. import db,photos
from ..models import User,Pitch,Category,Comment
from flask_login import login_required,current_user
from .forms import UpdateProfile,CreatePitches,CategoryForm,CommentForm

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting pitches
    title = '60 seconds to impress someone'
    pitch = Pitch.query.all()
    category = Category.get_categories()
    
    return render_template('index.html', title = title,pitch = pitch, category = category )

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}'s Profile"

    get_pitches = Pitch.query.filter_by(author = User.id).all()
    get_comments = Comment.query.filter_by(user_id = User.id).all()
    get_upvotes = Like.query.filter_by(user_id = User.id).all()
    get_downvotes = Dislike.query.filter_by(user_id = User.id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, title=title, pitches_no = get_pitches, comments_no = get_comments, likes_no = get_upvotes, dislikes_no = get_downvotes)

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
def pitch():
    form = CreatePitches()

    if form.validate_on_submit():
        
        title=form.title.data
        pitch=form.post.data
        new_pitch = Pitch(pitch = pitch,user= current_user,title = title)

        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('pitches.html',form = form,user= current_user)
 
@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    form = CategoryForm()

    if form.validate_on_submit():
        
        cat_name = form.name.data
        new_category = Category(cat_name = cat_name)
        new_category.save_category()
        return redirect(url_for('.index'))

    title='New category'
    return render_template('new_category.html',category_form = form, title = title)

# @main.route('/comment/new/<int:id>', methods=['GET','POST'])
# @login_required
# def create_comments(id):

#     form = CommentForm()

#     if form.validate_on_submit():

#         comment=form.comment.data

#         new_comment= Comment(comment= comment,pitches_id = id,user= current_user)
#         db.session.add(new_comment)
#         db.session.commit()

#     comment = Comment.query.filter_by(pitches_id=id).all()
        

#     return render_template('comment.html',comment = comment, form = form)   

@main.route('/pitch/<int:pitch_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    '''
    View comments page function that returns the comment page and its data
    '''
    # comment_form = CommentForm()

    comment_form = CommentForm()
    my_pitch = Pitch.query.get(pitch_id)
    if my_pitch is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_content = comment_form.comment_content.data

        new_comment = Comment(comment_content=comment_content, pitch_id = pitch_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', pitch_id=pitch_id))

    all_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    # all_comments = Comment.get_all_comments(id)
    # all_comments = Comment.get_all_comments(pitch_id)
    title = 'New Comment | Welcome to the Pitch Site'

    return render_template('comment.html', title = title, pitch=my_pitch ,comment_form = comment_form, comment = all_comments )





