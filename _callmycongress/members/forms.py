from django import forms


class MemberSearchForm(forms.Form):
    CHAMBER_CHOICES = (
        ('', 'Both'),
        ('legislatorLowerBody', 'House'),
        ('legislatorUpperBody', 'Senate')
    )
    address = forms.CharField(
        max_length=160,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address or zipcode'})
    )
    # zipcode = forms.CharField(
    #     max_length=6,
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    roles = forms.ChoiceField(
        required=False,
        choices=CHAMBER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )