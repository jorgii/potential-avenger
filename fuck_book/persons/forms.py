from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from persons.models import Person


class UserForm(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PersonRegisterForm(ModelForm):
    class Meta:
        model = Person
        fields = ['gender', 'birth_date', 'city', 'photo']


class ProfileEditForm(ModelForm):

    class Meta:
        model = Person
        fields = ['gender',
                  'birth_date',
                  'city',
                  'photo',
                  'preferred_poses',
                  'preferred_places',
                  'notification_settings']
