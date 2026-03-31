
from django.forms import ModelForm, Form, CharField, PasswordInput
from django.contrib.auth.hashers import make_password

from .models import Users


class UserRegisterForm(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'username', 'password']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)
    
    
    
class UserLoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)