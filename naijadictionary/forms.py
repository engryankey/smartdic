from django import forms
from django.contrib.auth.models import User
from naijadictionary.models import UserProfile, Submited
from django.core import validators

BIRTH_YEAR_CHOICES = []
for year in range(1930, 2010):
    BIRTH_YEAR_CHOICES.append(year)

GENDER = [
    ('', 'Gender'),
    ('male', 'Male'),
    ('female', 'Female')
]

class DefinitionForm(forms.Form):
    word = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Search for a word...', 'type':'search', 'class':'form-control', 'id':'dictfield'}))
    
class UserInfoForm(forms.ModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'placeholder':'Re-enter password', 'class':'form-control'}))
    username = forms.SlugField(min_length=4, widget=forms.TextInput(attrs={'placeholder':'Enter your desired username', 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'First Name', 'class': 'form-control', 'required':'True', 'minlength':3}),
            'last_name': forms.TextInput(attrs={'placeholder':'Last Name', 'class': 'form-control', 'required':'True', 'minlength':4}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control', 'required':'True'}),
        }

    # def clean(self):
    #     all_clean = super().clean()
    #     user_name = all_clean.get("username")
    #     fn = all_clean.get("first_name")

    #     if user_name[0].isdigit() == True:
    #         raise forms.ValidationError("Your username can't start with a number.")
    #     elif fn.isalpha() == False:
    #         raise forms.ValidationError("Your username can't start with a number.")

        

    def clean_first_name(self):
        fn = self.cleaned_data['first_name']
        if fn.isalpha() == False:
            raise forms.ValidationError("Your First Name must be all letters.")
        return fn

    def clean_last_name(self):
        ln = self.cleaned_data['last_name']
        if ln.isalpha() == False:
            raise forms.ValidationError("Your Last Name must be all letters.")
        return ln

    def clean_username(self):
        un = self.cleaned_data['username']
        if un[0].isdigit() == True:
            raise forms.ValidationError("Your Username can't start with a number.")
        return un

    def clean_password(self):
        pw = self.cleaned_data['password']
        if pw.isalpha() == True:
            raise forms.ValidationError("Please include atleast a number.")
        elif pw.isdigit() == True:
            raise forms.ValidationError("Must consist of letters and numbers.")
        return pw
        

    def clean(self):
        all_clean = super().clean()
        pw = all_clean.get("password")
        pw2 = all_clean.get("password2")

        if pw != pw2:
            raise forms.ValidationError("Your passwords don't match.")    


class UserProfileInfoForm(forms.ModelForm):

    gender = forms.ChoiceField(choices=GENDER, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    age = forms.IntegerField(label='DOB', widget=forms.NumberInput(attrs={'class':'form-control', 'id':'age', 'placeholder':'Age'}), required=True)
    location = forms.CharField(min_length=3, required=True, widget=forms.TextInput(attrs={'placeholder':'City', 'class':'form-control'}))
    class Meta:
        model = UserProfile
        fields = ('portfolio_url', 'profile_pic', 'gender', 'age', 'location')
        widgets = {
            'portfolio_url': forms.URLInput(attrs={'placeholder':'Enter your Portfolio url addres', 'class':'form-control', 'required':'False'}),
            'profile_pic': forms.FileInput(attrs={'placeholder':'Enter your Portfolio url addres', 'class':'form-control', 'id':'profile_pic'}),
        }

class SubmitedForm(forms.ModelForm):
    user_name = forms.CharField(min_length=3, required=True, widget=forms.HiddenInput(attrs={'placeholder':'City', 'class':'form-control'}))
    word = forms.CharField(min_length=3, required=True, help_text='Kindly type the word correctly.', widget=forms.TextInput(attrs={'placeholder':'Word', 'class':'form-control'}))
    meaning = forms.CharField(min_length=3, required=True, help_text='Now explain what this word means.', widget=forms.Textarea(attrs={'placeholder':'Meaning', 'class':'form-control', 'rows':5}))
    language = forms.CharField(min_length=3, required=True, help_text='Which language owns this word?', widget=forms.TextInput(attrs={'placeholder':'Language', 'class':'form-control'}))
    exampe = forms.CharField(min_length=3, required=True, help_text='Using a detailed sentence, give an example of how this word is used.', widget=forms.Textarea(attrs={'placeholder':'Example', 'class':'form-control', 'rows':3}))
    class Meta:
        model = Submited
        fields = ('user_name', 'word', 'meaning', 'language', 'exampe')
