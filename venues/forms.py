from django import forms


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
