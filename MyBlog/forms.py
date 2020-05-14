from django import forms
from .models import Article


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class SubscriberForm(forms.ModelForm):
    model = 'Subscriber'
    fields = ['email']


class EditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'preview', 'text', 'tags']
