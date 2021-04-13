from django import forms
from tempus_dominus.widgets import DateTimePicker
from .models import VManager, User, News


class VenueForm(forms.Form):
    name = forms.CharField(max_length=100)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'venue-address'}), label="Indirizzo:")
    url = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-control', 'id': 'venue-url'}), label='URL:')
    category = forms.TextInput()
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'venue-description'}),
        label="Descrizione:",
        max_length=400)


class EventForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descrivi il tuo evento',
            }),
        label='Descrizione evento',
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Titolo dell'evento",
            }
            ),
        label='TItolo',
    )

    venue = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Venue',
            }),
        label='Venue',
        empty_label='Scegli la venue'
    )

    date = forms.DateField(
        widget=DateTimePicker(
            options={'format': 'YYYY/MM/DD HH:mm'},
            attrs={
                'class': 'form-control datetimepicker',
                'id': 'datetimepicker1',
                'placeholder': 'Data',
                'data-target': '#datetimepicker1'
            },
        )
    )

    class Meta:
        model = News
        fields = ['author', 'venue', 'description', 'title', 'date']


class NewsForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Contenuto articolo',
            }),
        label='Contenuto',
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Titolo dell'articolo",
            }
            ),
        label='Titolo',
    )

    venue = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Venue',
            }),
        label='Venue',
        empty_label='Scegli la venue'

    )

    class Meta:
        model = News
        fields = ['author', 'venue', 'content', 'title']
