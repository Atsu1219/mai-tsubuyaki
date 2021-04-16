from django import forms
from .models import Message
from django.contrib.auth.models import User

from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    enter_password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザー名は既に使われています。別のユーザー名を利用してください。')
        return username

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('パスワードを5文字以上にしてください。')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'パスワードが一致しません。')

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        new_user = User.objects.create_user(username = username)
        new_user.set_password(password)
        new_user.save()

class PostForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'picture']
        labels = {
            'content': '',
            'picture': '',
        }
        widgets = {
            'content': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)