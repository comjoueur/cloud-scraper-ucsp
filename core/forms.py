from django import forms


class SearchForm(forms.Form):
    term = forms.CharField(label="Search Term", max_length=1000)
