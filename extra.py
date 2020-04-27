from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    """Contact form."""
    name = StringField('Username', [
        validators.DataRequired(message="You need to provide a username")], 
        id="reg_username")
    
    email = StringField('Email Address', [
        validators.Email(message=('Not a valid email address.')),
        validators.DataRequired()], id="reg_email")
    
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'), 
        validators.Length(min=8, message=('Your password is too short.'))], id="reg_password")
    
    confirm = PasswordField('Repeat Password', id="reg_password_confirm")
    
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()], id="reg_agree")