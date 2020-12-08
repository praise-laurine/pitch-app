from flask import render_template,request,redirect, url_for,abort
from . import main
from ..models import *
from flask_login import login_required,current_user
from .forms import * 
from .. import db,photos

# views
@main.route('/')
def index():
    '''
    view root page function that returns the index the page and its data
    '''
    title = 'Pitches'
    product_pitch = Pitch.query.filter_by(category = 'Product Pitch').all()
    interview_pitch = Pitch.query.filter_by(category = 'Interview Pitch').all()
    promotion_pitch = Pitch.query.filter_by(category = 'Promotion Pitch').all()
    love_pitch = Pitch.query.filter_by(category = 'Love Pitch').all()
    culture_pitch = Pitch.query.filter_by(category = 'Culture Pitch').all()
    inspiration_pitch = Pitch.query.filter_by(category = 'Inspiration Pitch').all()



    return render_template('index.html', title=title,product_pitch = product_pitch, interview_pitch = interview_pitch, promotion_pitch = promotion_pitch, love_pitch = love_pitch, culture_pitch= culture_pitch, inspiration_pitch = inspiration_pitch )


@main.route('/pitch/new_pitch', methods = ['POST', 'GET'])
@login_required  
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        pitch = Pitch(title = pitch_form.title.data, category = pitch_form.category.data, pitch_content = pitch_form.pitch_content.data, author = pitch_form.author.data)
        
        db.session.add(pitch)
        db.session.commit() 
        
        return redirect(url_for('main.index'))
    
    return render_template('new_pitch.html', pitch_form = pitch_form)   


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

@main.route('/categories/<cate>')
def category(cate):
    '''
    function to return the pitches by category
    '''
    category = Pitches.get_pitches(cate)
    # print(category)
    title = f'{cate}'
    return render_template('categories.html',title = title, category = category)







    



    
    
