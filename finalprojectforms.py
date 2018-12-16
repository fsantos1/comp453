from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Department, getDepartment, getDepartmentFactory
from wtforms.fields.html5 import DateField

class createproductform(FlaskForm):

    ProductID = IntegerField('Product ID:'
    NameOfProduct = StringField('Name of Product:')
    Manufacturer = StringField("Manufacturer:")
    Price = IntegerField("Price:")
    RAM = IntegerField("RAM:")
    ScreenSize = IntegerField('Screen Size:')
    submit = SubmitField('Update this department')

    

