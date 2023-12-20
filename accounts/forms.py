from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PostModel, CommentModel, GeneralInfoModel

class UserRegisterationForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Example: MyUserName','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Example : Something@Someemail.me','class':'form-control'}),required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'Example : MyN@m3GG','class':'form-control'}))
    confirmpassword = forms.CharField(label= 'Confirm Password' ,required=True, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Repeat the password above'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        Email_Check = User.objects.filter(email=email).exists()
        if Email_Check:
            raise ValidationError('The email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        Username_Check = User.objects.filter(username=username).exists()
        if Username_Check:
            raise ValidationError('The username already exists')
        return username

    def clean(self):
        cd = super().clean()
        Pass = cd.get('password')
        ConfPass = cd.get('confirmpassword')
        if Pass and ConfPass and Pass != ConfPass:
            raise ValidationError('The passwords must match')

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username Or Email Address' ,required=True, widget=forms.TextInput(attrs={'placeholder':"Your account's username",'class':'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Your account's password"}))


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'body')

class CreateNewPostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'body')

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'class':'form-control'})
        }

class EditUserProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = GeneralInfoModel
        fields = ('age', 'bio')
        widgets = {
            'age' : forms.NumberInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'})
        }
