from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    """Registration form."""
    name = StringField('Username', validators=[
        DataRequired(message="You need to provide a username")], 
        id="reg_username")
    
    email = StringField('Email Address', validators=[
        Email(message=('Not a valid email address.')),
        DataRequired()], id="reg_email")
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'), 
        Length(min=8, message=('Your password is too short.'))], id="reg_password")
    
    confirm = PasswordField('Repeat Password', validators=[DataRequired(message='Please confirm password')],id="reg_password_confirm")
    
    submit = SubmitField('Submit')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()], id="reg_agree")

class LoginForm(FlaskForm):
    """Login form."""
    name = StringField('Username', validators=[
        DataRequired(message="You need to provide a username")])

    password = PasswordField('Password', validators=[
        DataRequired(message="You need to provide a password")])

    submit = SubmitField('Submit')
