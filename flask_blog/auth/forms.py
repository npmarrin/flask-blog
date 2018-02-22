from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError

from .models import User


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 320),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(8)
        ]
    )


class RegistrationForm(LoginForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(1, 70)
        ]
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
