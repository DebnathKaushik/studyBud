from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm


class My_user_creation_register_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username','email','password1','password2']



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email']