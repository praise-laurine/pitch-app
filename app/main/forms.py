from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    comment = TextAreaField('Write your comments here...',validators=[Required()])
    submit = SubmitField('Comment')


class PitchForm(FlaskForm):
    title = StringField('Pitch Title', validators=[Required()])
    author = StringField('Author', validators=[Required()])
    pitch_content = TextAreaField('Write Pitch', validators=[Required()])  
    category = RadioField('Pick Category', choices=[('Pickup Lines', 'Pickup Lines'), ('Interview Pitch', 'Interview Pitch'), ('Product Pitch', 'Product Pitch'), ('Promotion Pitch', 'Promotion Pitch')], validators=[Required()])  
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')    



