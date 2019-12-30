from django import forms
from django.contrib.auth.forms import UserCreationForm as uC ,UserChangeForm as uCF
from .models import custm_user
from django.contrib.auth import authenticate

class loginForm(forms.Form):
    username= forms.CharField(label='Your username',max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Your Password',max_length=32, widget=forms.PasswordInput(attrs={"class":"form-control"}))

    def clean(self):
        username=self.cleaned_data["username"]
        password=self.cleaned_data["password"]
        usr= authenticate(username=username,password=password)
        if usr:
            return
        else:
            raise forms.ValidationError("Invalid data")
        

class UserCreationForm(uC):
    class Meta:
        model = custm_user
        fields =  ['username','email','password1','password2']
        # exclude = ['age']

class UserChangeForm(uCF):
    class Meta:
        model = custm_user
        fields =  ['username','email','first_name','last_name']
        # exclude = ['password'] 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = custm_user
        fields =  ['username','email','first_name','last_name','age','phone','dob','pro_pic']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True,'class':'readonly'}),
            'dob': forms.DateInput(attrs={"type":"date"}),
            'pro_pic':forms.FileInput(attrs={'class':'dp_selector'})
        }
        help_texts = {
            'username': "",
        }
        # exclude = ['password'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pro_pic'].required=False
        self.fields['dob'].widget.attrs['class'] = 'datepicker'


