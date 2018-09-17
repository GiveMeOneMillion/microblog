#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from app.models import User
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember_me=BooleanField('记住我的选择')
    submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('请输入一个其他的用户名.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('请使用不同的电子邮件地址.')

#配置文件编辑器表单
class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('有关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')
    #在编辑个人资料表单中验证用户名
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已注册')

#博客提交表单
class PostForm(FlaskForm):
    post = TextAreaField('说点什么吧！', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')