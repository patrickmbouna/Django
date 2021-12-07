#from django import forms
from django.forms import ModelForm, TextInput, EmailInput, widgets
from .models import Contact
from django.forms.utils import ErrorList

class ParagraphErrorList(ErrorList):

    def __str__(self) -> str:
        return self.as_divs()

    def as_divs(self) -> str:
        if not self: return ''
        return '<div class="errorlist">%s </di>'%''.join(['<p class="smallerror">%s</p>'% e for e in self ])

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'Email': EmailInput(attrs={'class': 'form-control'}),
        }






""""class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nom',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )"""