from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
	username = TextField('username', validators = [Required()])
	email = TextField('email', validators = [Required()])

class ChallengeForm(Form):
	answer = TextField('answer', validators = [Required()])