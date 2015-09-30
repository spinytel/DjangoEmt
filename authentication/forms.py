from django import forms
from authentication.models import Account


# Author : @mamun0024
class UserForm(forms.ModelForm):
    username = forms.CharField(label='Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    email = forms.CharField(label='Email', required=True, widget=forms.TextInput(attrs={'placeholder': 'User Email'}))
    password = forms.CharField(label='Password', max_length=200, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=200, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    is_admin = forms.ChoiceField(label="User Type", choices=[(False, 'General'), (True, 'Administrator')], widget=forms.Select(attrs={'class': 'selection'}), required=False)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'confirm_password')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Author : @mamun0024
class UserEditForm(forms.Form):
    username = forms.CharField(label='Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    email = forms.CharField(label='Email', required=True, widget=forms.TextInput(attrs={'placeholder': 'User Email'}))
    is_admin = forms.ChoiceField(label="User Type", choices=[(False, 'General'), (True, 'Administrator')], widget=forms.Select(attrs={'class': 'selection'}), required=False)
    user_pre_id = forms.CharField()
