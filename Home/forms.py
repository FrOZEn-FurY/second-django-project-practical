from django import forms

class SearchInListForm(forms.Form):
    search = forms.CharField(required=False)